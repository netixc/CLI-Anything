# Agent-Avatar CLI

Command-line interface for Agent-Avatar - a voice-interactive AI companion with Live2D avatar support.

## Installation

```bash
cd agent-harness
pip install -e .
```

## Usage

```bash
# Make the avatar speak (TTS only, no LLM)
cli-anything-agent-avatar speak "Hello!"

# Show help
cli-anything-agent-avatar --help

# JSON output
cli-anything-agent-avatar --json speak "Hello!"
```

## Commands

- `speak` - Make the avatar speak via TTS (no LLM needed)
- `server` - Server management (start, stop, status)
- `config` - Configuration management (show, validate)
- `character` - Character management (list, switch)
- `model` - Live2D model management (list)
- `conversation` - Conversation management (history, clear)
- `dev` - Development tools (lint, format)

## Requirements

- Python 3.10+
- Agent-Avatar server running
