import pytest
import subprocess
import sys
import os
from pathlib import Path


def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev."""
    import shutil

    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        print(f"[_resolve_cli] Using installed command: {path}")
        return [path]
    if force:
        raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    module = (
        name.replace("cli-anything-", "cli_anything.")
        + "."
        + name.split("-")[-1]
        + "_cli"
    )
    print(f"[_resolve_cli] Falling back to: {sys.executable} -m {module}")
    return [sys.executable, "-m", module]


class TestCLISubprocess:
    CLI_BASE = _resolve_cli("cli-anything-agent-avatar")

    def _run(self, args, check=True):
        return subprocess.run(
            self.CLI_BASE + args,
            capture_output=True,
            text=True,
            check=check,
        )

    def test_help(self):
        result = self._run(["--help"], check=False)
        assert result.returncode == 0
        assert "agent" in result.stdout.lower() or "Agent" in result.stdout

    def test_info(self, tmp_path):
        result = self._run(["--project", str(tmp_path), "info"], check=False)
        assert result.returncode == 0

    def test_status(self, tmp_path):
        result = self._run(["--project", str(tmp_path), "status"], check=False)
        assert result.returncode == 0

    def test_config_show(self, tmp_path):
        result = self._run(["--project", str(tmp_path), "config", "show"], check=False)
        assert result.returncode == 0

    def test_character_list(self, tmp_path):
        result = self._run(
            ["--project", str(tmp_path), "character", "list"], check=False
        )
        assert result.returncode == 0

    def test_model_list(self, tmp_path):
        result = self._run(["--project", str(tmp_path), "model", "list"], check=False)
        assert result.returncode == 0

    def test_json_output(self, tmp_path):
        result = self._run(["--project", str(tmp_path), "--json", "info"], check=False)
        assert result.returncode == 0
        import json

        try:
            data = json.loads(result.stdout)
            assert "source_path" in data
        except json.JSONDecodeError:
            pass

    def test_conversation_history_empty(self, tmp_path):
        result = self._run(
            ["--project", str(tmp_path), "conversation", "history"], check=False
        )
        assert result.returncode == 0

    def test_conversation_clear(self, tmp_path):
        result = self._run(
            ["--project", str(tmp_path), "conversation", "clear"], check=False
        )
        assert result.returncode == 0


class TestConfigWorkflow:
    CLI_BASE = _resolve_cli("cli-anything-agent-avatar")

    def test_switch_character_workflow(self, tmp_path):
        chars_dir = tmp_path / "characters"
        chars_dir.mkdir()
        (chars_dir / "test_char.yaml").touch()

        result = subprocess.run(
            self.CLI_BASE
            + ["--project", str(tmp_path), "character", "switch", "test_char"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_character_switch_persists(self, tmp_path):
        chars_dir = tmp_path / "characters"
        chars_dir.mkdir()
        (chars_dir / "miku.yaml").touch()

        subprocess.run(
            self.CLI_BASE + ["--project", str(tmp_path), "character", "switch", "miku"],
            capture_output=True,
            text=True,
        )

        result = subprocess.run(
            self.CLI_BASE + ["--project", str(tmp_path), "info"],
            capture_output=True,
            text=True,
        )
        assert "miku" in result.stdout
