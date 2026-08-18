# Gold Layer — Analytics Data Model

## Objective

The Gold layer exposes business-ready, query-efficient datasets for analytics and BI. It converts conformed Silver records into a star-schema model and aggregated KPI datasets.

## Star Schema

```text
                 +-------------+
                 |  dim_date   |
                 +------+------+ 
                        |
                        |
+-------------+    +---+-----------+    +-------------+
|  dim_meter  +----+  fact_energy  +----+   BI / SQL   |
+-------------+    +-------+-------+    +-------------+
                           |
                           v
                  +------------------+
                  | energy_daily_kpis|
                  +------------------+
```

## Gold Objects

### `dim_meter`

Conformed meter dimension containing the deterministic surrogate `meter_key`, meter identifier, region, and current-record metadata.

### `dim_date`

Calendar dimension generated from the observed Silver date range. It supports year/month/day and day-of-week slicing without repeating date derivations across BI queries.

### `fact_energy`

Atomic fact at `meter_id + reading_timestamp` grain. It contains meter/date keys, time attributes, region, energy quantity, and source lineage.

### `energy_daily_kpis`

Aggregated regional daily metrics:

- Total energy consumption (kWh)
- Average meter reading (kWh)
- Active meter count
- Reading count
- kWh per active meter

## Design Decisions

### Star schema

Dimensions are separated from the atomic fact to support reusable slicing and predictable BI query patterns.

### Surrogate key

`meter_key` is generated independently of the source identifier, allowing future source-system consolidation and dimensional history.

### Incremental processing

The repository includes Delta `MERGE` patterns for both atomic facts and aggregate KPI tables. The target production implementation can process only changed records or affected date/region partitions.

### SCD Type 2 readiness

`dim_meter` includes `effective_from`, `effective_to`, and `is_current`. Future changes to meter attributes can therefore be historized without rewriting existing fact relationships.

## Production Hardening Roadmap

- Replace overwrite notebook writes with transactional MERGE orchestration
- Add SCD Type 2 change detection for meter attributes
- Add partitioning/Z-ORDER strategy based on actual workload
- Add Unity Catalog table governance
- Add data contracts and schema evolution controls
- Add dbt/SQL semantic transformations where appropriate
- Add Power BI semantic model and incremental refresh
- Add CI/CD and automated data-quality gates
