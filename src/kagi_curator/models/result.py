"""
Standardized container for news curation output.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime


@dataclass
class Article:
    """Standardized article representation."""
    title: str
    summary: str
    url: str
    source: str
    published_date: datetime.datetime
    relevance_score: Optional[float] = None
    raw_data: Optional[Dict[str, Any]] = None


@dataclass
class Result:
    """
    Container for curated news results from a NewsCurator.
    
    This object contains the curated news for a single subsection along with
    metadata about the curation process.
    """
    subsection_name: str
    articles: List[Article]
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate the Result after initialization."""
        if not isinstance(self.subsection_name, str):
            raise TypeError("subsection_name must be a string")
        if not isinstance(self.articles, list):
            raise TypeError("articles must be a list")
        if not all(isinstance(article, Article) for article in self.articles):
            raise TypeError("All items in articles must be Article instances")