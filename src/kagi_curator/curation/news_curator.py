"""
Abstract base class for curating news for a specific subsection.
"""
from abc import ABC, abstractmethod
from typing import List
import datetime

from ..models.result import Result, Article
from ..sources.data_source_adapter import DataSourceAdapter


class NewsCurator(ABC):
    """
    Abstract base class for curating news for a specific subsection.
    
    Each NewsCurator is responsible for fetching, filtering, deduplicating,
    and ranking news articles for one specific news subsection (e.g., 
    "Vermont Statewide", "Lamoille County", etc.).
    """
    
    def __init__(self, subsection_name: str, data_sources: List[DataSourceAdapter]):
        """
        Initialize the NewsCurator.
        
        Args:
            subsection_name: Identifier for this subsection (e.g., "Vermont Statewide")
            data_sources: List of data source adapters to fetch news from
        """
        self.subsection_name = subsection_name
        self.data_sources = data_sources
    
    @abstractmethod
    def _get_queries(self) -> List[str]:
        """
        Get the list of queries to use for fetching news.
        
        Returns:
            List of query strings to fetch news about this subsection
        """
        pass
    
    @abstractmethod
    def _get_article_limit(self) -> int:
        """
        Get the maximum number of articles to return for this subsection.
        
        Returns:
            Integer limit for number of articles
        """
        pass
    
    def curate(self) -> Result:
        """
        Execute the full curation process for this subsection.
        
        Returns:
            Result object containing curated articles and metadata
        """
        all_articles = []
        errors = []
        
        # Fetch news from each data source
        queries = self._get_queries()
        limit_per_source = self._get_article_limit()
        
        for data_source in self.data_sources:
            for query in queries:
                try:
                    articles = data_source.fetch_news(query, limit_per_source)
                    # Convert dict articles to Article objects
                    article_objects = [
                        Article(
                            title=article.get('title', ''),
                            summary=article.get('summary', ''),
                            url=article.get('url', ''),
                            source=article.get('source', 'Unknown'),
                            published_date=article.get('published_date', datetime.datetime.now()),
                            relevance_score=article.get('relevance_score'),
                            raw_data=article.get('raw_data')
                        )
                        for article in articles
                    ]
                    all_articles.extend(article_objects)
                except Exception as e:
                    errors.append(f"Failed to fetch from {data_source.__class__.__name__} with query '{query}': {str(e)}")
        
        # Deduplicate articles (by URL)
        seen_urls = set()
        deduplicated_articles = []
        for article in all_articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                deduplicated_articles.append(article)
        
        # Rank articles (by relevance score or date)
        ranked_articles = self._rank_articles(deduplicated_articles)
        
        # Limit to final count
        final_limit = self._get_article_limit()
        final_articles = ranked_articles[:final_limit]
        
        # Prepare metadata
        metadata = {
            "total_articles_found": len(all_articles),
            "articles_after_deduplication": len(deduplicated_articles),
            "data_sources_used": [ds.__class__.__name__ for ds in self.data_sources],
            "queries_used": queries,
            "curation_timestamp": datetime.datetime.now()
        }
        
        return Result(
            subsection_name=self.subsection_name,
            articles=final_articles,
            metadata=metadata,
            errors=errors
        )
    
    def _rank_articles(self, articles: List[Article]) -> List[Article]:
        """
        Rank articles by relevance/recency.
        
        Default implementation sorts by published_date descending.
        Override for more sophisticated ranking algorithms.
        
        Args:
            articles: List of articles to rank
            
        Returns:
            List of articles sorted by rank (highest first)
        """
        # Sort by published_date descending (most recent first)
        return sorted(articles, key=lambda x: x.published_date, reverse=True)