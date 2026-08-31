from src.gold.incremental import build_scd2_meter_updates


def test_scd2_ignores_replayed_unchanged_meter(spark):
    current = spark.createDataFrame(
        [("MTR001", "north", "2026-08-01", "9999-12-31", True, 1)],
        ["meter_id", "region", "effective_from", "effective_to", "is_current", "meter_key"],
    ).withColumn("effective_from", __import__("pyspark.sql.functions", fromlist=["to_date"]).to_date("effective_from"))
    current = current.withColumn(
        "effective_to", __import__("pyspark.sql.functions", fromlist=["to_date"]).to_date("effective_to")
    )
    incoming = spark.createDataFrame(
        [("MTR001", "north")], ["meter_id", "region"]
    )

    result = build_scd2_meter_updates(current, incoming)

    assert result.count() == 0


def test_scd2_detects_changed_meter_region(spark):
    current = spark.createDataFrame(
        [("MTR001", "north", "2026-08-01", "9999-12-31", True, 1)],
        ["meter_id", "region", "effective_from", "effective_to", "is_current", "meter_key"],
    )
    from pyspark.sql import functions as F

    current = current.withColumn("effective_from", F.to_date("effective_from"))
    current = current.withColumn("effective_to", F.to_date("effective_to"))
    incoming = spark.createDataFrame(
        [("MTR001", "south")], ["meter_id", "region"]
    )

    result = build_scd2_meter_updates(current, incoming)

    assert result.count() == 1
    row = result.first()
    assert row["meter_id"] == "MTR001"
    assert row["region"] == "south"
    assert row["is_current"] is True
    assert str(row["effective_to"]) == "9999-12-31"


def test_scd2_detects_new_meter(spark):
    current = spark.createDataFrame(
        [("MTR001", "north", "2026-08-01", "9999-12-31", True, 1)],
        ["meter_id", "region", "effective_from", "effective_to", "is_current", "meter_key"],
    )
    from pyspark.sql import functions as F

    current = current.withColumn("effective_from", F.to_date("effective_from"))
    current = current.withColumn("effective_to", F.to_date("effective_to"))
    incoming = spark.createDataFrame(
        [("MTR002", "south")], ["meter_id", "region"]
    )

    result = build_scd2_meter_updates(current, incoming)

    assert result.count() == 1
    assert result.first()["meter_id"] == "MTR002"
