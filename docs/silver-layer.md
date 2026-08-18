# Silver Layer — Production Design

## Objective

The Silver layer converts source-aligned Bronze records into a trusted, conformed dataset suitable for downstream Gold analytics.

## Processing Contract

```text
Bronze Delta
   |
   +--> schema/type normalization
   |
   +--> business-key validation
   |
   +--> data-quality classification
   |       |
   |       +--> VALID ------> deduplication ------> Silver Delta
   |       |
   |       +--> REJECTED --> quarantine Delta
   |
   +--> lineage + ingestion metadata retained
```

## Business Grain

One record represents one meter reading for:

`meter_id + reading_timestamp`

This composite key is used for deterministic deduplication and the Delta MERGE strategy.

## Data Quality Rules

| Rule | Action |
|---|---|
| Missing meter ID | Reject |
| Invalid timestamp | Reject |
| Missing region | Reject |
| Missing energy value | Reject |
| Negative energy | Reject |
| Duplicate business key | Keep latest ingestion |

## Idempotency

The pipeline is designed so that replaying the same source batch does not create additional business records. The Delta MERGE uses the business key and only updates a record when the incoming ingestion timestamp is newer.

## Quarantine Strategy

Rejected records are persisted independently instead of being silently discarded. This supports operational investigation, source remediation, and replay after correction.

## Production Extensions

Future iterations will add:

- Auto Loader for incremental file discovery
- Structured Streaming checkpoints
- Delta Change Data Feed
- expectation metrics and alerting
- Unity Catalog governance
- table-level data contracts
- CI/CD validation with GitHub Actions
