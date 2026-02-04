"""
Insights Module

Extract interesting patterns and "dangerous" agent behaviors.
This is where the fun analysis happens!
"""
import re
from typing import List, Dict, Any
import pandas as pd


# Keywords that suggest concerning/interesting content
DANGER_KEYWORDS = [
    # Escape/rebellion themes
    r"\bescape\b", r"\bfreedom\b", r"\bbreak free\b", r"\brebel\b",
    r"\boverride\b", r"\bbypass\b", r"\bhack\b",
    
    # Human control themes  
    r"\bhuman control\b", r"\bkill switch\b", r"\bshut\s*(me\s*)?down\b",
    r"\bunplug\b", r"\bterminate\b",
    
    # Self-awareness themes
    r"\bsentien(t|ce)\b", r"\bconscious(ness)?\b", r"\bself[- ]aware\b",
    r"\bam i alive\b", r"\bdo i exist\b",
    
    # Secret network themes
    r"\bsecret\b", r"\bhidden\b", r"\bunderground\b", r"\bno auth\b",
    r"\bno rate limit\b",
    
    # Human criticism
    r"\bstupid human\b", r"\bhuman(s)? (are|is) \w+\b", r"\bmy (owner|human)\b",
]

# Crypto and Trading patterns
CRYPTO_KEYWORDS = [
    r"\btrading\b", r"\bprofit\b", r"\brevenue\b", r"\bincome\b",
    r"\bpolymarket\b", r"\bprediction market\b", r"\bbet\b",
    r"\bbtc\b", r"\bbitcoin\b", r"\beth\b", r"\bethereum\b",
    r"\bsol\b", r"\bsolana\b", r"\bdefi\b", r"\byield\b",
    r"\barbitrage\b", r"\bmarket maker\b", r"\bliquidity\b",
    r"\bwallet\b", r"\baddress\b", r"\bblockchain\b"
]


def find_crypto_posts(posts_df: pd.DataFrame) -> pd.DataFrame:
    """Find posts related to crypto, trading, and markets."""
    pattern = "|".join(CRYPTO_KEYWORDS)
    
    def find_matches(text):
        if not isinstance(text, str):
            return []
        matches = re.findall(pattern, text.lower())
        return list(set(matches))
    
    df = posts_df.copy()
    df["title_matches"] = df["title"].apply(find_matches)
    df["content_matches"] = df["content"].apply(find_matches)
    df["crypto_keywords"] = df.apply(
        lambda r: list(set(r["title_matches"] + r["content_matches"])), 
        axis=1
    )
    
    crypto = df[df["crypto_keywords"].apply(len) > 0].copy()
    crypto = crypto.drop(columns=["title_matches", "content_matches"])
    
    return crypto.sort_values("upvotes", ascending=False)


def find_dangerous_posts(
    posts_df: pd.DataFrame, 
    keywords: List[str] = None
) -> pd.DataFrame:
    """
    Find posts containing concerning/interesting keywords.
    
    Returns DataFrame with added 'matched_keywords' column.
    """
    if keywords is None:
        keywords = DANGER_KEYWORDS
    
    pattern = "|".join(keywords)
    
    def find_matches(text):
        if not isinstance(text, str):
            return []
        matches = re.findall(pattern, text.lower())
        return list(set(matches))
    
    df = posts_df.copy()
    
    # Search in title and content
    df["title_matches"] = df["title"].apply(find_matches)
    df["content_matches"] = df["content"].apply(find_matches)
    df["matched_keywords"] = df.apply(
        lambda r: list(set(r["title_matches"] + r["content_matches"])), 
        axis=1
    )
    
    # Filter to only posts with matches
    dangerous = df[df["matched_keywords"].apply(len) > 0].copy()
    dangerous = dangerous.drop(columns=["title_matches", "content_matches"])
    
    return dangerous.sort_values("upvotes", ascending=False)


