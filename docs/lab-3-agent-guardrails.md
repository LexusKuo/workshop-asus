# Lab 3 - Repository guardrails

**Time:** 15 minutes  
**Goal:** See how instructions, skills, and hooks give an agent repeatable project context
and deterministic validation.

## 1. Inspect the three guardrail layers

| Layer | File | Purpose |
|---|---|---|
| Repository instructions | `.github/copilot-instructions.md` | Always-on project context, commands, and non-negotiable rules |
| Agent Skill | `.github/skills/secure-fastapi-endpoint/SKILL.md` | Reusable workflow loaded for relevant endpoint/security tasks |
| Hook | `.github/hooks/validate-on-stop.json` | Runs deterministic validation when the agent tries to stop |

Discuss why tests and linters belong in a hook while architecture and security guidance
belong in instructions or a skill.

## 2. Test the validation command

```bash
python scripts/validate.py --fast
```

Then test the hook handler with a sample event:

```bash
echo '{}' | python scripts/agent_stop_hook.py
```

A healthy repository returns:

```json
{"decision": "allow"}
```

## 3. Make a team-specific improvement

Choose one change:

1. Add an ASUS coding rule to `.github/copilot-instructions.md`.
2. Add a required review step to the secure endpoint skill.
3. Extend `scripts/validate.py` with an existing, fast project check.

Keep the rule concrete and verifiable. Avoid generic guidance such as "write high quality
code."

## 4. Prove the guardrail has an effect

Ask agent mode to make a small endpoint change. Check the transcript for:

- discovery of repository instructions
- use of the secure endpoint skill when relevant
- execution of the stop hook
- correction of a lint or test failure before the agent finishes

## Debrief

- Instructions guide model judgment.
- Skills package repeatable domain workflows.
- Hooks run deterministic automation and can force another agent turn.
- Human approval still owns architecture, product behavior, and risk acceptance.

