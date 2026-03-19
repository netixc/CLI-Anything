import click
import sys
import json
import asyncio
import subprocess
import websockets
from pathlib import Path
from typing import Optional

from cli_anything.agent_avatar.core.project import create_project, load_project
from cli_anything.agent_avatar.core.session import create_session
from cli_anything.agent_avatar.utils import agent_avatar_backend as backend


@click.group(invoke_without_command=True)
@click.option("--project", type=click.Path(exists=True), help="Project path")
@click.option("--json", "output_json", is_flag=True, help="JSON output")
@click.pass_context
def cli(ctx, project, output_json):
    ctx.ensure_object(dict)
    project_path = Path(project) if project else Path.cwd()
    ctx.obj["project"] = create_project(project_path)
    ctx.obj["session"] = create_session(project_path)
    ctx.obj["output_json"] = output_json

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl, project_path=project_path)


@cli.group()
def server():
    """Server management commands"""
    pass


@server.command()
@click.option("--verbose", is_flag=True, help="Verbose logging")
@click.pass_context
def start(ctx, verbose):
    """Start the Agent-Avatar server (Docker)"""
    project = ctx.obj["project"]
    result = backend.start_server(
        source_path=project.source_path,
        verbose=verbose,
    )
    if ctx.obj["output_json"]:
        click.echo(result)
    else:
        if result.get("status") == "started":
            click.echo("Server started (Docker)")
        else:
            click.echo(f"Error: {result.get('message', 'unknown error')}")


@server.command()
@click.pass_context
def stop(ctx):
    """Stop the Agent-Avatar server (Docker)"""
    project = ctx.obj["project"]
    result = backend.stop_server(source_path=project.source_path)
    if ctx.obj["output_json"]:
        click.echo(result)
    else:
        if result["status"] == "stopped":
            click.echo("Server stopped")
        else:
            click.echo(f"Error: {result.get('message', 'unknown error')}")


@server.command()
@click.pass_context
def status(ctx):
    """Check server status"""
    project = ctx.obj["project"]
    result = backend.get_server_status(source_path=project.source_path)
    if ctx.obj["output_json"]:
        click.echo(result)
    else:
        running = result.get("running", False)
        status_str = "running" if running else "stopped"
        click.echo(f"Server: {status_str}")


@cli.group()
def config():
    """Configuration management"""
    pass


@config.command()
@click.pass_context
def show(ctx):
    """Show current configuration"""
    project = ctx.obj["project"]
    info = project.get_info()
    if ctx.obj["output_json"]:
        click.echo(info)
    else:
        click.echo(f"Source: {info['source_path']}")
        click.echo(f"Character: {info['character_active']}")
        click.echo(f"Server: {info['server_host']}:{info['server_port']}")


@config.command()
@click.pass_context
def validate(ctx):
    """Validate configuration"""
    project = ctx.obj["project"]
    result = backend.validate_config(project.config_path)
    if ctx.obj["output_json"]:
        click.echo(result)
    else:
        if result.get("valid"):
            click.echo("Configuration is valid")
        else:
            click.echo(f"Configuration error: {result.get('error')}", err=True)


@cli.group()
def character():
    """Character management"""
    pass


@character.command()
@click.pass_context
def list(ctx):
    """List available characters"""
    project = ctx.obj["project"]
    characters = backend.list_characters(project.source_path)
    if ctx.obj["output_json"]:
        click.echo({"characters": characters})
    else:
        for char in characters:
            active = "[active]" if char == project.character_active else ""
            click.echo(f"  {char} {active}")


@character.command()
@click.argument("name")
@click.pass_context
def switch(ctx, name):
    """Switch active character"""
    project = ctx.obj["project"]
    result = project.set_character(name)
    if ctx.obj["output_json"]:
        click.echo(result)
    else:
        click.echo(f"Switched to character: {name}")


@cli.group()
def model():
    """Live2D model management"""
    pass


@model.command()
@click.pass_context
def list(ctx):
    """List available Live2D models"""
    project = ctx.obj["project"]
    models = backend.list_live2d_models(project.source_path)
    if ctx.obj["output_json"]:
        click.echo({"models": models})
    else:
        for m in models:
            click.echo(f"  {m}")


@cli.group()
def conversation():
    """Conversation management"""
    pass


@conversation.command()
@click.option("--limit", type=int, default=10, help="Number of recent conversations")
@click.pass_context
def history(ctx, limit):
    """Show chat history"""
    project = ctx.obj["project"]
    history_dir = project.source_path / "chat_history"
    if not history_dir.exists():
        if ctx.obj["output_json"]:
            click.echo({"history": []})
        else:
            click.echo("No chat history found")
        return

    history_files = sorted(
        history_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True
    )
    histories = []
    for f in history_files[:limit]:
        histories.append({"file": f.name, "path": str(f)})

    if ctx.obj["output_json"]:
        click.echo({"history": histories})
    else:
        for h in histories:
            click.echo(f"  {h['file']}")


