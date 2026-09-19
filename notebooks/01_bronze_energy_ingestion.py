# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Energy Meter Ingestion
# MAGIC Reads sample meter data with an explicit schema, adds audit metadata,
# MAGIC and writes the source-aligned dataset to Delta.

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

SOURCE_PATH = f"{VOLUME_ROOT}/raw/sample/energy_meter_readings.csv"
BRONZE_PATH = f"{VOLUME_ROOT}/bronze/energy_meter_readings"

from src.bronze.bronze_ingestion import (
    add_ingestion_metadata,
    read_energy_meter_csv,
    write_bronze_delta,
)

raw_df = read_energy_meter_csv(spark, SOURCE_PATH)
bronze_df = add_ingestion_metadata(raw_df)

display(bronze_df)
write_bronze_delta(bronze_df, BRONZE_PATH)

print(
    f"Bronze ingestion completed. environment={ENVIRONMENT}, "
    f"catalog={CATALOG}, rows={bronze_df.count()}"
)
