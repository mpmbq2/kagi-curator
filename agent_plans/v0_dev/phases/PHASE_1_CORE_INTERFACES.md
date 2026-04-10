# Phase 1: Core Interfaces Implementation Plan

## Goal
Implement the foundational abstract base classes and data structures that define the architecture's contracts and enable extensibility.

## Components to Implement

### 1. BaseFormatter ABC
**File**: `src/kagi_curator/formatting/base_formatter.py`
**Purpose**: Define the interface for all formatters
**Key Methods**:
- `format(data: dict[str, Any]) -> str`: Abstract method for formatting news data

### 2. DataSourceAdapter ABC
**File**: `src/kagi_curator/sources/data_source_adapter.py`
**Purpose**: Define the interface for news data fetchers
**Key Methods**:
- `fetch_news(query: str, limit: int) -> List[Dict[str, Any]]`: Fetch news from a source

### 3. Result Dataclass
**File**: `src/kagi_curator/models/result.py`
**Purpose**: Standardized container for curation output
**Structure**:
- `subsection_name`: str
- `articles`: List[Article]
- `metadata`: Dict[str, Any]
- `errors`: List[str]

### 4. NewsCurator ABC
**File**: `src/kagi_curator/curation/news_curator.py`
**Purpose**: Base class for subsection-level news curation
**Key Methods**:
- `curate() -> Result`: Main curation workflow
- `_get_queries() -> List[str]`: Abstract - get search queries
- `_get_article_limit() -> int`: Abstract - get article limit
- `_rank_articles(articles: List[Article]) -> List[Article]`: Default ranking implementation

### 5. NewsFactory ABC
**File**: `src/kagi_curator/curation/news_factory.py`
**Purpose**: Base class for grouping curators into sections
**Key Methods**:
- `generate_section() -> Dict[str, Any]`: Execute all subsection curators
- `_organize_results(results: List[Result]) -> Dict[str, Any]`: Abstract - organize subsection results

### 6. NewsOrchestrator ABC
**File**: `src/kagi_curator/orchestration/news_orchestrator.py`
**Purpose**: Base class for coordinating the full workflow
**Key Methods**:
- `generate_newsletter() -> str`: Main entry point
- `_determine_execution_order() -> List[NewsFactory]`: Abstract - factory order
- `_aggregate_results(factory_results: List[Dict[str, Any]]) -> Dict[str, Any]`: Abstract - combine results

## Implementation Approach

### 1. Create Directory Structure
```
src/
└── kagi_curator/
    ├── formatting/
    │   └── base_formatter.py
    ├── sources/
    │   └── data_source_adapter.py
    ├── models/
    │   └── result.py
    ├── curation/
    │   ├── news_curator.py
    │   └── news_factory.py
    └── orchestration/
        └── news_orchestrator.py
```

### 2. Interface Design Principles
- Use Python's `abc` module for formal abstract base classes
- Include `__subclasshook__` methods for Protocol-like flexibility
- Define clear docstrings for all abstract methods
- Include type hints for better IDE support and clarity
- Implement validation in `__post_init__` for dataclasses where appropriate
- Provide sensible default implementations where possible (e.g., basic ranking)

### 3. Error Handling Strategy
- DataSourceAdapter implementations should raise specific exceptions (ConnectionError, ValueError)
- NewsCurator.curate() catches exceptions from data sources and records them in Result.errors
- NewsFactory and NewsOrchestrator collect errors from their children and include them in metadata
- Curation continues despite individual failures, returning partial results with error information

### 4. Dependencies
- Python 3.12+ (for dataclass features)
- Standard library only (no external dependencies for core interfaces)
- Future implementations will depend on:
  - feedparser>=6.0.12 (for RSS)
  - kagiapi>=0.2.1 (for Kagi API)

### 5. Testing Strategy
- Create abstract base class tests using concrete test implementations
- Test error handling paths
- Verify metadata collection
- Test that subclasses must implement abstract methods
- Validate data structures and type safety

## Deliverables
By the end of this phase, we will have:
1. All six core interface modules implemented
2. Proper directory structure in place
3. Docstrings and type hints complete
4. Basic error handling patterns established
5. Foundation ready for concrete implementations in Phase 2

## Next Steps
After completing Phase 1, proceed to:
- Phase 2: Implement concrete data source adapters (KagiAPIAdapter, RSSAdapter)
- Phase 3: Implement EmailFormatter and test formatting
- Phase 4: Create specific NewsCurator implementations for target subsections
- Phase 5: Build NewsFactory and NewsOrchestrator implementations
- Phase 6: Add configuration loading and scheduling mechanisms