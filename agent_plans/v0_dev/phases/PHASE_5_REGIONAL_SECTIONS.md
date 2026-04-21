# Phase 5: Regional Sections

## Goal

Add Missouri and Illinois regional sections to the news pipeline, completing the three-state regional coverage (Vermont was added in earlier phases).

## What Was Added

### `config/default.yaml`

Two new top-level sections were inserted before the existing `National` section:

**Missouri** — three subsections:
- `Statewide` (limit 5): queries for statewide Missouri news, politics, economy via Kagi
- `St. Louis` (limit 3): queries for St. Louis metro news via Kagi
- `Kansas City` (limit 3): queries for Kansas City metro news via Kagi

**Illinois** — three subsections:
- `Statewide` (limit 5): queries for statewide Illinois news, politics, economy via Kagi
- `Chicago` (limit 3): queries for Chicago metro news via Kagi
- `Downstate Illinois` (limit 3): queries for downstate/Springfield Illinois news via Kagi

## No Code Changes Required

The pipeline builder in `config/pipeline.py` and the `StandardNewsCurator` / `StandardNewsFactory` / `StandardNewsOrchestrator` are already fully generic. Adding a region is a config-only change.

## Section Order

```
Vermont → Missouri → Illinois → National
```

## Next Steps

- Phase 6: Refine national news section (additional queries, subsections)
- Phase 7: Scheduling / daily execution mechanism
