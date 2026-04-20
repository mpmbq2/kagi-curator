from __future__ import annotations

from typing import Any, Dict, List

from ..curation.news_factory import NewsFactory
from .news_orchestrator import NewsOrchestrator


class StandardNewsOrchestrator(NewsOrchestrator):
    """Concrete orchestrator that runs factories in the order they were provided."""

    def _determine_execution_order(self) -> List[NewsFactory]:
        return self.factories

    def _aggregate_results(self, factory_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        aggregated: Dict[str, Any] = {}
        for result in factory_results:
            section_name = result.get("_metadata", {}).get("section_name", "Unknown")
            aggregated[section_name] = result
        return aggregated
