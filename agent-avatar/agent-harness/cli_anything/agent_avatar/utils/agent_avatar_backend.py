import subprocess
import shutil
import os
from pathlib import Path
from typing import Optional, Dict, Any
import signal


CONTAINER_NAME = "open-llm-vtuber"


def get_docker_compose_path(source_path: Path) -> Optional[Path]:
    compose_files = [
        source_path / "docker-compose.yml",
        source_path / "docker-compose.yaml",
    ]
    for compose_file in compose_files:
        if compose_file.exists():
            return source_path
    return None


def start_server(
    source_path: Path,
    verbose: bool = False,
) -> Dict[str, Any]:
    compose_path = get_docker_compose_path(source_path)
    if not compose_path:
        return {"status": "error", "message": "docker-compose.yml not found"}

    cmd = ["docker", "compose", "up", "-d"]
    if verbose:
        result = subprocess.run(
            cmd,
            cwd=str(compose_path),
            capture_output=True,
            text=True,
        )
    else:
        result = subprocess.run(
            cmd,
            cwd=str(compose_path),
            capture_output=True,
            text=True,
        )

    if result.returncode == 0:
        return {"status": "started", "message": "Docker container started"}
    else:
        return {
            "status": "error",
            "message": result.stderr or "Failed to start container",
        }


def stop_server(source_path: Optional[Path] = None) -> Dict[str, Any]:
    if not source_path:
        return {"status": "error", "message": "No project path provided"}

    compose_path = get_docker_compose_path(source_path)
    if not compose_path:
        return {"status": "error", "message": "docker-compose.yml not found"}

    result = subprocess.run(
        ["docker", "compose", "down"],
        cwd=str(compose_path),
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return {"status": "stopped", "message": "Docker container stopped"}
    else:
        return {
            "status": "error",
            "message": result.stderr or "Failed to stop container",
        }


def get_server_status(source_path: Optional[Path] = None) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                f"name={CONTAINER_NAME}",
                "--format",
                "{{.Names}}",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if CONTAINER_NAME in result.stdout:
            return {"running": True, "container": CONTAINER_NAME, "status": "running"}
    except Exception:
        pass

    return {"running": False, "container": CONTAINER_NAME, "status": "stopped"}


def validate_config(config_path: Path) -> Dict[str, Any]:
    try:
        from ruamel.yaml import YAML

        yaml = YAML()
        with open(config_path) as f:
            config = yaml.load(f)
        return {"valid": True, "config": config}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def list_characters(source_path: Path) -> list:
    characters_dir = source_path / "characters"
    if not characters_dir.exists():
        return []
    return [f.stem for f in characters_dir.glob("*.yaml")]


def list_live2d_models(source_path: Path) -> list:
    models_dir = source_path / "live2d-models"
    if not models_dir.exists():
        return []
    return [f.stem for f in models_dir.glob("*.model3.json")]
