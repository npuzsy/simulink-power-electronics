# Companion Skills

Use this reference when the user asks about optional external skills that can
improve the agent workflow around this repository.

## Contents

- Installed Companion Skills
- Referencing External Skills
- Review Notes For This Repository

## Installed Companion Skills

### `using-superpowers`

Source: https://github.com/obra/superpowers/tree/main/skills/using-superpowers

Local install path:

```text
~/.codex/skills/using-superpowers
```

Install command:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo obra/superpowers \
  --path skills/using-superpowers
```

Purpose:

- improves skill-discovery discipline before starting work
- reminds agents to use relevant skills before ad hoc exploration
- provides Codex tool mappings for skills written with Claude Code tool names

Boundary:

- treat it as an optional companion process skill, not a hard dependency
- do not copy its instructions into this repository
- newly installed skills may require a Codex restart before native skill
  discovery sees them

## Referencing External Skills

Preferred pattern:

- reference external skills by name, source URL, and optional install command
- describe when they are useful and what they do not own
- keep the detailed workflow in the external skill
- avoid `@`-style eager file references or pasted full skill bodies
- do not make this skill fail if the companion skill is not installed

This matches the progressive-disclosure pattern used by Codex skills and the
cross-reference guidance from Superpowers skill-writing notes: keep the current
skill small, and load extra process guidance only when needed.

## Review Notes For This Repository

`using-superpowers` reinforces two rules already present here:

- check for relevant skills before starting a Simulink task
- keep `SKILL.md` as a router and move detailed guidance into references

No PE behavior should be delegated to `using-superpowers`; this repository still
owns power-electronics routing, model evidence standards, layout rules, and
validation expectations.
