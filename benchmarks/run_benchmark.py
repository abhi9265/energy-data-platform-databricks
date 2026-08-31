"""Run a reproducible local Spark benchmark for the Energy transformations."""
from __future__ import annotations

import csv
import json
import os
import time
from datetime import datetime, timedelta

from pyspark.sql import SparkSession

from src.gold.gold_model import build_dim_date, build_dim_meter, build_energy_kpis, build_fact_energy


ROWS = int(os.getenv("BENCHMARK_ROWS", "100000"))
OUT = os.getenv("BENCHMARK_OUT", "benchmark-results")


def main() -> None:
    spark = (
        SparkSession.builder.master("local[2]")
        .appName("energy-benchmark")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    try:
        start = time.perf_counter()
        base = datetime(2026, 1, 1)
        rows = [
            (f"meter-{i % 1000:04d}", base + timedelta(minutes=i % 1440), f"region-{i % 5}", float((i % 250) + 1))
            for i in range(ROWS)
        ]
        df = spark.createDataFrame(rows, "meter_id string, reading_timestamp timestamp, region string, energy_kwh double")
        df = df.withColumn("source_system", df["region"]).withColumn("source_file", df["region"]).withColumn("ingested_at", df["reading_timestamp"])
        dim_meter = build_dim_meter(df)
        dim_date = build_dim_date(df)
        fact = build_fact_energy(df, dim_meter)
        kpis = build_energy_kpis(fact)
        counts = {"input_rows": df.count(), "dim_meter_rows": dim_meter.count(), "dim_date_rows": dim_date.count(), "fact_rows": fact.count(), "kpi_rows": kpis.count()}
        elapsed = time.perf_counter() - start
        result = {"workload_rows": ROWS, "runtime_seconds": round(elapsed, 3), "rows_per_second": round(ROWS / elapsed, 2), **counts}
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
        with open(os.path.join(OUT, "results.csv"), "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys())
            writer.writeheader(); writer.writerow(result)
        print(json.dumps(result, indent=2))
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
