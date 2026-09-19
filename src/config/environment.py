"""Environment configuration and path helpers for the Energy platform."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REQUIRED_ENVIRONMENTS = {"dev", "test", "prod"}


@dataclass(frozen=True)
class EnvironmentConfig:
    name: str
    catalog: str
    schema: str
    volume_root: str

    @property
    def bronze_root(self) -> str:
        return f"{self.volume_root}/bronze"

    @property
    def silver_root(self) -> str:
        return f"{self.volume_root}/silver"

    @property
    def gold_root(self) -> str:
        return f"{self.volume_root}/gold"

    @property
    def ops_root(self) -> str:
        return f"{self.volume_root}/ops"


def load_environment_config(path: str | Path) -> dict[str, EnvironmentConfig]:
    raw = json.loads(Path(path).read_text())
    missing = REQUIRED_ENVIRONMENTS - set(raw)
    if missing:
        raise ValueError(f"Missing environments: {sorted(missing)}")

    configs: dict[str, EnvironmentConfig] = {}
    for name, values in raw.items():
        configs[name] = EnvironmentConfig(
            name=name,
            catalog=values["catalog"],
            schema=values["schema"],
            volume_root=values["volume_root"].rstrip("/"),
        )
    return configs


def validate_environment_isolation(configs: dict[str, EnvironmentConfig]) -> None:
    catalogs = [cfg.catalog for cfg in configs.values()]
    volume_roots = [cfg.volume_root for cfg in configs.values()]
    if len(catalogs) != len(set(catalogs)):
        raise ValueError("Environment catalogs must be unique")
    if len(volume_roots) != len(set(volume_roots)):
        raise ValueError("Environment volume roots must be unique")
