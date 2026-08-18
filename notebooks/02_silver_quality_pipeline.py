# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Energy Meter Pipeline
# MAGIC
# MAGIC Production-oriented curation from Bronze to Silver.
# MAGIC
# MAGIC **Controls:** schema normalization, DQ classification, quarantine,
# MAGIC deterministic deduplication, auditability, and Delta persistence.

# COMMAND ----------

from src.bronze.bronze_ingestion import read_energy_meter_csv
from src.silver.silver_transform import build_silver

BRONZE_PATH = "/Volumes/energy_dev/bronze/energy_meter_readings"
SILVER_PATH = "/Volumes/energy_dev/silver/energy_meter_readings"
QUARANTINE_PATH = "/Volumes/energy_dev/quarantine/energy_meter_readings"

# COMMAND ----------

bronze_df = spark.read.format("delta").load(BRONZE_PATH)
curated_df, rejected_df = build_silver(bronze_df)

# COMMAND ----------

# Persist curated records.
curated_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(SILVER_PATH)

# Persist rejected records separately for operational remediation.
rejected_df.write.format("delta").mode("append").save(QUARANTINE_PATH)

# COMMAND ----------

quality_summary = (
    curated_df.groupBy("region")
    .agg(
        {"energy_kwh": "sum"}
    )
    .withColumnRenamed("sum(energy_kwh)", "total_energy_kwh")
)

display(quality_summary)
print(f"Silver rows: {curated_df.count()}")
print(f"Quarantined rows: {rejected_df.count()}")
