from src.observability.audit_store import audit_rows


def test_audit_rows_preserve_normalized_contract():
    class Event:
        def as_dict(self):
            return {"pipeline_name": "energy-daily-pipeline", "run_id": "run-1",
                    "environment": "test", "layer": "silver", "status": "success"}

    assert audit_rows([Event()]) == [{
        "pipeline_name": "energy-daily-pipeline", "run_id": "run-1",
        "environment": "test", "layer": "silver", "status": "success",
    }]
