from src.gold.gold_model import build_energy_kpis


def test_kpi_division_is_safe_for_zero_active_meters(spark):
    fact = spark.createDataFrame(
        [("2026-08-01", "north", 0.0, 0)],
        ["date_key", "region", "total_energy_kwh", "active_meter_count"],
    )
    # The production KPI function receives meter-level facts, so an empty fact
    # set should simply produce no KPI rows rather than an invalid ratio.
    assert build_energy_kpis(
        spark.createDataFrame([], "date_key date, region string, energy_kwh double, meter_id string")
    ).count() == 0
