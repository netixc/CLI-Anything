---
name: "cli-anything-agent-avatar"
description: "CLI harness for Agent-Avatar - voice-interactive AI companion with Live2D avatar"
---

# Agent-Avatar CLI Skill

Command-line interface for Agent-Avatar - a voice-interactive AI companion with Live2D avatar support.

## Installation

```bash
cd agent-harness
pip install -e .
```

## Command Groups

### server
Server management commands.

- `start` - Start the Agent-Avatar server
- `stop` - Stop the running server
- `status` - Check server status

### config
Configuration management.

- `show` - Display current configuration
- `validate` - Validate configuration files

### character
Character management.

- `list` - List available characters
- `switch` - Switch active character

### model
Live2D model management.

- `list` - List available Live2D models

### conversation
Conversation management.

- `history` - Show chat history
- `clear` - Clear chat history

### dev
Development commands.

- `lint` - Run code linter
- `format` - Format code

## Usage Examples

```bash
# Make the avatar speak (TTS only, no LLM)
cli-anything-agent-avatar speak "Hello!"

# Show help
cli-anything-agent-avatar --help

# Start server
cli-anything-agent-avatar server start --host 0.0.0.0 --port 12393

# List characters
cli-anything-agent-avatar character list

# Switch character
cli-anything-agent-avatar character switch miku

# Show configuration
cli-anything-agent-avatar config show

# JSON output for scripting
cli-anything-agent-avatar --json speak "Hello!"
```

## Agent-Specific Notes

- Use `--json` flag for machine-readable output
- The CLI wraps the actual `run_server.py` via subprocess
- Configuration persists in `.cli-state.json`
- All paths are resolved relative to the project directory
