# Benchmark Methodology

## Purpose

Measure pipeline behavior on controlled synthetic workloads without presenting local execution as a Databricks production benchmark.

## Protocol

1. Fix Python, PySpark, and repository revision.
2. Generate a deterministic dataset with a recorded row count.
3. Record wall-clock time for the pipeline stage under test.
4. Record input rows, output rows, quarantined rows, and duplicate removals where available.
5. Repeat each workload at least three times and report the median.
6. Store the raw result with the commit SHA and execution environment.

## Reporting rule

Do not commit estimated or invented performance numbers. Results belong in `docs/benchmarks/results/` only after an actual run.

## Future Databricks benchmark

A separate Databricks run can compare the same workload with Spark UI metrics such as task duration, shuffle, input/output bytes, and partition behavior. That should be reported separately from local results.