# Incremental Processing and SCD Type 2

## Incremental processing

The platform uses an ingestion watermark to avoid reprocessing the full Silver dataset on every run.

1. Read the last committed watermark from the operational watermark table.
2. Select records with `ingested_at > last_watermark`.
3. Upsert atomic facts using the business key `meter_id + reading_timestamp`.
4. Identify affected `date_key + region` partitions.
5. Recompute only those KPI aggregates.
6. Merge KPI updates into Gold.
7. Advance the watermark only after successful downstream writes.

The watermark must be advanced as part of the same orchestration transaction boundary as the Gold writes; otherwise a failed run could skip data.

## SCD Type 2

`dim_meter` tracks historical region changes.

For an incoming change:

```text
Current version
MTR001 | north | current
          |
          | region changes
          v
Expired version
MTR001 | north | effective_to = D-1 | not current

New version
MTR001 | west  | effective_from = D  | current
```

### Guarantees

- At most one current version per `meter_id`
- Historical versions are retained
- Changed attributes create a new version
- Unchanged attributes do not create new versions
- Surrogate keys distinguish historical versions

## Failure semantics

The pipeline is designed so that the watermark is advanced only after the Gold merge succeeds. A retry therefore reads the same source window and the Delta MERGE remains idempotent.

## Production evolution

- Replace notebook orchestration with a Databricks Workflow/Asset Bundle job
- Store watermarks in a governed Unity Catalog operational schema
- Add transaction-level audit events
- Add late-arriving data policy
- Add replay/backfill parameters
- Add concurrent-run protection
