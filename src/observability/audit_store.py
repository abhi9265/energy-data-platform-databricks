"""Spark/Delta adapter for persisting pipeline audit events."""
from __future__ import annotations

from typing import Any

from src.observability.pipeline_audit import PipelineAuditEvent

AUDIT_COLUMNS = [
    "pipeline_name", "run_id", "environment", "layer", "status",
    "input_rows", "output_rows", "rejected_rows", "started_at",
    "completed_at", "error_message",
]


def audit_rows(events: list[PipelineAuditEvent]) -> list[dict[str, Any]]:
    """Return normalized rows ready for Spark createDataFrame/write."""
    return [event.as_dict() for event in events]


def write_audit_events(spark: Any, events: list[PipelineAuditEvent], target_table: str) -> None:
    """Append audit events to a fully-qualified Delta table."""
    if not events:
        return
    df = spark.createDataFrame(audit_rows(events))
    df.select(*AUDIT_COLUMNS).write.format("delta").mode("append").saveAsTable(target_table)
