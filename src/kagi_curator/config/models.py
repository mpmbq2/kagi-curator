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
class EmailConfig:
    smtp_host: str
    from_address: str
    to_addresses: List[str]
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None  # prefer SMTP_PASSWORD env var
    from_name: str = "Daily News Digest"
    subject: str = "Daily News Digest"
    use_tls: bool = True


@dataclass
class AppConfig:
    sections: List[SectionConfig]
    kagi_api_key: str | None = None
    email: EmailConfig | None = None
