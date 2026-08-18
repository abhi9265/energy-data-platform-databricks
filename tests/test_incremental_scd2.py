from src.gold.incremental import affected_partitions, select_incremental_batch
from src.gold.scd2_meter import prepare_meter_changes


def test_incremental_batch_uses_strict_watermark(spark):
    df = spark.createDataFrame(
        [("MTR001", 10), ("MTR002", 20), ("MTR003", 30)],
        ["meter_id", "sequence_no"],
    )

    result = select_incremental_batch(df, "sequence_no", 20)

    assert [r.meter_id for r in result.collect()] == ["MTR003"]


def test_affected_partitions_are_distinct(spark):
    df = spark.createDataFrame(
        [
            ("2026-08-01 01:00:00", "north"),
            ("2026-08-01 02:00:00", "north"),
            ("2026-08-01 01:00:00", "south"),
        ],
        ["reading_timestamp", "region"],
    )

    assert affected_partitions(df).count() == 2


def test_scd2_detects_new_and_changed_meters(spark):
    current = spark.createDataFrame(
        [("MTR001", "north", True), ("MTR002", "south", True)],
        ["meter_id", "region", "is_current"],
    )
    incoming = spark.createDataFrame(
        [("MTR001", "west"), ("MTR002", "south"), ("MTR003", "east")],
        ["meter_id", "region"],
    )

    result = prepare_meter_changes(current, incoming)
    rows = {(r.meter_id, r.region) for r in result.collect()}

    assert rows == {("MTR001", "west"), ("MTR003", "east")}
