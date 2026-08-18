# Databricks notebook source
# MAGIC %md
# MAGIC # Incremental Gold Pipeline
# MAGIC
# MAGIC Processes only records newer than the persisted watermark and recomputes
# MAGIC only affected date/region KPI partitions.

# COMMAND ----------

from src.gold.incremental import affected_partitions, select_incremental_batch

CATALOG = "energy_dev"
SCHEMA = "gold"
SILVER_TABLE = f"{CATALOG}.silver.energy_meter_readings"
WATERMARK_TABLE = f"{CATALOG}.ops.pipeline_watermarks"

# COMMAND ----------

# In production this value is read from the audit/watermark table.
last_watermark = spark.sql(
    f"SELECT max_watermark FROM {WATERMARK_TABLE} WHERE pipeline_name = 'silver_to_gold'"
).first()["max_watermark"]

silver_df = spark.table(SILVER_TABLE)
batch_df = select_incremental_batch(silver_df, "ingested_at", last_watermark)

print(f"Incremental records selected: {batch_df.count()}")

# COMMAND ----------

# Rebuild only affected date/region aggregates, then MERGE them into Gold.
affected = affected_partitions(batch_df)
affected.createOrReplaceTempView("affected_partitions")

spark.sql(f"""
CREATE OR REPLACE TEMP VIEW energy_daily_kpis_updates AS
SELECT
    to_date(s.reading_timestamp) AS date_key,
    s.region,
    sum(s.energy_kwh) AS total_energy_kwh,
    avg(s.energy_kwh) AS avg_meter_reading_kwh,
    count(DISTINCT s.meter_id) AS active_meter_count,
    count(*) AS reading_count,
    sum(s.energy_kwh) / count(DISTINCT s.meter_id) AS kwh_per_active_meter
FROM {SILVER_TABLE} s
INNER JOIN affected_partitions p
  ON to_date(s.reading_timestamp) = p.date_key
 AND s.region = p.region
GROUP BY to_date(s.reading_timestamp), s.region
""")

# The repository's gold_merge.sql contains the transactional MERGE contract.
print("Incremental Gold batch prepared; execute fact/KPI MERGEs and advance watermark atomically.")
