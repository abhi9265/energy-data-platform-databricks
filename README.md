# Energy Data Platform on Databricks

A production-style Data Engineering portfolio project demonstrating Azure Databricks, PySpark, Delta Lake, Spark SQL, GitHub Actions, Unity Catalog conventions, dimensional modelling, data-quality engineering, and BI design.

## Architecture

```text
Source Systems
      |
      v
   BRONZE -------- raw + lineage + ingestion metadata
      |
      v
   SILVER -------- validation + standardization + quarantine + deduplication
      |
      v
    GOLD --------- star schema + SCD2 + incremental MERGE + KPIs
      |
      +--------------------+
      |                    |
      v                    v
   Power BI          Operational Audit

CI/CD validates every pull request before promotion to main.
```

## Technology Stack

- Azure Databricks
- PySpark / Spark SQL
- Delta Lake
- Databricks Asset Bundles
- Unity Catalog
- Python / pytest
- GitHub Actions
- Power BI semantic modelling

## Engineering Controls

- Explicit schemas and data contracts
- Deterministic business keys and deduplication
- Quarantine for rejected records
- Configurable data-quality promotion gates
- SCD Type 2 dimension design
- Incremental Delta MERGE patterns
- Dev / test / prod configuration separation
- Pipeline audit events
- CI unit-test and quality-gate workflow
- Unity Catalog three-level namespace conventions
- BI contract isolated to Gold datasets

## Repository Structure

```text
.github/workflows/       CI/CD automation
config/                  environment + governance configuration
data/sample/             controlled sample source data
docs/                    architecture, modelling, BI and operational docs
notebooks/               Databricks orchestration notebooks
resources/               Databricks job definitions
src/bronze/              source-aligned ingestion
src/silver/              curation and data quality
src/gold/                dimensional model, KPIs and SCD2
src/observability/       pipeline audit framework
src/quality/             reusable data-quality gates
tests/                   Spark unit and contract tests
databricks.yml           Databricks Asset Bundle entry point
```

## Development Workflow

1. Create a feature branch.
2. Implement and test the change.
3. Open a pull request to `main`.
4. GitHub Actions runs PySpark unit tests and data-quality contract tests.
5. Review and merge only after validation.
6. Deploy through environment-specific Databricks configuration.

## Business Domain

The initial domain models energy meter readings and can be extended with revenue, billing statements, reference mappings, and weather inputs.

## Status

**Engineering Foundation — CI/CD, quality gates, environment contracts, SCD2, observability and BI foundations in progress.**
