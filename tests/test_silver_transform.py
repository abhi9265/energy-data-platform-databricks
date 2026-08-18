from src.silver.silver_transform import apply_data_quality_rules, deduplicate_valid_records


def test_negative_energy_is_rejected(spark):
    df = spark.createDataFrame(
        [("MTR001", "2026-08-01 00:00:00", "north", -1.0)],
        ["meter_id", "reading_timestamp", "region", "energy_kwh"],
    )
    result = apply_data_quality_rules(df)
    row = result.first()
    assert row["dq_status"] == "REJECTED"
    assert row["dq_reason"] == "NEGATIVE_ENERGY"


def test_duplicate_business_key_keeps_latest_ingestion(spark):
    df = spark.createDataFrame(
        [
            ("MTR001", "2026-08-01 00:00:00", "north", 10.0, "2026-08-01 01:00:00", "VALID"),
            ("MTR001", "2026-08-01 00:00:00", "north", 12.0, "2026-08-01 02:00:00", "VALID"),
        ],
        ["meter_id", "reading_timestamp", "region", "energy_kwh", "ingested_at", "dq_status"],
    )
    result = deduplicate_valid_records(df)
    assert result.count() == 1
    assert result.first()["energy_kwh"] == 12.0
