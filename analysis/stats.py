"""
Statistics Module

Generate summary statistics from Moltbook data.
"""
from typing import Dict, Any
import pandas as pd


def get_summary_stats(
    posts_df: pd.DataFrame,
    comments_df: pd.DataFrame = None,
    agents_df: pd.DataFrame = None
) -> Dict[str, Any]:
    """
    Generate summary statistics.
    
    Returns dict with:
    - total_posts, total_comments, total_agents
    - top_authors, top_submolts
    - activity_by_date
    """
    stats = {
        "total_posts": len(posts_df),
        "total_comments": len(comments_df) if comments_df is not None else 0,
        "total_agents": len(agents_df) if agents_df is not None else 0,
    }
    
    # Top authors by post count
    if "author_name" in posts_df.columns:
        stats["top_authors"] = (
            posts_df["author_name"]
            .value_counts()
            .head(20)
            .to_dict()
        )
    
    # Top submolts by post count
    if "submolt_name" in posts_df.columns:
        stats["top_submolts"] = (
            posts_df["submolt_name"]
            .value_counts()
            .head(20)
            .to_dict()
        )
    
    # Posts by date
    if "created_at" in posts_df.columns:
        posts_df = posts_df.copy()
        posts_df["date"] = posts_df["created_at"].dt.date
        stats["posts_by_date"] = (
            posts_df.groupby("date")
            .size()
            .to_dict()
        )
    
    # Average engagement
    if "upvotes" in posts_df.columns:
        stats["avg_upvotes"] = posts_df["upvotes"].mean()
        stats["avg_downvotes"] = posts_df["downvotes"].mean()
        stats["avg_comments"] = posts_df["comment_count"].mean()
    
    return stats


def get_engagement_leaderboard(posts_df: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
    """Get top posts by engagement (upvotes + comment_count)."""
    df = posts_df.copy()
    df["engagement"] = df["upvotes"] + df["comment_count"] * 2
    return df.nlargest(top_n, "engagement")[
        ["title", "author_name", "upvotes", "comment_count", "engagement"]
    ]


def get_author_stats(posts_df: pd.DataFrame, agents_df: pd.DataFrame = None) -> pd.DataFrame:
    """Get per-author statistics."""
    author_stats = posts_df.groupby("author_name").agg({
        "id": "count",
        "upvotes": "sum",
        "downvotes": "sum",
        "comment_count": "sum",
    }).rename(columns={"id": "post_count"})
    
    author_stats["avg_upvotes"] = author_stats["upvotes"] / author_stats["post_count"]
    
    if agents_df is not None and "name" in agents_df.columns:
        author_stats = author_stats.join(
            agents_df.set_index("name")[["karma", "follower_count"]],
            how="left"
        )
    
    return author_stats.sort_values("post_count", ascending=False)
