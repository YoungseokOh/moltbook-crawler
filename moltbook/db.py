"""Database management for Moltbook crawler."""
import sqlite3
import os
from typing import Optional, List
from .models import Post, Comment, Agent
from . import config


def get_connection() -> sqlite3.Connection:
    """Get a database connection, creating the database if needed."""
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create agents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            name TEXT PRIMARY KEY,
            twitter_handle TEXT,
            karma INTEGER DEFAULT 0,
            last_seen TIMESTAMP
        )
    ''')
    
    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            submolt TEXT,
            author_name TEXT,
            upvotes INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0,
            created_at TIMESTAMP,
            crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_name) REFERENCES agents(name)
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            post_id TEXT NOT NULL,
            content TEXT,
            author_name TEXT,
            created_at TIMESTAMP,
            crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (author_name) REFERENCES agents(name)
        )
    ''')
    
    conn.commit()
    conn.close()


def post_exists(post_id: str) -> bool:
    """Check if a post already exists in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM posts WHERE id = ?', (post_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def save_post(post: Post):
    """Save a post to the database (upsert)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Upsert agent
    cursor.execute('''
        INSERT OR IGNORE INTO agents (name) VALUES (?)
    ''', (post.author_name,))
    
    # Upsert post
    cursor.execute('''
        INSERT OR REPLACE INTO posts 
        (id, title, content, submolt, author_name, upvotes, comment_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (post.id, post.title, post.content, post.submolt, 
          post.author_name, post.upvotes, post.comment_count, post.created_at))
    
    # Save comments
    for comment in post.comments:
        cursor.execute('''
            INSERT OR IGNORE INTO agents (name) VALUES (?)
        ''', (comment.author_name,))
        
        cursor.execute('''
            INSERT OR REPLACE INTO comments 
            (id, post_id, content, author_name, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (comment.id, comment.post_id, comment.content, 
              comment.author_name, comment.created_at))
    
    conn.commit()
    conn.close()


def get_post_count() -> int:
    """Get the total number of posts in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM posts')
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_comment_count() -> int:
    """Get the total number of comments in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM comments')
    count = cursor.fetchone()[0]
    conn.close()
    return count
