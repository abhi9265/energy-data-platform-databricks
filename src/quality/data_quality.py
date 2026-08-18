"""Reusable data-quality gates for pipeline promotion.

The quality layer is intentionally independent of Databricks orchestration so
it can run in CI, local development, or as a pre-promotion gate in a job.
"""

from dataclasses import dataclass

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


@dataclass(frozen=True)
class QualityThresholds:
    """Promotion thresholds expressed as ratios from 0 to 1."""

    max_rejection_rate: float = 0.02
    max_duplicate_rate: float = 0.01
    min_valid_rate: float = 0.98


@dataclass(frozen=True)
class QualityResult:
    """Machine-readable quality result suitable for audit logging."""

    total_rows: int
    rejected_rows: int
    duplicate_rows: int
    rejection_rate: float
    duplicate_rate: float
    valid_rate: float
    passed: bool


def evaluate_quality(
    df: DataFrame,
    business_keys: list[str],
    thresholds: QualityThresholds | None = None,
) -> QualityResult:
    """Evaluate DQ metrics and fail promotion when configured thresholds are breached."""
    thresholds = thresholds or QualityThresholds()
    total_rows = df.count()

    if total_rows == 0:
        return QualityResult(0, 0, 0, 0.0, 0.0, 0.0, False)

    rejected_rows = df.filter(F.col("dq_status") == "REJECTED").count() if "dq_status" in df.columns else 0
    distinct_rows = df.select(*business_keys).dropDuplicates().count()
    duplicate_rows = total_rows - distinct_rows

    rejection_rate = rejected_rows / total_rows
    duplicate_rate = duplicate_rows / total_rows
    valid_rate = 1 - rejection_rate
    passed = (
        rejection_rate <= thresholds.max_rejection_rate
        and duplicate_rate <= thresholds.max_duplicate_rate
        and valid_rate >= thresholds.min_valid_rate
    )

    return QualityResult(
        total_rows=total_rows,
        rejected_rows=rejected_rows,
        duplicate_rows=duplicate_rows,
        rejection_rate=rejection_rate,
        duplicate_rate=duplicate_rate,
        valid_rate=valid_rate,
        passed=passed,
    )


def assert_quality_gate(result: QualityResult) -> None:
    """Raise a clear CI/job failure when data quality is below the contract."""
    if not result.passed:
        raise ValueError(
            "Data-quality gate failed: "
            f"rejection_rate={result.rejection_rate:.2%}, "
            f"duplicate_rate={result.duplicate_rate:.2%}, "
            f"valid_rate={result.valid_rate:.2%}"
        )
