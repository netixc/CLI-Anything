# Agent-Avatar CLI Harness Specification

## Overview

Agent-Avatar is a voice-interactive AI companion with Live2D avatar support. It features:
- Real-time voice conversations with LLM models
- Visual perception (camera, screen, screenshots)
- Live2D character animations
- Modular AI engine architecture (LLM, ASR, TTS, VAD)

## Backend Analysis

### Core Engine
- **Framework**: FastAPI with WebSocket server (`run_server.py`)
- **Service Context**: Dependency injection container managing all engines
- **Protocol**: WebSocket for real-time bidirectional communication

### Data Model
- **Configuration**: YAML files (`conf.yaml`, `characters/*.yaml`)
- **Chat History**: JSON files in `chat_history/`
- **Live2D Models**: `.model3.json` + assets in `live2d-models/`
- **Cache**: Audio files, temporary data in `cache/`

### Existing CLI Tools
- `uv run run_server.py` - Main server entry point
- `uv run upgrade.py` - Project update utility
- `ruff check/format` - Code quality tools

## CLI Architecture Design

### Command Groups

1. **Server Management** (`server`)
   - `start` - Start the WebSocket server
   - `stop` - Stop the running server
   - `status` - Check server status
   - `restart` - Restart the server

2. **Configuration** (`config`)
   - `show` - Display current configuration
   - `validate` - Validate configuration files
   - `set` - Update configuration values
   - `character list` - List available characters
   - `character switch` - Switch active character

3. **Character Management** (`character`)
   - `list` - List all characters
   - `info` - Show character details
   - `create` - Create new character
   - `delete` - Delete a character

4. **Model Management** (`model`)
   - `list` - List available Live2D models
   - `info` - Show model details
   - `expression` - Trigger expression
   - `motion` - Play motion

5. **Conversation** (`conversation`)
   - `history` - Show chat history
   - `clear` - Clear chat history
   - `export` - Export conversation

6. **Development** (`dev`)
   - `lint` - Run code linter
   - `format` - Format code
   - `update` - Update project

### State Model

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 12393,
    "running": false,
    "pid": null
  },
  "character": {
    "active": "mao_pro",
    "config_path": "characters/mao_pro.yaml"
  },
  "session": {
    "started_at": null,
    "conversations": []
  }
}
```

### Output Formats
- Human-readable: Tables, colors, formatted text
- Machine-readable: JSON via `--json` flag

## Implementation Patterns

### Server Backend Integration
The CLI wraps the actual `run_server.py` using subprocess:
```python
def start_server(host, port, verbose):
    subprocess.run(["uv", "run", "run_server.py", "--verbose" if verbose else ""])
```

### Configuration Manipulation
Uses ruamel.yaml to safely edit YAML configs:
```python
from ruamel.yaml import YAML
yaml = YAML()
with open("conf.yaml") as f:
    config = yaml.load(f)
```

## Directory Structure

```
agent_avatar/
├── core/
│   ├── __init__.py
│   ├── server.py      # Server management
│   ├── config.py      # Configuration handling
│   ├── character.py   # Character management
│   ├── model.py       # Live2D model control
│   └── session.py     # Session state
├── utils/
│   ├── __init__.py
│   ├── agent_avatar_backend.py  # Wraps run_server.py
│   └── repl_skin.py   # REPL interface
├── tests/
│   ├── TEST.md
│   ├── test_core.py
│   └── test_full_e2e.py
└── skills/
    └── SKILL.md
```
