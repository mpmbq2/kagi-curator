from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class DataSourceConfig:
    type: str  # "kagi" or "rss"
    url: str | None = None


@dataclass
class SubsectionConfig:
    name: str
    queries: List[str]
    article_limit: int
    data_sources: List[DataSourceConfig] = field(default_factory=lambda: [DataSourceConfig(type="kagi")])


@dataclass
class SectionConfig:
    name: str
    subsections: List[SubsectionConfig]


@dataclass
class AppConfig:
    sections: List[SectionConfig]
    kagi_api_key: str | None = None
