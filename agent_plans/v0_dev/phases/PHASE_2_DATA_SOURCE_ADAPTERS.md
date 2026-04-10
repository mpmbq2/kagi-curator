# Phase 2: Data Source Adapters Implementation Plan

## Goal
Implement concrete data source adapters for fetching news from Kagi API and RSS feeds, following the DataSourceAdapter ABC interface defined in Phase 1.

## Components to Implement

### 1. KagiAPIAdapter
**File**: `src/kagi_curator/sources/kagi_api_adapter.py`
**Purpose**: Fetch news using the Kagi API
**Key Features**:
- Authenticate with Kagi API using API key
- Implement fetch_news method to query Kagi's search/enrich/fastgpt endpoints
- Convert Kagi API response to standardized article format
- Handle rate limits and API errors appropriately
- Support configurable parameters (search type, date range, etc.)

### 2. RSSAdapter
**File**: `src/kagi_curator/sources/rss_adapter.py`
**Purpose**: Fetch news from RSS/XML feeds
**Key Features**:
- Parse RSS/Atom feeds using feedparser
- Implement fetch_news method to fetch and filter feed entries
- Convert feed entries to standardized article format
- Handle various RSS feed formats and extensions
- Support feed URL lists and fallback mechanisms
- Handle network errors and malformed feeds gracefully

## Implementation Approach

### KagiAPIAdapter Details
- Initialize with API key and optional configuration (search type, max results, etc.)
- Use kagiapi.KagiClient for API interactions
- Map KAPI response fields to Article dataclass:
  - title: from result title
  - summary: from description/snippet
  - url: from result URL
  - source: from publisher/site name
  - published_date: from timestamp or use current time
  - relevance_score: from Kagi's ranking if available
- Support different query types (search, enrich, fastgpt) based on configuration
- Implement proper error handling for API failures, rate limits, invalid responses

### RSSAdapter Details
- Initialize with list of feed URLs and optional configuration
- Use feedparser to parse feeds
- Map feed entry fields to Article dataclass:
  - title: from entry.title
  - summary: from entry.summary or entry.description
  - url: from entry.link
  - source: from entry.source.title or feed title
  - published_date: from entry.published_parsed or entry.updated_parsed
  - relevance_score: None (RSS doesn't typically provide relevance scores)
- Support feed validation and fallback URLs
- Implement date filtering for recent articles only
- Handle common RSS extensions (media, content, etc.)

## Common Patterns
Both adapters should:
1. Implement the fetch_news(query, limit) method from DataSourceAdapter ABC
2. Return List[Dict[str, Any]] that can be converted to Article objects
3. Raise appropriate exceptions (ConnectionError, ValueError) on failure
4. Include raw data in the returned dict when useful for debugging
5. Respect the limit parameter to avoid over-fetching
6. Handle datetime parsing and normalization
7. Include source identification in each article
8. Have proper logging for debugging and monitoring

## Dependencies
- kagiapi>=0.2.1 (for KagiAPIAdapter)
- feedparser>=6.0.12 (for RSSAdapter)
- Both are already listed in pyproject.toml

## Testing Strategy
- Unit tests with mocked API responses
- Integration tests with real feeds (for RSS)
- Error condition tests (network failures, invalid responses)
- Data conversion verification
- Respect for limits and filtering
- Date handling verification

## Deliverables
By the end of this phase, we will have:
1. KagiAPIAdapter implementing DataSourceAdapter
2. RSSAdapter implementing DataSourceAdapter
3. Both adapters properly handling errors and edge cases
4. Consistent article data format matching the Article dataclass expectations
5. Ready for use in NewsCurator implementations

## Next Steps
After completing Phase 2, proceed to:
- Phase 3: Implement EmailFormatter and test formatting
- Phase 4: Create specific NewsCurator implementations for target subsections
- Phase 5: Build NewsFactory and NewsOrchestrator implementations
- Phase 6: Add configuration loading and scheduling mechanisms