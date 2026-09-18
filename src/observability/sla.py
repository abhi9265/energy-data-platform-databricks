"""Pure-Python SLA evaluation helpers for pipeline operations.

These helpers are runtime-agnostic so SLA contracts can be tested in CI and
used later by Databricks jobs or an operational dashboard.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SlaResult:
    pipeline_name: str
    status: str
    duration_seconds: float
    freshness_minutes: float
    success: bool
    breaches: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "pipeline_name": self.pipeline_name,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
            "freshness_minutes": self.freshness_minutes,
            "success": self.success,
            "breaches": list(self.breaches),
        }


def evaluate_sla(
    pipeline_name: str,
    status: str,
    duration_seconds: float,
    freshness_minutes: float,
    max_duration_seconds: float,
    max_freshness_minutes: float,
) -> SlaResult:
    """Evaluate operational SLA thresholds without requiring a Spark runtime."""
    breaches: list[str] = []
    if status.lower() != "success":
        breaches.append("PIPELINE_FAILED")
    if duration_seconds > max_duration_seconds:
        breaches.append("DURATION_SLA_BREACH")
    if freshness_minutes > max_freshness_minutes:
        breaches.append("FRESHNESS_SLA_BREACH")

    return SlaResult(
        pipeline_name=pipeline_name,
        status=status,
        duration_seconds=duration_seconds,
        freshness_minutes=freshness_minutes,
        success=not breaches,
        breaches=tuple(breaches),
    )
