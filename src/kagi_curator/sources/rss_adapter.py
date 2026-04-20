import datetime
from typing import List, Dict, Any
from urllib.parse import urlparse

import feedparser

from .data_source_adapter import DataSourceAdapter


class RSSAdapter(DataSourceAdapter):
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_news(self, query: str, limit: int) -> List[Dict[str, Any]]:
        feed = feedparser.parse(self.feed_url)

        if feed.bozo and not feed.entries:
            exc = getattr(feed, "bozo_exception", None)
            raise ConnectionError(f"Failed to parse RSS feed '{self.feed_url}': {exc}")

        results = []
        for entry in feed.entries[:limit]:
            url = entry.get("link") or ""
            results.append({
                "title": entry.get("title") or "",
                "summary": entry.get("summary") or entry.get("description") or "",
                "url": url,
                "source": feed.feed.get("title") or self._extract_domain(self.feed_url),
                "published_date": self._parse_entry_date(entry),
                "raw_data": dict(entry),
            })
        return results

    def _parse_entry_date(self, entry) -> datetime.datetime:
        for field in ("published_parsed", "updated_parsed", "created_parsed"):
            time_struct = entry.get(field)
            if time_struct:
                try:
                    return datetime.datetime(*time_struct[:6])
                except Exception:
                    continue
        return datetime.datetime.now()

    def _extract_domain(self, url: str) -> str:
        if not url:
            return "Unknown"
        try:
            return urlparse(url).netloc
        except Exception:
            return "Unknown"
