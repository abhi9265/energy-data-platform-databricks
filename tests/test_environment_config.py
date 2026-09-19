import json
from pathlib import Path

import pytest

from src.config.environment import (
    load_environment_config,
    validate_environment_isolation,
)


CONFIG_PATH = Path("config/environments.json")


def test_environment_config_has_required_environments_and_isolation():
    config = json.loads(CONFIG_PATH.read_text())

    assert set(config) == {"dev", "test", "prod"}

    catalogs = {env["catalog"] for env in config.values()}
    volume_roots = {env["volume_root"] for env in config.values()}
    assert len(catalogs) == 3
    assert len(volume_roots) == 3

    for env in config.values():
        assert env["schema"] == "analytics"
        assert env["volume_root"].startswith("/Volumes/")
        assert env["catalog"].startswith("energy_")


def test_production_environment_uses_production_catalog():
    config = json.loads(CONFIG_PATH.read_text())
    assert config["prod"]["catalog"] == "energy_prod"


def test_loader_returns_typed_environment_configs():
    configs = load_environment_config(CONFIG_PATH)
    validate_environment_isolation(configs)

    assert configs["dev"].silver_root == "/Volumes/energy_dev/silver"
    assert configs["prod"].gold_root == "/Volumes/energy_prod/gold"


def test_loader_rejects_missing_environment(tmp_path):
    path = tmp_path / "environments.json"
    path.write_text(json.dumps({"dev": {
        "catalog": "energy_dev",
        "schema": "analytics",
        "volume_root": "/Volumes/energy_dev",
    }}))

    with pytest.raises(ValueError, match="Missing environments"):
        load_environment_config(path)
