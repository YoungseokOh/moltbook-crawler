#!/usr/bin/env python3
"""Main entry point for Moltbook crawler."""
import argparse
import logging
import sys

from moltbook import config
from moltbook.crawler import MoltbookCrawler
from moltbook.db import init_db, post_exists, save_post, get_post_count, get_comment_count


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
                        help='Maximum number of posts to crawl (default: all)')
    parser.add_argument('--incremental', action='store_true',
                        help='Skip posts already in the database')
    parser.add_argument('--no-headless', action='store_true',
                        help='Run browser in visible mode (for debugging)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 50)
    logger.info("Moltbook Crawler Starting")
    logger.info("=" * 50)
    
    # Initialize database
    init_db()
    logger.info(f"Database initialized at: {config.DB_PATH}")
    logger.info(f"Current posts in DB: {get_post_count()}")
    
    # Start crawling
    headless = not args.no_headless
    new_posts = 0
    skipped_posts = 0
    
    with MoltbookCrawler(headless=headless) as crawler:
        # Get post links from feed
        post_links = crawler.get_post_links_from_feed(max_posts=args.limit)
        total = len(post_links)
        
        for i, link in enumerate(post_links, 1):
            post_id = link.split("/post/")[-1].split("?")[0]
            
            # Check if already exists (incremental mode)
            if args.incremental and post_exists(post_id):
                logger.debug(f"Skipping existing post: {post_id}")
                skipped_posts += 1
                continue
            
            logger.info(f"[{i}/{total}] Crawling: {link}")
            post = crawler.parse_post(link)
            
            if post:
                save_post(post)
                new_posts += 1
                logger.info(f"Saved: {post.title[:40]}... ({len(post.comments)} comments)")
            else:
                logger.warning(f"Failed to parse: {link}")
    
    # Summary
    logger.info("=" * 50)
    logger.info("Crawling Complete!")
    logger.info(f"New posts saved: {new_posts}")
    logger.info(f"Posts skipped (already exists): {skipped_posts}")
    logger.info(f"Total posts in DB: {get_post_count()}")
    logger.info(f"Total comments in DB: {get_comment_count()}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
