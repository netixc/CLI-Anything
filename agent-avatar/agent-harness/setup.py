from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-agent-avatar",
    version="1.0.0",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
        "ruamel-yaml>=0.18.0",
        "websockets>=10.0.0",
        "playsound>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-agent-avatar=cli_anything.agent_avatar.agent_avatar_cli:main",
        ],
    },
    python_requires=">=3.10",
    package_data={
        "cli_anything.agent_avatar": ["skills/*.md", "utils/repl_skin.py"],
    },
)
