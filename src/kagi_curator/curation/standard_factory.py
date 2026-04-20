from __future__ import annotations

from typing import Any, Dict, List

from ..models.result import Result
from .news_factory import NewsFactory


class StandardNewsFactory(NewsFactory):
    """Concrete factory that organizes subsection results into a keyed dict."""

    def _organize_results(self, results: List[Result]) -> Dict[str, Any]:
        organized: Dict[str, Any] = {}
        for result in results:
            organized[result.subsection_name] = {
                "articles": [
                    {
                        "title": a.title,
                        "summary": a.summary,
                        "url": a.url,
                        "source": a.source,
                        "published_date": a.published_date.isoformat(),
                    }
                    for a in result.articles
                ],
                "metadata": {
                    k: str(v) if hasattr(v, "isoformat") else v
                    for k, v in result.metadata.items()
                },
                "errors": result.errors,
            }
        return organized
