# Databricks Deployment Runbook

This runbook describes how to validate the Asset Bundle and the daily energy pipeline in a real Databricks workspace. Repository configuration is implemented, but a successful deployment is only evidence once these commands have been executed against an actual workspace.

## Preconditions

- Databricks CLI with Asset Bundles support installed.
- A workspace URL and authentication configured for the CLI.
- Unity Catalog catalogs and Volumes available for the selected environment.
- Required permissions to deploy the bundle and run the job.

## Validate the bundle

From the repository root:

    databricks bundle validate -t dev

Repeat for test and prod after confirming the corresponding workspace permissions and catalog/volume setup.

## Deploy

    databricks bundle deploy -t dev

The bundle defines the energy_daily_pipeline job and passes environment, catalog, schema and volume-root parameters into each notebook task.

## Run

    databricks bundle run -t dev energy_daily_pipeline

Confirm that Bronze, Silver and Gold tasks complete successfully and that the run uses the intended environment-specific paths.

## Runtime validation checklist

- Bronze writes to the selected environment's Bronze path.
- Silver writes curated records and quarantine records to the selected environment.
- Gold writes fact, KPI, date and SCD2 meter state to the selected environment.
- Re-running the same input does not create unintended duplicate Gold facts or SCD2 versions.
- Job timeout/retry settings behave as configured.
- Audit and SLA outputs are available for operational review.

## Evidence boundary

A successful bundle validate only proves that the bundle configuration is syntactically and structurally valid. A successful bundle deploy proves deployment to the authenticated workspace. A successful bundle run plus inspection of the resulting tables and job run proves runtime behavior.

Do not describe local tests or bundle validation as production deployment evidence. Record the workspace, target environment, run identifier and observed results when a real runtime validation is performed.
