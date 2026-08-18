from src.gold.scd2_meter import prepare_meter_changes, scd2_merge_sql


def test_prepare_meter_changes_returns_new_and_changed_meters(spark):
    current = spark.createDataFrame(
        [("MTR001", "north", True), ("MTR002", "south", True)],
        ["meter_id", "region", "is_current"],
    )
    incoming = spark.createDataFrame(
        [("MTR001", "north"), ("MTR002", "east"), ("MTR003", "west")],
        ["meter_id", "region"],
    )

    result = prepare_meter_changes(current, incoming)
    actual = {(row["meter_id"], row["region"]) for row in result.collect()}

    assert actual == {("MTR002", "east"), ("MTR003", "west")}


def test_scd2_sql_uses_environment_namespace():
    sql = scd2_merge_sql("energy_prod", "gold")

    assert "energy_prod.gold.dim_meter" in sql
    assert "is_current = true" in sql
    assert "effective_to = current_date()" in sql
