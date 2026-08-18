# Energy Data Platform on Databricks

[![CI](https://github.com/abhi9265/energy-data-platform-databricks/actions/workflows/ci.yml/badge.svg)](https://github.com/abhi9265/energy-data-platform-databricks/actions/workflows/ci.yml)

A production-style **Databricks lakehouse** project demonstrating how source energy data can be transformed into governed, incremental, BI-ready datasets.

> **Portfolio focus:** PySpark, Delta Lake, dimensional modeling, SCD Type 2, incremental processing, data quality, CI/CD, Unity Catalog conventions, auditability, and semantic analytics.

## Architecture

```text
Source Systems
      │
      ▼
   BRONZE
 raw + lineage + ingestion metadata
      │
      ▼
   SILVER
 validation + standardization + quarantine + deduplication
      │
      ▼
    GOLD
 star schema + SCD2 + incremental MERGE + KPIs
      │
   ┌──┴─────────────┐
   ▼                ▼
Power BI       Operational Audit
```

## Technology

- Azure Databricks
- PySpark / Spark SQL
- Delta Lake
- Databricks Asset Bundles
- Unity Catalog conventions
- Python / pytest
- GitHub Actions
- Power BI semantic-model contract

## Engineering Controls

- Explicit schemas and data contracts
- Deterministic business keys and deduplication
- Quarantine for rejected records
- Reusable data-quality thresholds
- SCD Type 2 dimension design
- Incremental Delta MERGE patterns
- Dev/test/prod configuration contracts
- Pipeline audit events
- CI unit-test and quality-gate workflow
- Unity Catalog three-level namespace conventions
- Gold-layer BI contract

## Repository Structure

```text
.github/workflows/   CI/CD automation
config/              environment and governance configuration
data/sample/         controlled sample data
docs/                architecture, modeling, BI and operations
notebooks/           Databricks orchestration
resources/           Databricks job definitions
src/bronze/          source-aligned ingestion
src/silver/          curation and quality
src/gold/            dimensional model, KPIs and SCD2
src/observability/   pipeline audit framework
src/quality/         reusable data-quality gates
tests/               Spark and contract tests
databricks.yml       Asset Bundle entry point
```

## Development Workflow

1. Create a feature branch.
2. Implement the change with tests.
3. Open a pull request to `main`.
4. GitHub Actions validates unit and data-quality tests.
5. Review and merge only after validation.
6. Promote through environment-specific Databricks configuration.

## Business Domain

The initial model covers energy meter readings and is designed to extend to revenue, billing, reference mappings, and external weather inputs.

## Current Status

**Production engineering foundation implemented.**

The next hardening milestones are executable incremental orchestration, full SCD2 transaction wiring, deployment validation, and end-to-end operational observability.
