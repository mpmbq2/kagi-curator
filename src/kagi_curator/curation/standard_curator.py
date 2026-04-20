from __future__ import annotations

from typing import List

from ..sources.data_source_adapter import DataSourceAdapter
from .news_curator import NewsCurator


class StandardNewsCurator(NewsCurator):
    """Concrete curator configured with explicit queries and article limit."""

    def __init__(
        self,
        subsection_name: str,
        queries: List[str],
        article_limit: int,
        data_sources: List[DataSourceAdapter],
    ) -> None:
        super().__init__(subsection_name, data_sources)
        self._queries = queries
        self._article_limit = article_limit

    def _get_queries(self) -> List[str]:
        return self._queries

    def _get_article_limit(self) -> int:
        return self._article_limit
