from src.bronze.bronze_ingestion import add_ingestion_metadata


def test_add_ingestion_metadata(spark):
    source_df = spark.createDataFrame(
        [("MTR001", "north", 12.4)],
        ["meter_id", "region", "energy_kwh"],
    )

    result = add_ingestion_metadata(source_df)

    assert "source_system" in result.columns
    assert "source_file" in result.columns
    assert "ingested_at" in result.columns
    assert result.first()["source_system"] == "energy_meter_csv"
