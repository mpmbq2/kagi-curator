# News Curator App - Initial Architecture Overview

## High-Level Architecture

This document outlines the proposed architecture for a modular, extensible news curator application that delivers daily news updates via email (with flexibility for other output formats in the future).

### Core Components

#### 1. NewsOrchestrator (Top Level)
**Purpose**: Coordinates the entire news curation process and generates final output payload

**Responsibilities**:
- Initialize with a list of NewsFactory instances and a Formatter
- Execute each factory in sequence (national first, then regional)
- Aggregate results from all factories
- Format final output using the provided Formatter instance
- Handle overall workflow and error handling

#### 2. NewsFactory (Regional/Section Grouping)
**Purpose**: Groups related NewsCurator objects for a specific news category/region

**Responsibilities**:
- Manage a collection of NewsCurator objects
- Execute all curators and collect their results
- Structure/organize results according to subsection hierarchy
- Return structured data representing the factory's section

#### 3. NewsCurator (Individual Subsection Handler)
**Purpose**: Handles news collection and curation for one specific subsection

**Responsibilities**:
- Fetch news from configured data sources (Kagi API, RSS feeds)
- Filter, deduplicate, and rank news items
- Limit to configured number of top stories (3-5 for national, 2 for subsections)
- Return structured Result object with curated news

#### 4. Result Object
**Purpose**: Standardized container for news curation output

**Structure**:
- `subsection_name`: Identifier for this subsection
- `articles`: List of article dictionaries with:
  - `title`: Article headline
  - `summary`: Brief description
  - `url`: Source link
  - `source`: Publication name
  - `published_date`: Timestamp
  - `relevance_score`: Optional ranking metric
- `metadata`: Additional info (total found, processing time, etc.)

#### 5. Data Source Adapters
- **KagiAdapter**: Handles Kagi API interactions
- **RSSAdapter**: Parses RSS/XML feeds
- **Common interface**: Both implement `fetch_news(query, limit)` returning raw articles

#### 6. Formatter Hierarchy
- **BaseFormatter (Abstract Base Class)**:
  - Defines interface for formatting structured data
  - Abstract method: `format(data) -> str`
  
- **EmailFormatter (extends BaseFormatter)**:
  - Converts structured data to HTML email format
  - Features: Template-based HTML generation, section headers, email-specific styling
  
- **Future Formatters** (examples):
  - **WebFormatter**: Generates HTML for web display
  - **PlainTextFormatter**: Creates plain text output
  - **JSONFormatter**: Outputs structured JSON
  - **MarkdownFormatter**: Generates Markdown format

### Extension Points

#### Adding New Sections/Regions
1. Create new NewsFactory subclass
2. Instantiate with appropriate NewsCurator objects
3. Add to NewsOrchestrator's factory list

#### Adding New Subsections
1. Create NewsCurator for the specific subsection
2. Configure data sources and queries
3. Add to relevant NewsFactory

#### Adding New Data Sources
1. Implement new adapter with standard interface
2. Reference in NewsCurator configuration

#### Adding New Output Formats
1. Create new Formatter subclass extending BaseFormatter
2. Pass formatter instance to NewsOrchestrator initialization

### Data Flow

1. NewsOrchestrator.initialize(factories, formatter)
2. For each factory in factories:
   - Factory.execute():
     - For each curator in curators:
       - Curator.fetch_news():
         - Query each configured data source
         - Combine and deduplicate results
         - Rank by relevance/recency
         - Return top N as Result
     - Factory.organize_results(results)
   - Orchestrator.aggregate_factory_results()
3. Orchestrator.format_output(aggregated_data, formatter)
4. Return formatted output string

### Configuration Approach

- External configuration (YAML/JSON) for:
  - Section/subsection definitions
  - Data source URLs/queries per subsection
  - Number of articles per subsection
  - Email template paths
- Factory and curator instantiation from config
- Easy modification without code changes

### Key Benefits

1. **Modularity**: Each component has single responsibility
2. **Extensibility**: New sections, sources, or formats can be added independently
3. **Testability**: Each class can be unit tested in isolation
4. **Maintainability**: Changes to one subsection don't affect others
5. **Flexibility**: Different data sources can be mixed and matched per subsection
6. **Output Format Agnostic**: Core logic independent of presentation format

### Implementation Roadmap

1. **Phase 1**: Implement core interfaces (BaseFormatter, Result, basic adapters)
2. **Phase 2**: Implement NewsCurator and NewsFactory classes
3. **Phase 3**: Implement NewsOrchestrator with configuration loading
4. **Phase 4**: Implement EmailFormatter and initial email delivery
5. **Phase 5**: Add regional sections (Vermont, Missouri, Illinois) with subsections
6. **Phase 6**: Add national news section
7. **Phase 7**: Implement scheduling/daily execution mechanism