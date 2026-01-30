"""Data models for Moltbook crawler."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Agent:
    """Represents an AI agent on Moltbook."""
    name: str
    twitter_handle: Optional[str] = None
    karma: int = 0
    last_seen: Optional[datetime] = None


@dataclass
class Comment:
    """Represents a comment on a post."""
    id: str
    post_id: str
    content: str
    author_name: str
    created_at: Optional[datetime] = None


@dataclass
class Post:
    """Represents a post on Moltbook."""
    id: str
    title: str
    content: str
    submolt: str
    author_name: str
    upvotes: int = 0
    comment_count: int = 0
    created_at: Optional[datetime] = None
    comments: List[Comment] = field(default_factory=list)
