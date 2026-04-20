"""
Abstract base class for data source adapters that fetch news from various sources.
"""
from abc import ABC, abstractmethod
from typing import List

from ..models.result import Article


class DataSourceAdapter(ABC):
    """
    Abstract base class for data source adapters that fetch news from various sources.

    Each adapter implements a standardized interface for fetching news articles
    based on a query and desired count limit.
    """

    @abstractmethod
    def fetch_news(self, query: str, limit: int) -> List[Article]:
        """
        Fetch news articles from the data source.

        Args:
            query: Search query or topic to fetch news about
            limit: Maximum number of articles to return

        Returns:
            List of Article objects.

        Raises:
            ConnectionError: If unable to connect to the data source
            ValueError: If query parameters are invalid
        """
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fetch_news') and 
                callable(subclass.fetch_news))