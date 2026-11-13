"""Offline tests for EivaBot: config validation and syntax of all Python files."""
from __future__ import annotations

import importlib.util
import os
import pathlib
import py_compile
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------- syntax / compilation ----------

PY_FILES = [p for p in ROOT.rglob("*.py") if ".venv" not in p.parts and "__pycache__" not in p.parts]


@pytest.mark.parametrize("path", PY_FILES, ids=[str(p.relative_to(ROOT)) for p in PY_FILES])
def test_compiles(path):
    py_compile.compile(str(path), doraise=True)


# ---------- config validation ----------

cfg_mod = _load("eiva_config", ROOT / "config.py")


def test_missing_required_vars():
    os.environ.pop("APP_ID", None)
    os.environ.pop("API_HASH", None)
    os.environ.pop("EivaBOT_SESSION", None)
    with pytest.raises(cfg_mod.ConfigError) as exc:
        cfg_mod.Config.from_env()
    assert "APP_ID" in str(exc.value) and "API_HASH" in str(exc.value)


def test_valid_config(monkeypatch):
    monkeypatch.setenv("APP_ID", "12345")
    monkeypatch.setenv("API_HASH", "a" * 32)
    monkeypatch.setenv("EivaBOT_SESSION", "session-string")
    monkeypatch.setenv("HANDLER", "!")
    monkeypatch.setenv("SUDO_USERS", "111 222, abc")
    monkeypatch.setenv("LOGGER_ID", "-1001234")
    monkeypatch.setenv("PM_PERMIT", "DISABLE")

    cfg = cfg_mod.Config.from_env()
    assert cfg.api_id == 12345
    assert cfg.handler == "!"
    assert cfg.sudo_users == [111, 222]  # invalid 'abc' skipped
    assert cfg.logger_id == -1001234
    assert cfg.pm_permit is False


def test_invalid_app_id(monkeypatch):
    monkeypatch.setenv("APP_ID", "notanumber")
    monkeypatch.setenv("API_HASH", "a" * 32)
    monkeypatch.setenv("EivaBOT_SESSION", "x")
    with pytest.raises(cfg_mod.ConfigError):
        cfg_mod.Config.from_env()


def test_env_example_has_no_real_secrets():
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "12345" in text  # placeholder
    assert len([l for l in text.splitlines() if l.startswith("API_HASH=")]) == 1
