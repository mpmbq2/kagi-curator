"""
Abstract base class for data source adapters that fetch news from various sources.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import datetime


class DataSourceAdapter(ABC):
    """
    Abstract base class for data source adapters that fetch news from various sources.
    
    Each adapter implements a standardized interface for fetching news articles
    based on a query and desired count limit.
    """
    
    @abstractmethod
    def fetch_news(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """
        Fetch news articles from the data source.
        
        Args:
            query: Search query or topic to fetch news about
            limit: Maximum number of articles to return
            
        Returns:
            List of article dictionaries with standardized fields:
            - title: Article headline
            - summary: Brief description or snippet
            - url: Direct link to the article
            - source: Publication or source name
            - published_date: datetime object of publication
            - raw_data: Optional original source data for debugging
            
        Raises:
            ConnectionError: If unable to connect to the data source
            ValueError: If query parameters are invalid
        """
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fetch_news') and 
                callable(subclass.fetch_news))