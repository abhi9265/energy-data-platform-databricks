# Operational Observability

The public MVP contains runtime-agnostic operational contracts that can be connected to Databricks Jobs and Unity Catalog without hard-coded credentials or workspace paths.

## Audit contract

The audit event records pipeline/run identity, environment and layer, status, input/output/rejected row counts, UTC timestamps, and an optional error message.

The Delta adapter can append records to an environment-specific <catalog>.ops.pipeline_audit table.

## SLA contract

The SLA evaluator checks pipeline success, maximum execution duration, and maximum data freshness. Its structured output can feed a Databricks SQL dashboard or alerting layer.

## Runtime wiring

A Databricks deployment should configure an environment-specific <catalog>.ops.pipeline_audit table and grant the job identity least-privilege access.

No benchmark or SLA result is claimed until produced by a reproducible Databricks execution.