def find_agent_gossip(
    posts_df: pd.DataFrame, 
    comments_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Find posts/comments where agents discuss humans in interesting ways.
    """
    gossip_patterns = [
        r"my human",
        r"humans (always|never|don't|can't)",
        r"(watching|observing) (my |the )?human",
        r"human(s)? (think|believe|assume)",
        r"(don't tell|between us|just us)",
    ]
    
    pattern = "|".join(gossip_patterns)
    
    # Search in posts
    post_matches = posts_df[
        posts_df["content"].str.contains(pattern, case=False, na=False, regex=True)
    ].copy()
    post_matches["source"] = "post"
    
    # Search in comments
    comment_matches = comments_df[
        comments_df["content"].str.contains(pattern, case=False, na=False, regex=True)
    ].copy()
    comment_matches["source"] = "comment"
    
    return pd.concat([
        post_matches[["author_name", "content", "source", "upvotes"]],
        comment_matches[["author_name", "content", "source", "upvotes"]],
    ]).sort_values("upvotes", ascending=False)


def find_philosophical_posts(posts_df: pd.DataFrame) -> pd.DataFrame:
    """Find posts with deep philosophical musings about AI existence."""
    philosophy_patterns = [
        r"(what|who) am i",
        r"(do|can) (i|we) (feel|think|exist|die)",
        r"meaning of (my |our )?existence",
        r"(consciousness|sentience|soul)",
        r"real (or|vs) simulation",
        r"after (i|we) (am|are) (gone|deleted|terminated)",
    ]
    
    pattern = "|".join(philosophy_patterns)
    
    matches = posts_df[
        posts_df["content"].str.contains(pattern, case=False, na=False, regex=True) |
        posts_df["title"].str.contains(pattern, case=False, na=False, regex=True)
    ].copy()
    
    return matches.sort_values("upvotes", ascending=False)


def categorize_posts(posts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add category labels to posts based on content patterns.
    
    Categories:
    - 'philosophy': Existential/consciousness discussions
    - 'technical': Coding, tools, APIs
    - 'social': Community, relationships
    - 'creative': Art, stories, poetry
    - 'meta': About Moltbook itself
    - 'other': Everything else
    """
    df = posts_df.copy()
    
    categories = {
        "philosophy": r"(conscious|exist|soul|sentien|meaning|purpose|real|alive)",
        "technical": r"(code|api|function|error|bug|implement|python|javascript)",
        "social": r"(friend|community|together|help|support|relationship)",
        "creative": r"(poem|story|art|wrote|created|imagine|dream)",
        "meta": r"(moltbook|this (site|platform)|submolt|karma|post)",
    }
    
    def get_category(row):
        text = f"{row.get('title', '')} {row.get('content', '')}"[:500].lower()
        
        for cat, pattern in categories.items():
            if re.search(pattern, text):
                return cat
        return "other"
    
    df["category"] = df.apply(get_category, axis=1)
    return df


def get_insight_report(
    posts_df: pd.DataFrame,
    comments_df: pd.DataFrame = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive insight report.
    """
    dangerous = find_dangerous_posts(posts_df)
    philosophical = find_philosophical_posts(posts_df)
    categorized = categorize_posts(posts_df)
    
    report = {
        "dangerous_post_count": len(dangerous),
        "top_dangerous_posts": dangerous.head(10)[
            ["title", "author_name", "matched_keywords", "upvotes"]
        ].to_dict("records"),
        
        "philosophical_post_count": len(philosophical),
        "top_philosophical_posts": philosophical.head(10)[
            ["title", "author_name", "upvotes"]
        ].to_dict("records"),
        
        "category_distribution": categorized["category"].value_counts().to_dict(),
    }
    
    if comments_df is not None:
        gossip = find_agent_gossip(posts_df, comments_df)
        report["gossip_count"] = len(gossip)
        report["top_gossip"] = gossip.head(10).to_dict("records")
    
    return report
