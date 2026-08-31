# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Analytics Pipeline
# MAGIC
# MAGIC Builds a BI-ready dimensional model from Silver data and persists the
# MAGIC incremental Gold state with transactional Delta MERGE operations.
# MAGIC
# MAGIC **Outputs:** `dim_meter`, `dim_date`, `fact_energy`, and `energy_daily_kpis`.

# COMMAND ----------

from src.gold.gold_model import (
    build_dim_date,
    build_dim_meter,
    build_energy_kpis,
    build_fact_energy,
)
from src.gold.incremental import (
    build_scd2_meter_updates,
    upsert_daily_kpis,
    upsert_fact_energy,
)

SILVER_PATH = "/Volumes/energy_dev/silver/energy_meter_readings"
GOLD_BASE = "/Volumes/energy_dev/gold"
DIM_METER_PATH = f"{GOLD_BASE}/dim_meter"
DIM_DATE_PATH = f"{GOLD_BASE}/dim_date"
FACT_ENERGY_PATH = f"{GOLD_BASE}/fact_energy"
KPI_PATH = f"{GOLD_BASE}/energy_daily_kpis"

# COMMAND ----------

silver_df = spark.read.format("delta").load(SILVER_PATH)

# Build conformed dimensions and atomic fact for the incoming Silver slice.
dim_meter = build_dim_meter(silver_df)
dim_date = build_dim_date(silver_df)
fact_energy = build_fact_energy(silver_df, dim_meter)
energy_daily_kpis = build_energy_kpis(fact_energy)

# COMMAND ----------

# Incremental Gold persistence. Existing Delta tables are updated with MERGE;
# a first run creates the Delta table so the same notebook is bootstrap-safe.
upsert_fact_energy(fact_energy, FACT_ENERGY_PATH)
upsert_daily_kpis(energy_daily_kpis, KPI_PATH)

# dim_date is an immutable conformed dimension: add new dates without
# rewriting existing rows.
if DeltaTable.isDeltaTable(spark, DIM_DATE_PATH):
    DeltaTable.forPath(spark, DIM_DATE_PATH).alias("target").merge(
        dim_date.alias("source"),
        "target.date_key = source.date_key",
    ).whenNotMatchedInsertAll().execute()
else:
    dim_date.write.format("delta").mode("overwrite").save(DIM_DATE_PATH)

# SCD2 meter changes: close the current version before inserting the new
# version. New meters are inserted directly by the same MERGE contract.
if DeltaTable.isDeltaTable(spark, DIM_METER_PATH):
    current_meter = spark.read.format("delta").load(DIM_METER_PATH)
    changes = build_scd2_meter_updates(current_meter, silver_df)
    target = DeltaTable.forPath(spark, DIM_METER_PATH)
    if changes.take(1):
        (
            target.alias("target")
            .merge(
                changes.alias("source"),
                "target.meter_id = source.meter_id AND target.is_current = true",
            )
            .whenMatchedUpdate(
                set={"is_current": "false", "effective_to": "source.effective_from"}
            )
            .whenNotMatchedInsertAll()
            .execute()
        )
else:
    dim_meter.write.format("delta").mode("overwrite").save(DIM_METER_PATH)

# COMMAND ----------

from delta.tables import DeltaTable

print(f"dim_meter rows: {spark.read.format('delta').load(DIM_METER_PATH).count()}")
print(f"dim_date rows: {spark.read.format('delta').load(DIM_DATE_PATH).count()}")
print(f"fact_energy rows: {spark.read.format('delta').load(FACT_ENERGY_PATH).count()}")
print(f"daily KPI rows: {spark.read.format('delta').load(KPI_PATH).count()}")

display(spark.read.format("delta").load(KPI_PATH).orderBy("date_key", "region"))
