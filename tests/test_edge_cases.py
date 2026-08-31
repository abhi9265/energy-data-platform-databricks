from src.gold.gold_model import build_energy_kpis


def test_empty_gold_input_produces_no_kpi_rows(spark):
    empty_fact = spark.createDataFrame(
        [], "date_key date, region string, energy_kwh double, meter_id string"
    )
    assert build_energy_kpis(empty_fact).count() == 0
