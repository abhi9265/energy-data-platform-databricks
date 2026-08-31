# Energy Data Platform on Databricks

[![CI](https://github.com/abhi9265/energy-data-platform-databricks/actions/workflows/ci.yml/badge.svg)](https://github.com/abhi9265/energy-data-platform-databricks/actions/workflows/ci.yml)

A production-oriented **Databricks lakehouse prototype** showing how energy meter data can be ingested, validated, deduplicated, modeled and prepared for BI workloads.

> **Portfolio focus:** PySpark, Delta Lake, dimensional modeling, SCD Type 2 patterns, incremental processing, data quality, CI/CD, Unity Catalog conventions, auditability and semantic analytics.

## Business Problem

Energy data commonly arrives as operational meter readings that need to be cleaned, validated and transformed into trustworthy analytics datasets. This project demonstrates a maintainable lakehouse design for that problem while keeping the sample data and execution environment reproducible.

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
 star schema + KPI models + SCD2/incremental patterns
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
- SCD Type 2 dimension design/patterns
- Incremental Delta MERGE patterns
- Dev/test/prod configuration contracts
- Pipeline audit events
- CI unit-test and data-quality gates
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
src/gold/            dimensional model, KPIs and SCD2 patterns
src/observability/   pipeline audit framework
src/quality/         reusable data-quality gates
tests/               Spark and contract tests
databricks.yml       Asset Bundle entry point
```

## Local Development

The repository is designed to be testable without a Databricks workspace:

```bash
python -m pip install -e .
pytest
```

The tests exercise the PySpark transformations and data-quality contracts locally. Databricks deployment is represented through the Asset Bundle configuration and requires a configured Databricks environment.

See [`docs/DEMO.md`](docs/DEMO.md) for the short reproducible local execution path and what it proves.

## Development Workflow

1. Create a feature branch.
2. Implement the change with tests.
3. Open a pull request to `main`.
4. GitHub Actions validates the test and data-quality gates.
5. Review and merge only after validation.
6. Promote through environment-specific Databricks configuration.

## Business Domain

The initial model covers energy meter readings and is designed to extend to revenue, billing, reference mappings and external weather inputs.

## Implementation Status

### Implemented

- Bronze ingestion with explicit schema and lineage metadata
- Silver standardization, validation, quarantine and deterministic deduplication
- Gold dimensional/KPI modeling foundations
- Reusable data-quality and audit utilities
- SCD Type 2 and incremental Delta MERGE patterns
- PySpark tests and GitHub Actions CI
- Databricks Asset Bundle job configuration

### Hardening / deployment work

- Wire incremental MERGE logic into the executable notebook orchestration
- Wire SCD2 transaction logic into the executable Gold path
- Validate Asset Bundle deployment in a real Databricks workspace
- Expand end-to-end operational observability and production SLAs

This distinction is intentional: the repository documents implemented code separately from deployment hardening so that the portfolio does not overstate production readiness.
