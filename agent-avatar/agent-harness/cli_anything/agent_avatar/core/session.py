from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import json
from pathlib import Path
import copy


@dataclass
class SessionSnapshot:
    timestamp: str
    character: str
    server_host: str
    server_port: int


@dataclass
class Session:
    project_path: Path
    character: str = "mao_pro"
    server_host: str = "0.0.0.0"
    server_port: int = 12393
    server_pid: Optional[int] = None
    started_at: Optional[str] = None
    history: list = field(default_factory=list)
    undo_stack: list = field(default_factory=list)
    redo_stack: list = field(default_factory=list)

    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now().isoformat()

    def save_snapshot(self) -> SessionSnapshot:
        snapshot = SessionSnapshot(
            timestamp=datetime.now().isoformat(),
            character=self.character,
            server_host=self.server_host,
            server_port=self.server_port,
        )
        return snapshot

    def push_undo(self):
        snapshot = self.save_snapshot()
        self.redo_stack.clear()
        self.undo_stack.append(snapshot)
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)

    def undo(self) -> Optional[SessionSnapshot]:
        if len(self.undo_stack) < 2:
            return None
        current = self.save_snapshot()
        self.redo_stack.append(current)
        self.undo_stack.pop()
        snapshot = self.undo_stack[-1]
        self.character = snapshot.character
        self.server_host = snapshot.server_host
        self.server_port = snapshot.server_port
        return snapshot

    def redo(self) -> Optional[SessionSnapshot]:
        if not self.redo_stack:
            return None
        current = self.save_snapshot()
        self.undo_stack.append(current)
        snapshot = self.redo_stack.pop()
        self.character = snapshot.character
        self.server_host = snapshot.server_host
        self.server_port = snapshot.server_port
        return snapshot

    def to_dict(self) -> dict:
        return {
            "project_path": str(self.project_path),
            "character": self.character,
            "server_host": self.server_host,
            "server_port": self.server_port,
            "server_pid": self.server_pid,
            "started_at": self.started_at,
            "history": self.history,
            "undo_levels": len(self.undo_stack),
            "redo_levels": len(self.redo_stack),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return cls(
            project_path=Path(data["project_path"]),
            character=data.get("character", "mao_pro"),
            server_host=data.get("server_host", "0.0.0.0"),
            server_port=data.get("server_port", 12393),
            server_pid=data.get("server_pid"),
            started_at=data.get("started_at"),
            history=data.get("history", []),
        )


def create_session(project_path: Path, **kwargs) -> Session:
    return Session(project_path=project_path, **kwargs)
