#!/usr/bin/env python3
"""Parallel crawler for Moltbook - streaming Producer-Consumer pattern."""
import argparse
import logging
import sys
import threading
import queue
import time
from typing import Set

from moltbook import config
from moltbook.crawler import MoltbookCrawler
from moltbook.db import init_db, save_post, get_post_count, get_comment_count, get_all_post_ids


class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
            return self._value
    
    @property
    def value(self):
        with self._lock:
            return self._value


class ThreadSafeSet:
    def __init__(self, initial: Set[str] = None):
        self._set = set(initial) if initial else set()
        self._lock = threading.Lock()
    
    def add(self, item):
        with self._lock:
            self._set.add(item)
    
    def __contains__(self, item):
        with self._lock:
            return item in self._set
    
    def __len__(self):
        with self._lock:
            return len(self._set)


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/crawler.log')
        ]
    )


def worker_thread(worker_id: int, url_queue: queue.Queue, known_ids: ThreadSafeSet, 
                  counter: ThreadSafeCounter, headless: bool, stop_event: threading.Event):
    """Worker thread that continuously processes URLs from queue."""
    logger = logging.getLogger(__name__)
    save_lock = threading.Lock()
    
    while not stop_event.is_set():
        try:
            url = url_queue.get(timeout=2)
        except queue.Empty:
            continue
        
        if url is None:  # Poison pill to stop worker
            url_queue.task_done()
            break
        
        post_id = url.split("/post/")[-1].split("?")[0]
        
        # Skip if already saved
        if post_id in known_ids:
            url_queue.task_done()
            continue
        
        try:
            with MoltbookCrawler(headless=headless) as crawler:
                post = crawler.parse_post(url)
                
                if post:
                    with save_lock:
                        save_post(post)
                        known_ids.add(post.id)
                    count = counter.increment()
                    logger.info(f"[W{worker_id}] ✓ #{count} {post.title[:35]}... ({len(post.comments)} comments)")
                else:
                    logger.warning(f"[W{worker_id}] ✗ Failed: {url}")
        except Exception as e:
            logger.error(f"[W{worker_id}] Error: {url} - {e}")
        
        url_queue.task_done()


def producer_thread(url_queue: queue.Queue, known_ids_initial: Set[str], 
                    headless: bool, max_posts: int, batch_size: int, stop_event: threading.Event):
    """Producer thread that collects URLs and puts them in queue."""
    logger = logging.getLogger(__name__)
    total_queued = 0
    
    try:
        with MoltbookCrawler(headless=headless) as crawler:
            for batch in crawler.stream_post_links(
                known_ids=known_ids_initial,
                max_posts=max_posts,
                batch_size=batch_size
            ):
                if stop_event.is_set():
                    break
                    
                for url in batch:
                    url_queue.put(url)
                    total_queued += 1
                
                logger.info(f"[Producer] Queued batch: +{len(batch)} (total queued: {total_queued})")
                
                if max_posts and total_queued >= max_posts:
                    break
    except Exception as e:
        logger.error(f"[Producer] Error: {e}")
    
    logger.info(f"[Producer] Done. Total URLs queued: {total_queued}")


def main():
    parser = argparse.ArgumentParser(description='Moltbook Streaming Parallel Crawler')
    parser.add_argument('--limit', type=int, default=None,
                        help='Maximum number of NEW posts to crawl (default: all)')
    parser.add_argument('--workers', type=int, default=config.PARALLEL_WORKERS,
                        help=f'Number of parallel browser instances (default: {config.PARALLEL_WORKERS})')
    parser.add_argument('--batch-size', type=int, default=20,
                        help='Links per batch from feed (default: 20)')
    parser.add_argument('--no-headless', action='store_true',
                        help='Run browser in visible mode')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Moltbook STREAMING Parallel Crawler")
    logger.info(f"Workers: {args.workers} | Batch Size: {args.batch_size}")
    logger.info("=" * 60)
    
    init_db()
    logger.info(f"Database: {config.DB_PATH}")
    
    known_ids_initial = get_all_post_ids()
    known_ids = ThreadSafeSet(known_ids_initial)
    initial_count = len(known_ids)
    logger.info(f"Posts in DB: {initial_count}")
    
    headless = not args.no_headless
    start_time = time.time()
    
    # Shared resources
    url_queue = queue.Queue(maxsize=200)
    counter = ThreadSafeCounter()
    stop_event = threading.Event()
    
    try:
        # Start producer thread (collects links)
        producer = threading.Thread(
            target=producer_thread,
            args=(url_queue, known_ids_initial, headless, args.limit, args.batch_size, stop_event)
        )
        producer.start()
        
        # Start worker threads (process posts)
        workers = []
        for i in range(args.workers):
            w = threading.Thread(
                target=worker_thread,
                args=(i+1, url_queue, known_ids, counter, headless, stop_event)
            )
            w.start()
            workers.append(w)
        
        # Wait for producer to finish
        producer.join()
        
        # Wait for queue to be processed
        url_queue.join()
        
        # Stop workers
        for _ in workers:
            url_queue.put(None)
        for w in workers:
            w.join(timeout=5)
            
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("Interrupted! Stopping gracefully...")
        stop_event.set()
    
    # Summary
    elapsed = time.time() - start_time
    new_posts = get_post_count() - initial_count
    logger.info("=" * 60)
    logger.info("Crawling Complete!")
    logger.info(f"Time: {elapsed/60:.1f} min | New posts: {new_posts}")
    logger.info(f"Total posts: {get_post_count()} | Comments: {get_comment_count()}")
    if elapsed > 60:
        logger.info(f"Speed: {new_posts / (elapsed/60):.1f} posts/min")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
