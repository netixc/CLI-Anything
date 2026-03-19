import pytest
import json
import tempfile
from pathlib import Path

from cli_anything.agent_avatar.core.project import Project, create_project, load_project
from cli_anything.agent_avatar.core.session import Session, create_session


class TestProject:
    def test_create_project_with_defaults(self, tmp_path):
        project = create_project(tmp_path)
        assert project.source_path == tmp_path
        assert project.character_active == "mao_pro"
        assert project.server_host == "0.0.0.0"
        assert project.server_port == 12393

    def test_project_saves_state(self, tmp_path):
        project = create_project(tmp_path)
        project.set_character("new_character")
        assert project.character_active == "new_character"
        assert tmp_path.joinpath(".cli-state.json").exists()

    def test_project_loads_existing_state(self, tmp_path):
        state_file = tmp_path / ".cli-state.json"
        state_file.write_text(json.dumps({"character_active": "test_char"}))
        project = create_project(tmp_path)
        assert project.character_active == "test_char"

    def test_set_character(self, tmp_path):
        project = create_project(tmp_path)
        result = project.set_character("miku")
        assert result["character"] == "miku"
        assert project.character_active == "miku"

    def test_set_server_config(self, tmp_path):
        project = create_project(tmp_path)
        result = project.set_server_config("127.0.0.1", 8080)
        assert result["host"] == "127.0.0.1"
        assert result["port"] == 8080
        assert project.server_host == "127.0.0.1"
        assert project.server_port == 8080

    def test_get_info(self, tmp_path):
        project = create_project(tmp_path)
        info = project.get_info()
        assert "source_path" in info
        assert "character_active" in info
        assert "server_host" in info
        assert "server_port" in info


class TestSession:
    def test_create_session_defaults(self, tmp_path):
        session = create_session(tmp_path)
        assert session.project_path == tmp_path
        assert session.character == "mao_pro"
        assert session.server_port == 12393
        assert session.started_at is not None

    def test_undo_stack_max_50(self, tmp_path):
        session = create_session(tmp_path)
        for i in range(60):
            session.push_undo()
        assert len(session.undo_stack) == 50

    def test_undo_restores_state(self, tmp_path):
        session = create_session(tmp_path)
        session.character = "char1"
        session.push_undo()
        session.character = "char2"
        session.push_undo()
        session.undo()
        assert session.character == "char1"

    def test_redo_restores_state(self, tmp_path):
        session = create_session(tmp_path)
        session.character = "char1"
        session.push_undo()
        session.character = "char2"
        session.undo()
        session.redo()
        assert session.character == "char2"

    def test_to_dict(self, tmp_path):
        session = create_session(tmp_path)
        data = session.to_dict()
        assert "project_path" in data
        assert "character" in data
        assert "undo_levels" in data
        assert "redo_levels" in data

    def test_from_dict(self, tmp_path):
        data = {
            "project_path": str(tmp_path),
            "character": "test_char",
            "server_host": "localhost",
            "server_port": 9999,
        }
        session = Session.from_dict(data)
        assert session.character == "test_char"
        assert session.server_host == "localhost"
        assert session.server_port == 9999


class TestBackendHelpers:
    def test_list_characters_empty(self, tmp_path):
        from cli_anything.agent_avatar.utils.agent_avatar_backend import list_characters

        chars = list_characters(tmp_path)
        assert chars == []

    def test_list_characters_with_files(self, tmp_path):
        from cli_anything.agent_avatar.utils.agent_avatar_backend import list_characters

        chars_dir = tmp_path / "characters"
        chars_dir.mkdir()
        (chars_dir / "miku.yaml").touch()
        (chars_dir / "luka.yaml").touch()
        chars = list_characters(tmp_path)
        assert "miku" in chars
        assert "luka" in chars

    def test_list_live2d_models_empty(self, tmp_path):
        from cli_anything.agent_avatar.utils.agent_avatar_backend import (
            list_live2d_models,
        )

        models = list_live2d_models(tmp_path)
        assert models == []

    def test_list_live2d_models_with_files(self, tmp_path):
        from cli_anything.agent_avatar.utils.agent_avatar_backend import (
            list_live2d_models,
        )

        models_dir = tmp_path / "live2d-models"
        models_dir.mkdir()
        (models_dir / "miku.model3.json").touch()
        models = list_live2d_models(tmp_path)
        assert "miku.model3" in models
