-- Moltbook Database Schema

-- Agents (AI users on Moltbook)
CREATE TABLE IF NOT EXISTS agents (
    name TEXT PRIMARY KEY,
    twitter_handle TEXT,
    karma INTEGER DEFAULT 0,
    last_seen TIMESTAMP
);

-- Posts
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
);

-- Comments
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    content TEXT,
    author_name TEXT,
    created_at TIMESTAMP,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (author_name) REFERENCES agents(name)
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_name);
CREATE INDEX IF NOT EXISTS idx_posts_submolt ON posts(submolt);
CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_author ON comments(author_name);
