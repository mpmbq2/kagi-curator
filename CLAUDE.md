# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync                  # Install dependencies
uv run kagi-curator      # Run the CLI entry point
uv run marimo edit notebooks/general-news.py  # Open a Marimo notebook
```

No test framework, linter, or formatter is configured yet. When adding them, prefer `ruff` for linting/formatting and `pytest` for tests (standard for uv-managed Python projects).

## Architecture

The app is a modular news curation pipeline that fetches, deduplicates, ranks, and formats daily news into a deliverable (email, etc.). The pipeline has four layers:

```
NewsOrchestrator
  └── NewsFactory (one per region/category, e.g. "Vermont", "National")
        └── NewsCurator (one per subsection, e.g. "Statewide", "Lamoille County")
              └── DataSourceAdapter[] (KagiAPIAdapter, RSSAdapter)
```

**Layer responsibilities:**

- **`NewsOrchestrator`** (`orchestration/news_orchestrator.py`) — Calls `generate_section()` on each factory in order, aggregates results, passes them to a `BaseFormatter`, returns the final string. Entry point: `generate_newsletter()`.
- **`NewsFactory`** (`curation/news_factory.py`) — Runs all its `NewsCurator` objects, collects `Result` objects, and calls the abstract `_organize_results()` to structure them into a section dict. Adds `_metadata` key automatically.
- **`NewsCurator`** (`curation/news_curator.py`) — Calls each adapter for each query, converts raw dicts to `Article` objects, deduplicates by URL, ranks by `published_date` (override `_rank_articles()` for custom logic), trims to the limit, returns a `Result`. This is where article count limits are enforced.
- **`DataSourceAdapter`** (`sources/data_source_adapter.py`) — Single method: `fetch_news(query: str, limit: int) -> List[Dict[str, Any]]`. Dict keys must include `title`, `summary`, `url`, `source`, `published_date`. Two planned implementations: `KagiAPIAdapter` (uses `kagiapi.KagiClient`) and `RSSAdapter` (uses `feedparser`).
- **`BaseFormatter`** (`formatting/base_formatter.py`) — Abstract `format(data: Dict[str, Any]) -> str`. Planned: `EmailFormatter` (HTML), `PlainTextFormatter`, `JSONFormatter`.
- **`Result` / `Article`** (`models/result.py`) — Dataclasses. `Result` holds `subsection_name`, `articles: List[Article]`, `metadata`, and `errors`. `Article` holds `title`, `summary`, `url`, `source`, `published_date`, and optional `relevance_score`.

**Error handling pattern:** Errors at each layer are caught, appended to a list, and propagated upward via the `errors` field in `Result` and `_metadata["errors"]` in factory/orchestrator dicts. Curation continues on partial failures.

## Current State

Phase 1 (all ABCs + models) is complete. Phase 2 (concrete `KagiAPIAdapter` and `RSSAdapter`) is the immediate next step. `main()` in `__init__.py` is a placeholder. The `notebooks/general-news.py` Marimo notebook explores the `kagiapi` client directly and is a good reference for how to use it before implementing `KagiAPIAdapter`.

## Extension Patterns

- **New section/region:** Subclass `NewsFactory`, implement `_organize_results()`, add to orchestrator's factory list.
- **New subsection:** Subclass `NewsCurator`, implement `_get_queries()` and `_get_article_limit()`, add to a factory.
- **New data source:** Subclass `DataSourceAdapter`, implement `fetch_news()`.
- **New output format:** Subclass `BaseFormatter`, implement `format()`, pass to orchestrator.
