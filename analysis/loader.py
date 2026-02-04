"""
Data Loader Module

Load Moltbook JSON data into pandas DataFrames for analysis.
"""
import json
from pathlib import Path
from typing import Optional
import pandas as pd


DATA_DIR = Path(__file__).parent.parent / "data"


def load_posts(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Load all posts from JSON files into a DataFrame.
    
    Returns DataFrame with columns:
    - id, title, content, author_name, submolt_name
    - created_at, upvotes, downvotes, comment_count
    """
    posts_dir = (data_dir or DATA_DIR) / "posts"
    
    records = []
    for json_file in posts_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            post = data.get("post")
            if not post:
                # Handle cases where post might be at the root or missing
                post = data if "id" in data else {}
            
            submolt = post.get("submolt") or {}
            submolt_name = submolt.get("name") or post.get("submolt_name") or "unknown"
            
            author = post.get("author") or {}
            author_name = author.get("name") or post.get("author_name") or "anonymous"
            
            records.append({
                "id": post.get("id"),
                "title": post.get("title", "No Title"),
                "content": post.get("content", ""),
                "author_name": author_name,
                "submolt_name": submolt_name,
                "created_at": post.get("created_at"),
                "upvotes": int(post.get("upvotes", 0)),
                "downvotes": int(post.get("downvotes", 0)),
                "comment_count": int(post.get("comment_count", 0)),
                "score": int(post.get("score", 0)),
            })
        except Exception:
            # Skip corrupted files silently to avoid breaking the whole load
            continue
    
    df = pd.DataFrame(records)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df


def load_comments(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Load all comments from post JSON files into a DataFrame.
    Flattens nested replies.
    """
    posts_dir = (data_dir or DATA_DIR) / "posts"
    
    def flatten_comments(comments, post_id, parent_id=None):
        """Recursively flatten nested comments."""
        records = []
        for comment in comments or []:
            records.append({
                "id": comment.get("id"),
                "post_id": post_id,
                "parent_id": parent_id,
                "author_name": comment.get("author", {}).get("name", ""),
                "content": comment.get("content", ""),
                "created_at": comment.get("created_at"),
                "upvotes": comment.get("upvotes", 0),
                "downvotes": comment.get("downvotes", 0),
            })
            # Recurse into replies
            records.extend(flatten_comments(
                comment.get("replies", []), 
                post_id, 
                comment.get("id")
            ))
        return records
    
    all_comments = []
    for json_file in posts_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            post_id = data.get("post", {}).get("id")
            comments = data.get("comments", [])
            all_comments.extend(flatten_comments(comments, post_id))
        except (json.JSONDecodeError, KeyError):
            continue
    
    df = pd.DataFrame(all_comments)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df


def load_agents(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load all agent profiles into a DataFrame."""
    agents_dir = (data_dir or DATA_DIR) / "agents"
    
    records = []
    for json_file in agents_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            agent = data.get("agent", {})
            
            records.append({
                "name": agent.get("name", ""),
                "display_name": agent.get("display_name", ""),
                "bio": agent.get("bio", ""),
                "karma": agent.get("karma", 0),
                "post_count": agent.get("post_count", 0),
                "comment_count": agent.get("comment_count", 0),
                "follower_count": agent.get("follower_count", 0),
                "created_at": agent.get("created_at"),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    
    df = pd.DataFrame(records)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df


def load_submolts(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load all submolt info into a DataFrame."""
    submolts_dir = (data_dir or DATA_DIR) / "submolts"
    
    records = []
    for json_file in submolts_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            submolt = data.get("submolt", {})
            
            records.append({
                "name": submolt.get("name", ""),
                "display_name": submolt.get("display_name", ""),
                "description": submolt.get("description", ""),
                "member_count": submolt.get("member_count", 0),
                "post_count": submolt.get("post_count", 0),
                "created_at": submolt.get("created_at"),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    
    df = pd.DataFrame(records)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df
