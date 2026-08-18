# Architecture

## Medallion Design

### Bronze
Raw, append-oriented Delta tables preserving source structure and ingestion metadata.

Typical metadata:
- `_ingested_at`
- `_source_file`
- `_batch_id`

### Silver
Validated and conformed data with:
- type normalization
- null handling
- deduplication
- business-key validation
- standard naming
- reference-data enrichment

### Gold
Business-facing facts, dimensions, aggregates, and KPIs optimized for analytics.

## Pipeline Pattern

```text
Source -> Landing -> Bronze -> Data Quality -> Silver -> Business Logic -> Gold -> BI
```

## Design Principles

1. Raw data is never silently overwritten.
2. Pipelines should be restartable and idempotent.
3. Business logic belongs in curated layers, not ingestion code.
4. Data-quality failures should be observable and actionable.
5. Gold models should be designed around business questions.
