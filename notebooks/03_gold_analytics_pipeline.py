# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Analytics Pipeline
# MAGIC
# MAGIC Builds a BI-ready dimensional model from Silver data.
# MAGIC
# MAGIC **Outputs:** `dim_meter`, `dim_date`, `fact_energy`, and `energy_daily_kpis`.

# COMMAND ----------

from src.gold.gold_model import (
    build_dim_date,
    build_dim_meter,
    build_energy_kpis,
    build_fact_energy,
)

SILVER_PATH = "/Volumes/energy_dev/silver/energy_meter_readings"
GOLD_BASE = "/Volumes/energy_dev/gold"

# COMMAND ----------

silver_df = spark.read.format("delta").load(SILVER_PATH)

# Build conformed dimensions and atomic fact.
dim_meter = build_dim_meter(silver_df)
dim_date = build_dim_date(silver_df)
fact_energy = build_fact_energy(silver_df, dim_meter)
energy_daily_kpis = build_energy_kpis(fact_energy)

# COMMAND ----------

# Persist Gold datasets. In production, these writes are replaced by
# transactional Delta MERGE jobs for incremental processing.
dim_meter.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_BASE}/dim_meter")
dim_date.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_BASE}/dim_date")
fact_energy.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_BASE}/fact_energy")
energy_daily_kpis.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_BASE}/energy_daily_kpis")

# COMMAND ----------

print(f"dim_meter rows: {dim_meter.count()}")
print(f"dim_date rows: {dim_date.count()}")
print(f"fact_energy rows: {fact_energy.count()}")
print(f"daily KPI rows: {energy_daily_kpis.count()}")

display(energy_daily_kpis.orderBy("date_key", "region"))
