#!/usr/bin/env python3
"""Main entry point for Moltbook crawler."""
import argparse
import logging
import sys

from moltbook import config
from moltbook.crawler import MoltbookCrawler
from moltbook.db import init_db, save_post, get_post_count, get_comment_count, get_all_post_ids


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/crawler.log')
        ]
    )


def main():
    parser = argparse.ArgumentParser(description='Moltbook Post Crawler')
    parser.add_argument('--limit', type=int, default=None,
                        help='Maximum number of NEW posts to crawl (default: all)')
    parser.add_argument('--batch-size', type=int, default=10,
                        help='Number of posts to collect before processing (default: 10)')
    parser.add_argument('--no-headless', action='store_true',
                        help='Run browser in visible mode (for debugging)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 50)
    logger.info("Moltbook Crawler Starting (Streaming Mode)")
    logger.info("=" * 50)
    
    # Initialize database
    init_db()
    logger.info(f"Database initialized at: {config.DB_PATH}")
    
    # Load existing post IDs for skip logic
    known_ids = get_all_post_ids()
    logger.info(f"Current posts in DB: {len(known_ids)}")
    
    # Start crawling
    headless = not args.no_headless
    new_posts = 0
    failed_posts = 0
    batch_num = 0
    
    try:
        with MoltbookCrawler(headless=headless) as crawler:
            # Stream post links and process immediately
            for batch in crawler.stream_post_links(
                known_ids=known_ids,
                max_posts=args.limit,
                batch_size=args.batch_size
            ):
                batch_num += 1
                logger.info(f"=== Batch {batch_num}: Processing {len(batch)} posts ===")
                
                for i, link in enumerate(batch, 1):
                    post_id = link.split("/post/")[-1].split("?")[0]
                    logger.info(f"[Batch {batch_num}, {i}/{len(batch)}] Crawling: {link}")
                    
                    post = crawler.parse_post(link)
                    
                    if post:
                        save_post(post)
                        known_ids.add(post.id)  # Update known_ids so we don't recrawl
                        new_posts += 1
                        logger.info(f"✓ Saved: {post.title[:40]}... ({len(post.comments)} comments)")
                    else:
                        failed_posts += 1
                        logger.warning(f"✗ Failed to parse: {link}")
                
                # Progress summary after each batch
                logger.info(f"Batch {batch_num} complete. Total saved: {new_posts}, Failed: {failed_posts}")
    
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 50)
        logger.info("Crawling interrupted by user (Ctrl+C)")
    
    # Summary
    logger.info("=" * 50)
    logger.info("Crawling Complete!")
    logger.info(f"New posts saved: {new_posts}")
    logger.info(f"Failed to parse: {failed_posts}")
    logger.info(f"Total posts in DB: {get_post_count()}")
    logger.info(f"Total comments in DB: {get_comment_count()}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()

