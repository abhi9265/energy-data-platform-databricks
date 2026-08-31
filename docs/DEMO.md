# Local Demo

This demo proves the transformation path without requiring a Databricks workspace.

## Run

```bash
python -m pip install -e .
pytest
```

The test suite exercises the Bronze/Silver/Gold transformations and data-quality contracts using the controlled sample dataset.

## What the demo proves

```text
sample meter data
      ↓
explicit Bronze schema + lineage
      ↓
Silver validation + quarantine + deduplication
      ↓
Gold fact/dimension + KPI transformations
```

The repository intentionally does not claim that this local run is a substitute for a Databricks deployment. Databricks Asset Bundle deployment, incremental MERGE orchestration, and full SCD2 transaction wiring remain deployment-hardening work.
