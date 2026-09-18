from src.observability.sla import evaluate_sla


def test_sla_passes_when_all_contracts_hold():
    result = evaluate_sla(
        "energy-daily-pipeline",
        "success",
        duration_seconds=300,
        freshness_minutes=20,
        max_duration_seconds=900,
        max_freshness_minutes=60,
    )

    assert result.success is True
    assert result.breaches == ()


def test_sla_reports_multiple_breaches():
    result = evaluate_sla(
        "energy-daily-pipeline",
        "failed",
        duration_seconds=1200,
        freshness_minutes=90,
        max_duration_seconds=900,
        max_freshness_minutes=60,
    )

    assert result.success is False
    assert result.breaches == (
        "PIPELINE_FAILED",
        "DURATION_SLA_BREACH",
        "FRESHNESS_SLA_BREACH",
    )


def test_sla_result_is_dashboard_ready():
    result = evaluate_sla(
        "energy-daily-pipeline",
        "success",
        10,
        5,
        100,
        30,
    )

    payload = result.as_dict()
    assert payload["pipeline_name"] == "energy-daily-pipeline"
    assert payload["success"] is True
    assert payload["breaches"] == []
