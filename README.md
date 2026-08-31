# Energy Data Platform on Databricks

[![CI](https://github.com/abhi9265/energy-data-platform-databricks/actions/workflows/ci.yml/badge.svg)](https://github.com/abhi9265/energy-data-platform-databricks/actions/workflows/ci.yml)

> **Databricks lakehouse portfolio project:** ingest, validate, deduplicate and model energy meter data with PySpark, Delta Lake, data-quality controls and BI-ready outputs.
>
> **Topics:** `PySpark` · `Databricks` · `Delta Lake` · `Spark SQL` · `Data Quality` · `SCD2` · `Incremental Processing` · `Data Engineering`

## At a glance

A production-oriented **Databricks lakehouse prototype** that turns operational energy meter data into governed, analytics-ready datasets. The repository demonstrates Bronze/Silver/Gold processing, quality controls, dimensional modeling, SCD Type 2 and incremental-processing patterns, with local tests and CI evidence.

> **Evidence boundary:** local execution verifies the transformation and quality path. A real Databricks workspace deployment, executable incremental MERGE orchestration and full SCD2 transaction wiring are intentionally identified as hardening work rather than presented as completed production evidence.

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

## Architecture → Code Map

| Architecture layer | Repository implementation | Purpose |
|---|---|---|
| Bronze | `src/bronze/` | Source-aligned ingestion, explicit schema and lineage |
| Silver | `src/silver/` | Standardization, validation, quarantine and deterministic deduplication |
| Gold | `src/gold/` | Facts, dimensions, KPIs and modeling foundations |
| Quality | `src/quality/` | Reusable data-quality gates and thresholds |
| Observability | `src/observability/` | Pipeline audit framework and audit events |
| Orchestration | `notebooks/` + `resources/` | Databricks execution/job configuration |
| Deployment | `databricks.yml` | Databricks Asset Bundle entry point |
| Tests | `tests/` | Spark transformations and data/contract verification |

## Gold Layer → Power BI Report Preview

The Gold layer exposes BI-ready facts, dimensions and daily regional KPIs. The actual Gold model calculates total energy consumption, average meter reading, active meter count, reading count and kWh per active meter at **date × region** grain. fileciteturn1071file0

### Energy Operations Dashboard

```text
┌──────────────────────────────────────────────────────────────────┐
│ ENERGY OPERATIONS — GOLD LAYER / POWER BI REPORT PREVIEW        │
├──────────────────┬──────────────────┬───────────────────────────┤
│ TOTAL ENERGY     │ AVG READING      │ ACTIVE METERS             │
│ total_energy_kwh │ avg_meter_       │ active_meter_count        │
│                  │ reading_kwh      │                           │
├──────────────────┼──────────────────┼───────────────────────────┤
│ READINGS         │ KWH / METER      │ REPORT GRAIN              │
│ reading_count    │ kwh_per_active_  │ Date × Region             │
│                  │ meter             │                           │
├──────────────────┴──────────────────┴───────────────────────────┤
│                                                                  │
│ REGIONAL ENERGY TREND                                             │
│                                                                  │
│ Region A  █████████████████████████                             │
│ Region B  ███████████████████                                   │
│ Region C  ███████████████                                       │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ DETAIL: Date | Region | Total kWh | Avg kWh | Active Meters     │
│         | Reading Count | kWh / Active Meter                    │
├──────────────────────────────────────────────────────────────────┤
│ Sources: Silver → Gold dimensional model → BI semantic layer    │
└──────────────────────────────────────────────────────────────────┘
```

### Gold → BI semantic contract

| Gold output | Grain | BI usage |
|---|---|---|
| `fact_energy` | Meter reading | Drill-through/detail and time analysis |
| `dim_meter` | Meter | Region and meter slicing |
| `dim_date` | Date | Calendar/time intelligence |
| `energy_kpis` | Date × Region | Executive KPI cards, trends and regional comparison |

> **Presentation note:** this is a **README Power BI-style report preview**, not a claim that a Power BI report has been deployed. It shows how the implemented Gold outputs can be consumed by a BI semantic model. fileciteturn1071file0

## Engineering Capabilities

| Area | Demonstrated capability |
|---|---|
| Lakehouse | Bronze/Silver/Gold Delta architecture |
| Processing | PySpark and Spark SQL transformations |
| Data quality | Contract validation, rejection handling and quarantine |
| Reliability | Deterministic business keys and deduplication |
| Modeling | Dimensional/KPI foundations and SCD Type 2 patterns |
| Incremental processing | Delta MERGE patterns |
| Governance | Unity Catalog three-level namespace conventions |
| Observability | Pipeline audit framework |
| Testing | PySpark and contract tests |
| CI/CD | GitHub Actions validation |
| BI | Gold-layer / Power BI semantic-model contract |

## Execution Evidence

### Verified local path

The repository is designed to run its transformation verification without requiring a Databricks workspace:

```bash
python -m pip install -e .
pytest
```

The documented demo uses the controlled sample dataset to exercise the Bronze → Silver → Gold transformation path, including schema/lineage, validation, quarantine, deduplication and Gold fact/dimension/KPI transformations. fileciteturn1065file0

### What this evidence proves

```text
controlled sample data
        ↓
explicit Bronze schema + lineage
        ↓
Silver validation + quarantine + deduplication
        ↓
Gold fact/dimension + KPI transformations
```

This is **local transformation evidence**, not a claim of a completed Databricks production deployment. The repository explicitly keeps Asset Bundle deployment, incremental MERGE orchestration and full SCD2 transaction wiring in the hardening boundary. fileciteturn1065file0

## Run the Demo

```bash
git clone https://github.com/abhi9265/energy-data-platform-databricks.git
cd energy-data-platform-databricks
python -m pip install -e .
pytest
```

For the short reproducible path, see [`docs/DEMO.md`](docs/DEMO.md).

## Data Flow

```text
Meter reading
     ↓
Bronze ingestion + lineage
     ↓
Schema / quality validation
     ├── rejected → quarantine
     └── accepted
           ↓
       deduplication
           ↓
         Silver
           ↓
   dimensional + KPI models
           ↓
          Gold
           ↓
      Power BI / analytics
```

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

## Development Workflow

1. Create a feature branch.
2. Implement the change with tests.
3. Open a pull request to `main`.
4. GitHub Actions validates the test and data-quality gates.
5. Review and merge only after validation.
6. Promote through environment-specific Databricks configuration.

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

## Interview Topics

This project supports discussions around:

- Bronze/Silver/Gold lakehouse design
- Data-quality and quarantine strategy
- Deterministic deduplication
- Dimensional modeling and serving-layer grain
- SCD Type 2 and incremental MERGE design
- Unity Catalog and environment configuration
- Pipeline auditability
- CI/CD for data platforms
- Designing analytics-ready data for BI workloads
