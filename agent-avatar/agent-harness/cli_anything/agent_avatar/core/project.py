from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


@dataclass
class ProjectState:
    source_path: Path
    config_path: Path
    character_active: str
    server_host: str
    server_port: int
    server_running: bool
    created_at: str


class Project:
    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.config_path = source_path / "conf.yaml"
        self.state_file = source_path / ".cli-state.json"
        self._load_state()

    def _load_state(self):
        if self.state_file.exists():
            with open(self.state_file) as f:
                data = json.load(f)
                self.character_active = data.get("character_active", "mao_pro")
                self.server_host = data.get("server_host", "0.0.0.0")
                self.server_port = data.get("server_port", 12393)
                self.server_running = data.get("server_running", False)
        else:
            self.character_active = "mao_pro"
            self.server_host = "0.0.0.0"
            self.server_port = 12393
            self.server_running = False

    def _save_state(self):
        data = {
            "character_active": self.character_active,
            "server_host": self.server_host,
            "server_port": self.server_port,
            "server_running": self.server_running,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.state_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_info(self) -> dict:
        return {
            "source_path": str(self.source_path),
            "config_path": str(self.config_path),
            "character_active": self.character_active,
            "server_host": self.server_host,
            "server_port": self.server_port,
            "server_running": self.server_running,
        }

    def set_character(self, name: str) -> dict:
        self.character_active = name
        self._save_state()
        return {"character": name, "status": "updated"}

    def set_server_config(self, host: str, port: int) -> dict:
        self.server_host = host
        self.server_port = port
        self._save_state()
        return {"host": host, "port": port, "status": "updated"}


def create_project(source_path: Path) -> Project:
    return Project(source_path)


def load_project(source_path: Optional[Path] = None) -> Project:
    if source_path is None:
        source_path = Path.cwd()
    return Project(source_path)
