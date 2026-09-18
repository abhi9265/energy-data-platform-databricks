import json
from pathlib import Path


def test_environment_config_has_required_environments_and_isolation():
    config = json.loads(Path("config/environments.json").read_text())

    assert set(config) == {"dev", "test", "prod"}

    catalogs = {env["catalog"] for env in config.values()}
    assert len(catalogs) == 3

    for env in config.values():
        assert env["schema"] == "analytics"
        assert env["volume_root"].startswith("/Volumes/")
        assert env["catalog"].startswith("energy_")


def test_production_environment_uses_production_catalog():
    config = json.loads(Path("config/environments.json").read_text())
    assert config["prod"]["catalog"] == "energy_prod"
