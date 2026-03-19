# Agent-Avatar CLI Test Plan

## Test Inventory

- `test_core.py`: 15 unit tests planned
- `test_full_e2e.py`: 10 E2E tests planned

## Unit Test Plan

### test_project.py

| Function | Description | Tests |
|----------|-------------|-------|
| `Project.__init__` | Initialize project state | Loads existing state, creates default state |
| `Project._save_state` | Persist state to JSON | Writes correct JSON format |
| `Project.get_info` | Return project info | Returns all expected fields |
| `Project.set_character` | Update active character | Updates and persists |
| `Project.set_server_config` | Update server config | Updates host and port |
| `create_project` | Factory function | Returns Project instance |
| `load_project` | Load existing project | Uses cwd if no path |

### test_session.py

| Function | Description | Tests |
|----------|-------------|-------|
| `Session.__init__` | Initialize session | Sets defaults correctly |
| `Session.push_undo` | Save undo snapshot | Max 50 levels |
| `Session.undo` | Restore previous state | Returns snapshot |
| `Session.redo` | Restore next state | Returns snapshot |
| `Session.to_dict` | Serialize session | Contains all fields |
| `Session.from_dict` | Deserialize session | Reconstructs correctly |
| `create_session` | Factory function | Returns Session instance |

### test_backend.py

| Function | Description | Tests |
|----------|-------------|-------|
| `find_run_server` | Locate run_server.py | Returns path or raises |
| `find_uv` | Locate uv command | Returns path or raises |
| `list_characters` | List character files | Returns correct list |
| `list_live2d_models` | List model files | Returns correct list |

## E2E Test Plan

### test_config_workflow.py

| Test | Description |
|------|-------------|
| `test_config_show` | Run config show command |
| `test_config_validate` | Validate configuration file |
| `test_character_list` | List all characters |
| `test_model_list` | List all Live2D models |

### test_session_workflow.py

| Test | Description |
|------|-------------|
| `test_session_creation` | Create new session |
| `test_undo_redo_stack` | Test undo/redo functionality |
| `test_history_tracking` | Verify history updates |

## Realistic Workflow Scenarios

### Workflow 1: Server Management
1. Start server in background
2. Check status
3. Stop server

### Workflow 2: Character Switching
1. List available characters
2. Switch to new character
3. Verify state persisted

### Workflow 3: Configuration Update
1. Show current config
2. Update server port
3. Validate new config
4. Undo changes

---

## Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.10.18, pytest-9.0.2, pluggy-1.6.0
rootdir: /root/projectx/Agent-Avatar
collected 27 items

cli_anything/agent_avatar/tests/test_core.py::TestProject::test_create_project_with_defaults PASSED [  3%]
cli_anything/agent_avatar/tests/test_core.py::TestProject::test_project_saves_state PASSED [  7%]
cli_anything/agent_avatar/tests/test_core.py::TestProject::test_project_loads_existing_state PASSED [ 11%]
cli_anything/agent_avatar/tests/test_core.py::TestProject::test_set_character PASSED [ 14%]
cli_anything/agent_avatar/tests/test_core.py::TestProject::test_set_server_config PASSED [ 18%]
cli_anything/agent_avatar/tests/test_core.py::TestProject::test_get_info PASSED [ 22%]
cli_anything/agent_avatar/tests/test_core.py::TestSession::test_create_session_defaults PASSED [ 25%]
cli_anything/agent_avatar/tests/test_core.py::TestSession::test_undo_stack_max_50 PASSED [ 29%]
cli_anything/agent_avatar/tests/test_core.py::TestSession::test_undo_restores_state PASSED [ 33%]
cli_anything/agent_avatar/tests/test_core.py::TestSession::test_redo_restores_state PASSED [ 37%]
cli_anything/agent_avatar/tests/test_core.py::TestSession::test_to_dict PASSED [ 40%]
cli_anything/agent_avatar/tests/test_core.py::TestSession::test_from_dict PASSED [ 44%]
cli_anything/agent_avatar/tests/test_backend_helpers.py::TestBackendHelpers::test_list_characters_empty PASSED [ 48%]
cli_anything/agent_avatar/tests/test_core.py::TestBackendHelpers::test_list_characters_with_files PASSED [ 51%]
cli_anything/agent_avatar/tests/test_core.py::TestBackendHelpers::test_list_live2d_models_empty PASSED [ 55%]
cli_anything/agent_avatar/tests/test_core.py::TestBackendHelpers::test_list_live2d_models_with_files PASSED [ 59%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_help PASSED [ 62%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_info PASSED [ 66%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_status PASSED [ 70%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_config_show PASSED [ 74%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_character_list PASSED [ 77%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_model_list PASSED [ 81%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_json_output PASSED [ 85%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_conversation_history_empty PASSED [ 88%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestCLISubprocess::test_conversation_clear PASSED [ 92%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestConfigWorkflow::test_switch_character_workflow PASSED [ 96%]
cli_anything/agent_avatar/tests/test_full_e2e.py::TestConfigWorkflow::test_character_switch_persists PASSED [100%]

============================== 27 passed in 0.97s ==============================
```

## Summary

- **Total Tests**: 27
- **Pass Rate**: 100%
- **Execution Time**: ~1 second
- **Coverage**: Core modules, session management, backend helpers, CLI subprocess tests
