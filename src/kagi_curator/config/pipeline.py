from __future__ import annotations

from ..curation.standard_curator import StandardNewsCurator
from ..curation.standard_factory import StandardNewsFactory
from ..formatting.base_formatter import BaseFormatter
from ..orchestration.standard_orchestrator import StandardNewsOrchestrator
from ..sources.data_source_adapter import DataSourceAdapter
from ..sources.kagi_api_adapter import KagiAPIAdapter
from ..sources.rss_adapter import RSSAdapter
from .models import AppConfig, DataSourceConfig


def build_pipeline(config: AppConfig, formatter: BaseFormatter) -> StandardNewsOrchestrator:
    """Construct the full news pipeline from configuration."""
    factories = []
    for section_config in config.sections:
        curators = []
        for subsection_config in section_config.subsections:
            data_sources = [
                _build_data_source(ds, config.kagi_api_key)
                for ds in subsection_config.data_sources
            ]
            curators.append(
                StandardNewsCurator(
                    subsection_name=subsection_config.name,
                    queries=subsection_config.queries,
                    article_limit=subsection_config.article_limit,
                    data_sources=data_sources,
                )
            )
        factories.append(
            StandardNewsFactory(section_name=section_config.name, curators=curators)
        )
    return StandardNewsOrchestrator(factories=factories, formatter=formatter)


def _build_data_source(ds_config: DataSourceConfig, kagi_api_key: str | None) -> DataSourceAdapter:
    if ds_config.type == "kagi":
        return KagiAPIAdapter(api_key=kagi_api_key)
    if ds_config.type == "rss":
        if not ds_config.url:
            raise ValueError("RSS data source requires a 'url' field")
        return RSSAdapter(feed_url=ds_config.url)
    raise ValueError(f"Unknown data source type: {ds_config.type!r}")
