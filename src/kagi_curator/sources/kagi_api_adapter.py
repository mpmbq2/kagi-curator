import datetime
from typing import List
from urllib.parse import urlparse

from kagiapi import KagiClient

from ..models.result import Article
from .data_source_adapter import DataSourceAdapter


class KagiAPIAdapter(DataSourceAdapter):
    def __init__(self, api_key: str | None = None):
        self.client = KagiClient(api_key=api_key)

    def fetch_news(self, query: str, limit: int) -> List[Article]:
        response = self.client.enrich(query)

        if errors := response.get("error"):
            raise ConnectionError(f"Kagi API error: {errors}")

        items = response.get("data") or []
        results = []
        for item in items[:limit]:
            url = item.get("url") or ""
            results.append(Article(
                title=item.get("title") or "",
                summary=item.get("snippet") or "",
                url=url,
                source=self._extract_domain(url),
                published_date=self._parse_date(item.get("published")),
                raw_data=item,
            ))
        return results

    def _parse_date(self, value) -> datetime.datetime:
        if not value:
            return datetime.datetime.now()
        if isinstance(value, datetime.datetime):
            return value.replace(tzinfo=None)
        try:
            dt = datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            return dt.replace(tzinfo=None)
        except ValueError:
            return datetime.datetime.now()

    def _extract_domain(self, url: str) -> str:
        if not url:
            return "Unknown"
        try:
            return urlparse(url).netloc
        except Exception:
            return "Unknown"
