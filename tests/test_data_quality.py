from src.quality.data_quality import QualityThresholds, assert_quality_gate, evaluate_quality


def test_quality_gate_passes_within_thresholds(spark):
    df = spark.createDataFrame(
        [
            ("MTR001", "2026-08-01 00:00:00", "VALID"),
            ("MTR002", "2026-08-01 00:00:00", "VALID"),
        ],
        ["meter_id", "reading_timestamp", "dq_status"],
    )

    result = evaluate_quality(df, ["meter_id", "reading_timestamp"])

    assert result.passed is True
    assert result.valid_rate == 1.0
    assert_quality_gate(result)


def test_quality_gate_rejects_excessive_bad_records(spark):
    df = spark.createDataFrame(
        [
            ("MTR001", "2026-08-01 00:00:00", "VALID"),
            ("MTR002", "2026-08-01 00:00:00", "REJECTED"),
            ("MTR003", "2026-08-01 00:00:00", "REJECTED"),
        ],
        ["meter_id", "reading_timestamp", "dq_status"],
    )

    result = evaluate_quality(
        df,
        ["meter_id", "reading_timestamp"],
        QualityThresholds(max_rejection_rate=0.10, max_duplicate_rate=0.01, min_valid_rate=0.90),
    )

    assert result.passed is False
