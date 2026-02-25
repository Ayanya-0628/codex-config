---
name: continuous-learning
description: Automatically extract reusable patterns from OpenCode sessions, with emphasis on user corrections and user preference persistence.
---

# Continuous Learning Skill

Automatically evaluates sessions to persist:
- user corrections (what was changed)
- user preferences (how to respond and format)
- repeatable workflows (what to always do)

## How It Works

This skill is designed to run at session end and maintain durable memory files:

1. **Session Evaluation**: checks if session length is enough.
2. **Preference Extraction**: captures correction/preference signals.
3. **Persistence**:
   - learned notes -> `~/.config/opencode/skills/learned/`
   - user preference ledger -> `~/.config/opencode/skills/learned/user-preferences.md`

## Configuration

Edit `config.json` to customize:

```json
{
  "min_session_length": 6,
  "extraction_threshold": "low",
  "auto_approve": true,
  "learned_skills_path": "~/.config/opencode/skills/learned/",
  "preferences_path": "~/.config/opencode/skills/learned/user-preferences.md",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "user_preferences",
    "style_preferences",
    "progress_protocol",
    "project_specific"
  ]
}
```

## Preference Signals To Capture

Track these when users correct the assistant:

- must/always/never constraints
- output format preferences
- progress reporting cadence
- file naming conventions
- verification expectations

## OpenCode Use

When active, this skill should append findings (never overwrite):

- `~/.config/opencode/skills/learned/user-preferences.md`
- task-specific notes in `~/.config/opencode/skills/learned/*.md`

Suggested heading format:

```markdown
## YYYY-MM-DD HH:MM
- Context:
- User correction:
- Persistent preference:
- Action rule:
```

## Non-Negotiable

If a user repeats a correction more than once, convert it into a durable rule and apply by default in future sessions.
