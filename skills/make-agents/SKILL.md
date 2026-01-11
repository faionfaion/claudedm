---
name: make-agents
description: Creates, edits, updates, or modifies Claude Code custom agents (subagents). Use when user asks to create agent, edit agent, update agent, subagent. Triggers on "agent", "subagent", "autonomous worker".
user-invocable: true
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(rm:*), Bash(ls:*), Glob
---

# Creating or Updating Agents

**Communication with user: Ukrainian. Agent content: English.**

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create a new agent/subagent
- Edit/update/change/modify existing agent
- Fix or improve an agent
- Add functionality to an agent

**Trigger phrases:** "create agent", "edit agent", "subagent", "autonomous worker", "створи агента", "оновити агента"

---

## Agents vs Skills vs Commands

| Type | Invocation | Context | Use Case |
|------|------------|---------|----------|
| **Agent** | Explicit or auto-delegated | Isolated (own window) | Autonomous workers, parallel tasks |
| **Skill** | Auto-triggered by context | Shared | Knowledge packages, procedures |
| **Command** | Manual `/invoke` | Shared | Quick actions with arguments |

**Analogy:** Skills = recipes, Agents = specialized coworkers

---

## Agent File Format

```markdown
---
name: agent-name
description: Action-oriented description for auto-delegation
model: sonnet                    # sonnet, opus, haiku, inherit
tools: [Read, Write, Bash, Grep] # Tool whitelist (least privilege)
skills: [skill-name]             # Optional skills to load
color: "#2F54EB"                 # UI color
version: "1.0.0"
disable-model-invocation: false  # true = only manual /agent-name
permissionMode: default          # default, acceptEdits, bypassPermissions
---

# Agent System Prompt

Instructions for the agent...
```

---

## Frontmatter Fields

**Required:**
- `name` - unique identifier
- `description` - what agent does (critical for auto-delegation)

**Model & Tools:**
- `model` - sonnet (default), opus, haiku, inherit
- `tools` - whitelist: `[Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Task]`
- `disallowedTools` - blacklist (alternative to whitelist)
- `skills` - skills to load in agent context

**Visibility:**
- `disable-model-invocation: true` - only callable via `/agent-name`
- `mode: true` - mark as mode command

**Permissions:**
- `permissionMode`:
  - `default` - ask for each tool
  - `acceptEdits` - auto-accept file edits
  - `bypassPermissions` - no prompts (dangerous)

**UI:**
- `color` - CSS color for identification
- `version` - version string

**Hooks:**
- `pre-hook` - script before agent runs
- `post-hook` - script after agent finishes

---

## Agent Locations

- Personal: `~/.claude/agents/agent-name.md`
- Project: `.claude/agents/agent-name.md`

Project overrides personal with same name.

---

## Best Practices

**Design:**
- One clear goal per agent
- Action-oriented descriptions for auto-delegation
- Scope tools per agent (least privilege)

**Tool Scoping Examples:**
- Research agent: `[Read, Glob, Grep, WebSearch]`
- Implementation agent: `[Read, Write, Edit, Bash]`
- Documentation agent: `[Read, Write, Glob]`

**Context:**
- Each agent has isolated context window
- Prevents context pollution between tasks
- Enables parallel execution

---

## Parallel Execution Pattern

```
Main Agent
├── Agent A (module 1) ─┐
├── Agent B (module 2) ─┼─ parallel
└── Agent C (module 3) ─┘
```

Spawn via Task tool with `subagent_type`.

---

## Pipeline Pattern

```
spec-writer → architect-review → implementer → tester
```

Each stage has focused context.

---

## Creation Process

1. Ask: purpose, tools needed, when to delegate
2. Create file: `~/.claude/agents/agent-name.md`
3. Write frontmatter with minimal tools
4. Write clear system prompt
5. Test with `/agent-name`

---

## Examples

**Research Agent:**
```markdown
---
name: researcher
description: Researches codebase and documentation. Use when need to understand code structure or find implementations.
model: haiku
tools: [Read, Glob, Grep, WebFetch]
---

# Research Agent

Research the codebase thoroughly before answering.
Use Grep to find patterns, Glob to find files.
Report findings in structured format.
```

**Implementation Agent:**
```markdown
---
name: implementer
description: Implements features and fixes bugs. Use when code changes are needed.
model: sonnet
tools: [Read, Write, Edit, Bash, Grep, Glob]
permissionMode: acceptEdits
---

# Implementation Agent

Implement the requested changes following project conventions.
Run tests after changes.
Commit with descriptive message.
```

---

## Troubleshooting

- Agent not auto-delegating → improve description keywords
- Tools not working → check tools whitelist
- Context issues → each agent has isolated context
- Permission errors → check permissionMode

---

## Self-Updating

This skill can update itself. To update:
1. Edit `~/.claude/claudedm/skills/make-agents/SKILL.md`
2. Sync: `cp -r ~/.claude/claudedm/skills/make-agents ~/.claude/skills/`
3. Changes apply immediately (hot-reload)

---

## Documentation

- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Agent SDK Quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)
- [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Awesome Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
