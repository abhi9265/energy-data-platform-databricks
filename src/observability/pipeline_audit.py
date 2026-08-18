"""Pipeline audit and operational logging helpers."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class PipelineAuditEvent:
    pipeline_name: str
    run_id: str
    environment: str
    layer: str
    status: str
    input_rows: int
    output_rows: int
    rejected_rows: int
    started_at: str
    completed_at: str
    error_message: str | None = None

    def as_dict(self) -> dict:
        return asdict(self)


def new_audit_event(
    pipeline_name: str,
    run_id: str,
    environment: str,
    layer: str,
    status: str,
    input_rows: int,
    output_rows: int,
    rejected_rows: int,
    started_at: datetime,
    error_message: str | None = None,
) -> PipelineAuditEvent:
    """Create a normalized audit record suitable for a Delta audit table."""
    completed_at = datetime.now(timezone.utc)
    return PipelineAuditEvent(
        pipeline_name=pipeline_name,
        run_id=run_id,
        environment=environment,
        layer=layer,
        status=status,
        input_rows=input_rows,
        output_rows=output_rows,
        rejected_rows=rejected_rows,
        started_at=started_at.astimezone(timezone.utc).isoformat(),
        completed_at=completed_at.isoformat(),
        error_message=error_message,
    )
