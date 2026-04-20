from __future__ import annotations

from typing import Any, Dict

from .base_formatter import BaseFormatter


class PlainTextFormatter(BaseFormatter):
    """Formats curated news data as readable plain text."""

    def format(self, data: Dict[str, Any]) -> str:
        lines: list[str] = []
        overall_meta = data.get("_metadata", {})
        generation_time = overall_meta.get("generation_timestamp", "")

        lines.append("=" * 60)
        lines.append("DAILY NEWS DIGEST")
        if generation_time:
            lines.append(f"Generated: {generation_time}")
        lines.append("=" * 60)
        lines.append("")

        for key, section in data.items():
            if key == "_metadata" or not isinstance(section, dict):
                continue

            section_name = section.get("_metadata", {}).get("section_name", key)
            lines.append(f"{'=' * 60}")
            lines.append(f"{section_name.upper()}")
            lines.append(f"{'=' * 60}")
            lines.append("")

            for subsection_key, subsection_data in section.items():
                if subsection_key == "_metadata" or not isinstance(subsection_data, dict):
                    continue

                lines.append(f"--- {subsection_key} ---")
                lines.append("")

                articles = subsection_data.get("articles", [])
                if not articles:
                    lines.append("  No articles found.")
                    lines.append("")
                    continue

                for i, article in enumerate(articles, 1):
                    title = article.get("title") or "No title"
                    source = article.get("source") or "Unknown"
                    url = article.get("url") or ""
                    summary = article.get("summary") or ""

                    lines.append(f"  {i}. {title}")
                    lines.append(f"     Source: {source}")
                    if summary:
                        truncated = summary[:200] + ("..." if len(summary) > 200 else "")
                        lines.append(f"     {truncated}")
                    if url:
                        lines.append(f"     {url}")
                    lines.append("")

        errors = overall_meta.get("errors", [])
        if errors:
            lines.append("--- Errors ---")
            for error in errors:
                lines.append(f"  ! {error}")
            lines.append("")

        return "\n".join(lines)