@conversation.command()
@click.pass_context
def clear(ctx):
    """Clear chat history"""
    project = ctx.obj["project"]
    history_dir = project.source_path / "chat_history"
    if history_dir.exists():
        for f in history_dir.glob("*.json"):
            f.unlink()
    click.echo("Chat history cleared")


@cli.group()
def dev():
    """Development commands"""
    pass


@dev.command()
@click.pass_context
def lint(ctx):
    """Run code linter"""
    project = ctx.obj["project"]
    try:
        result = subprocess.run(
            ["ruff", "check", str(project.source_path)],
            capture_output=True,
            text=True,
        )
        click.echo(result.stdout or "No issues found")
        if result.returncode != 0:
            click.echo(result.stderr, err=True)
    except FileNotFoundError:
        click.echo("ruff not found. Install with: uv pip install ruff", err=True)


@dev.command()
@click.pass_context
def format(ctx):
    """Format code"""
    project = ctx.obj["project"]
    try:
        result = subprocess.run(
            ["ruff", "format", str(project.source_path)],
            capture_output=True,
            text=True,
        )
        click.echo(result.stdout or "Code formatted")
    except FileNotFoundError:
        click.echo("ruff not found. Install with: uv pip install ruff", err=True)


@cli.command()
@click.pass_context
def info(ctx):
    """Show project information"""
    project = ctx.obj["project"]
    info = project.get_info()
    if ctx.obj["output_json"]:
        click.echo(info)
    else:
        click.echo("Agent-Avatar CLI")
        click.echo(f"  Version: 1.0.0")
        click.echo(f"  Source: {info['source_path']}")
        click.echo(f"  Config: {info['config_path']}")
        click.echo(f"  Character: {info['character_active']}")
        click.echo(f"  Server: {info['server_host']}:{info['server_port']}")


@cli.command()
@click.pass_context
def status(ctx):
    """Show session status"""
    session = ctx.obj["session"]
    data = session.to_dict()
    if ctx.obj["output_json"]:
        click.echo(data)
    else:
        click.echo("Session Status")
        click.echo(f"  Started: {data['started_at']}")
        click.echo(f"  Character: {data['character']}")
        click.echo(f"  Undo levels: {data['undo_levels']}")
        click.echo(f"  Redo levels: {data['redo_levels']}")


async def _speak_async(host: str, port: int, text: str, timeout: int = 60):
    """Send text directly to TTS engine via WebSocket (no LLM)."""
    uri = f"ws://{host}:{port}/client-ws"
    ws = None
    try:
        ws = await asyncio.wait_for(websockets.connect(uri), timeout=timeout)
        await asyncio.sleep(1)
        await ws.send(json.dumps({"type": "direct-tts", "text": text}))
        await asyncio.sleep(2)
        return {"success": True, "sent": True, "text": text}
    except asyncio.TimeoutError:
        return {"success": False, "error": "Timeout connecting to server"}
    except ConnectionRefusedError:
        return {
            "success": False,
            "error": f"Connection refused. Is server running at {uri}?",
        }
    except websockets.exceptions.ConnectionClosed as e:
        return {"success": True, "sent": True, "note": f"Connection closed: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@cli.command()
@click.argument("text")
@click.option("--host", default="0.0.0.0", help="Server host")
@click.option("--port", default=12393, type=int, help="Server port")
@click.pass_context
def speak(ctx, text, host, port):
    """Send text directly to TTS (no LLM needed). Avatar speaks the text."""
    result = asyncio.run(_speak_async(host, port, text))
    if ctx.obj["output_json"]:
        click.echo(result)
    else:
        if result["success"]:
            click.echo(f"Speaking: {text}")
        else:
            click.echo(f"Error: {result.get('error')}", err=True)


@click.command()
@click.option("--project-path", type=click.Path(exists=True), help="Project path")
@click.pass_context
def repl(ctx, project_path):
    """Enter REPL mode"""
    from cli_anything.agent_avatar.utils.repl_skin import ReplSkin

    path = Path(project_path) if project_path else Path.cwd()
    skin = ReplSkin("agent-avatar", version="1.0.0")
    skin.print_banner()

    click.echo("Agent-Avatar REPL - Type 'help' for commands, 'exit' to quit")

    while True:
        try:
            user_input = click.prompt("\nagent-avatar", type=str, default="")
            if user_input.lower() in ("exit", "quit"):
                break
            if user_input.lower() == "help":
                click.echo(
                    "Available commands: info, status, server start, server stop, config show, character list"
                )
            elif user_input.lower() == "info":
                ctx.invoke(info)
            elif user_input.lower() == "status":
                ctx.invoke(status)
        except (KeyboardInterrupt, EOFError):
            break

    skin.print_goodbye()


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
