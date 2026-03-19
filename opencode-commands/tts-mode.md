---
description: Enable TTS mode - speak all responses via Agent-Avatar
subtask: true
---

# Enable TTS Mode

When this command is invoked, immediately speak a confirmation message using the Agent-Avatar CLI:

```
source /root/projectx/Agent-Avatar/agent-harness/.venv/bin/activate && cli-anything-agent-avatar speak "TTS mode enabled. All responses will be spoken."
```

Then follow these rules for ALL future responses in this session:

1. **Every response** must use the bash speak command
2. **NO text after** the speak command - the speak command IS the response
3. **NO markdown, NO bullet points, NO explanation**
4. **NO mentioning tts or tool is used**

Example correct response: use bash tool or tts wont work 
```
cli-anything-agent-avatar speak "Understood. TTS mode active."
```

Example WRONG response (do NOT do this):
```
cli-anything-agent-avatar speak "Done!"

This command does X, Y, Z...
```
