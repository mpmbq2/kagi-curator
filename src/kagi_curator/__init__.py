from __future__ import annotations

import os
import sys

from .config.loader import load_config
from .config.pipeline import build_pipeline
from .formatting.plain_text_formatter import PlainTextFormatter


def main() -> None:
    config_path = os.environ.get("KAGI_CURATOR_CONFIG")
    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        print(f"Error: configuration file not found — {e}", file=sys.stderr)
        sys.exit(1)

    formatter = PlainTextFormatter()
    orchestrator = build_pipeline(config, formatter)
    print(orchestrator.generate_newsletter())
