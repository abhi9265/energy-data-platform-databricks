from src.gold.gold_model import build_dim_meter, build_energy_kpis, build_fact_energy


def test_dim_meter_has_deterministic_surrogate_key(spark):
    df = spark.createDataFrame(
        [("MTR001", "north"), ("MTR001", "north"), ("MTR002", "south")],
        ["meter_id", "region"],
    )

    result = build_dim_meter(df)

    assert result.count() == 2
    assert result.filter("meter_key is null").count() == 0
    assert result.filter("is_current = true").count() == 2


def test_fact_preserves_atomic_meter_reading_grain(spark):
    silver = spark.createDataFrame(
        [("MTR001", "2026-08-01 01:00:00", "north", 12.4, "energy_meter_csv", "file.csv", "2026-08-01 02:00:00")],
        ["meter_id", "reading_timestamp", "region", "energy_kwh", "source_system", "source_file", "ingested_at"],
    )
    dim_meter = build_dim_meter(silver)

    result = build_fact_energy(silver, dim_meter)

    assert result.count() == 1
    assert result.first()["energy_kwh"] == 12.4
    assert result.first()["meter_key"] is not None


def test_daily_kpi_calculation(spark):
    fact = spark.createDataFrame(
        [
            ("MTR001", "2026-08-01", "north", 10.0),
            ("MTR002", "2026-08-01", "north", 20.0),
        ],
        ["meter_id", "date_key", "region", "energy_kwh"],
    )

    result = build_energy_kpis(fact).first()

    assert result["total_energy_kwh"] == 30.0
    assert result["active_meter_count"] == 2
    assert result["reading_count"] == 2
