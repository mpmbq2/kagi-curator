from __future__ import annotations

import os
from pathlib import Path
from typing import Union

import yaml

from .models import AppConfig, DataSourceConfig, EmailConfig, SectionConfig, SubsectionConfig

_DEFAULT_CONFIG = Path(__file__).parent.parent.parent.parent / "config" / "default.yaml"


def load_config(path: Union[str, Path, None] = None) -> AppConfig:
    """Load pipeline configuration from a YAML file.

    Falls back to config/default.yaml when no path is provided.
    The Kagi API key is read from KAGI_API_KEY env var if not set in the file.
    SMTP password is read from SMTP_PASSWORD env var if not set in the file.
    """
    config_path = Path(path) if path else _DEFAULT_CONFIG

    with open(config_path) as f:
        data = yaml.safe_load(f) or {}

    api_key = (data.get("kagi") or {}).get("api_key") or os.environ.get("KAGI_API_KEY")

    sections = [_parse_section(s) for s in data.get("sections", [])]
    email_config = _parse_email(data.get("email")) if data.get("email") else None

    return AppConfig(sections=sections, kagi_api_key=api_key or None, email=email_config)


def _parse_email(data: dict) -> EmailConfig:
    password = data.get("smtp_password") or os.environ.get("SMTP_PASSWORD")
    return EmailConfig(
        smtp_host=data["smtp_host"],
        from_address=data["from_address"],
        to_addresses=data.get("to_addresses", []),
        smtp_port=int(data.get("smtp_port", 587)),
        smtp_username=data.get("smtp_username"),
        smtp_password=password or None,
        from_name=data.get("from_name", "Daily News Digest"),
        subject=data.get("subject", "Daily News Digest"),
        use_tls=bool(data.get("use_tls", True)),
    )


def _parse_section(data: dict) -> SectionConfig:
    return SectionConfig(
        name=data["name"],
        subsections=[_parse_subsection(s) for s in data.get("subsections", [])],
    )


def _parse_subsection(data: dict) -> SubsectionConfig:
    raw_sources = data.get("data_sources", [{"type": "kagi"}])
    data_sources = [DataSourceConfig(type=ds["type"], url=ds.get("url")) for ds in raw_sources]
    return SubsectionConfig(
        name=data["name"],
        queries=data.get("queries", []),
        article_limit=data.get("article_limit", 5),
        data_sources=data_sources,
    )
