# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Energy Meter Pipeline
# MAGIC
# MAGIC Production-oriented curation from Bronze to Silver.
# MAGIC
# MAGIC **Controls:** schema normalization, DQ classification, quarantine,
# MAGIC deterministic deduplication, auditability, and Delta persistence.

# COMMAND ----------

dbutils.widgets.text("environment", "dev", "Environment")
dbutils.widgets.text("catalog", "energy_dev", "Unity Catalog")
dbutils.widgets.text("schema", "analytics", "Schema")
dbutils.widgets.text("volume_root", "/Volumes/energy_dev", "Volume root")

ENVIRONMENT = dbutils.widgets.get("environment").strip().lower()
CATALOG = dbutils.widgets.get("catalog").strip()
SCHEMA = dbutils.widgets.get("schema").strip()
VOLUME_ROOT = dbutils.widgets.get("volume_root").rstrip("/")

if ENVIRONMENT not in {"dev", "test", "prod"}:
    raise ValueError(f"Unsupported environment: {ENVIRONMENT}")
if not CATALOG.startswith("energy_"):
    raise ValueError(f"Unexpected catalog: {CATALOG}")
if not VOLUME_ROOT.startswith("/Volumes/"):
    raise ValueError(f"Unexpected volume root: {VOLUME_ROOT}")

BRONZE_PATH = f"{VOLUME_ROOT}/bronze/energy_meter_readings"
SILVER_PATH = f"{VOLUME_ROOT}/silver/energy_meter_readings"
QUARANTINE_PATH = f"{VOLUME_ROOT}/quarantine/energy_meter_readings"

from src.silver.silver_transform import build_silver

bronze_df = spark.read.format("delta").load(BRONZE_PATH)
curated_df, rejected_df = build_silver(bronze_df)

curated_df.write.format("delta").mode("overwrite").option(
    "overwriteSchema", "true"
).save(SILVER_PATH)

rejected_df.write.format("delta").mode("append").save(QUARANTINE_PATH)

quality_summary = (
    curated_df.groupBy("region")
    .agg({"energy_kwh": "sum"})
    .withColumnRenamed("sum(energy_kwh)", "total_energy_kwh")
)

display(quality_summary)
print(
    f"Silver completed. environment={ENVIRONMENT}, "
    f"catalog={CATALOG}, rows={curated_df.count()}, "
    f"quarantined={rejected_df.count()}"
)
