---
name: make-tasks
description: Creates, edits, updates, or modifies task files (TASK_*.md). Use when user asks to create task, edit task, update task, change task, modify task, add task to queue. Triggers on "task", "TASK_", "таска", "завдання".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*), Bash(ls:*), Bash(date:*), Task
---

# Creating or Updating Tasks

**Communication with user: Ukrainian. Task content: Ukrainian.**

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create a new task (TASK_*.md)
- Edit/update/change/modify existing task
- Add task to the queue
- Fix or improve a task file

**Trigger phrases:** "create task", "edit task", "update task", "modify task", "add task", "нова таска", "створити таску", "змінити таску", "оновити таску", "додати завдання"

---

Creates well-structured task files by delegating research and writing to a subagent.

---

## Input: Arguments Format

When invoked from `/maketasks` or directly:

```
TASK CREATION REQUEST:
- Title: [Short title for the task]
- Summary: [One-line business value description]
- Complexity: simple/normal/complex
- Description: [What needs to be done and why]
- Technical notes: [Optional hints]
- Out of scope: [What NOT to do]
- Depends on: [TASK_XXX if any]
```

---

## Orchestrator Workflow

### STEP 1: Parse Input

If structured input is provided, parse it. If invoked directly, ask the user what task to create.

### STEP 2: Get Next Task Number

Use Bash tool to get the date and find the last task number:

```bash
date "+%Y-%m-%d"
ls /home/moskalyuk_ruslan/aitasks/todo/ /home/moskalyuk_ruslan/aitasks/in_progress/ /home/moskalyuk_ruslan/aitasks/done/ 2>/dev/null | grep -oE 'TASK_[0-9]+' | sort -t_ -k2 -n | tail -1
```

If last is TASK_260, next is TASK_261.

### STEP 3: Generate File Name

**Format:** `TASK_XXX_short_descriptive_name.md`

**Rules:**
- Lowercase with underscores
- 3-5 descriptive words
- Example: `TASK_261_add_validation_report.md`

### STEP 4: Launch Subagent

Use the **Task tool** to launch a subagent with the prompt template below. Pass only basic information; the subagent performs its own research.

---

## Subagent Prompt Template

```markdown
# Task Creation Assignment

**Communication in Ukrainian.**

## Your Mission

Create a complete, well-structured task file:
1. Research the codebase (related files, patterns, existing code)
2. Write the task file with full context
3. Save to the todo directory

## Task Details

- **Task Number:** TASK_{NUMBER}
- **File Name:** {TASK_FILENAME}
- **File Path:** /home/moskalyuk_ruslan/aitasks/todo/{TASK_FILENAME}
- **Created Date:** {DATE}

### Input from Orchestrator

**Title:** {TITLE}
**Summary:** {SUMMARY}
**Complexity:** {COMPLEXITY}
**Description:** {DESCRIPTION}
**Technical notes:** {TECHNICAL_NOTES}
**Out of scope:** {OUT_OF_SCOPE}
**Depends on:** {DEPENDS_ON}

## Project Context

- **Project:** E-Pass electronic transport payment system
- **Working directory:** /home/moskalyuk_ruslan/epass
- **Tech stack:** Django 4.2+, Python 3.11+, PostgreSQL, pytest

---

## Execution Phases

### Phase 1: Deep Research

Research the codebase before writing the task.

1. **Find related files** using Glob and Grep tools
2. **Read domain documentation** (app/CLAUDE.md, domain-specific CLAUDE.md files)
3. **Find existing patterns** - how similar features are implemented
4. **Check existing tasks** in todo/done directories

Document findings: related files, existing patterns, similar implementations.

### Phase 2: Enrich Task Content

Based on research:
1. Define concrete, achievable Goals
2. Add Related Files with descriptions
3. Write measurable Acceptance Criteria
4. Add Technical Notes with implementation hints
5. Define Out of Scope items

### Phase 3: Write Task File

Use the Write tool to create the task file at the specified path.

### Phase 4: Verify

Use Bash tool to verify the file was created and check first 6 lines.

---

## Task File Template

# TASK_XXX: Short Descriptive Title
<!-- SUMMARY: One sentence describing what and why -->
## Complexity: simple/normal/complex
## Created: YYYY-MM-DD
## Project: /home/moskalyuk_ruslan/epass

## Description
Clear explanation of what needs to be done.

**Business value:**
- Why this matters for the business
- Who benefits from this

## Context
- **Related files:**
  - path/to/file.py - description (discovered via research)
  - path/to/other.py - description
- **Existing patterns:** how similar features are implemented
- **Related tasks:** TASK_XXX (if dependencies exist)

## Goals
1. First specific goal
2. Second specific goal
3. Third specific goal

## Acceptance Criteria
- [ ] Criterion 1 - specific, measurable
- [ ] Criterion 2 - specific, measurable
- [ ] All tests pass (make test-dev)
- [ ] Code follows project conventions

## Technical Notes
Implementation hints from research:
- Suggested approach based on existing patterns
- Libraries/patterns to use
- Edge cases to consider

## Out of Scope
What this task explicitly does NOT include:
- Item 1
- Item 2

## Subtasks
<!-- To be filled by executor -->
- [ ] 01. TBD

## Implementation
<!-- To be filled by executor -->

## Summary
<!-- To be filled after completion -->

---

## Output Format

Return structured result:

STATUS: SUCCESS | FAILED
TASK_FILE: TASK_XXX_name.md
PATH: /home/moskalyuk_ruslan/aitasks/todo/TASK_XXX_name.md

RESEARCH_FINDINGS:
- Related files: N files discovered
- Patterns found: pattern 1, pattern 2
- Similar tasks: TASK_YYY

KEY_CRITERIA:
- Criterion 1
- Criterion 2

If failed:

STATUS: FAILED
REASON: description of the problem
```

---

## First 6 Lines Rule (CRITICAL)

```markdown
# TASK_XXX: Short Descriptive Title
<!-- SUMMARY: One sentence (business value) -->
## Complexity: simple/normal/complex
## Created: YYYY-MM-DD
## Project: /path/to/project
```

**Why:** `head -6 TASK_*.md` allows quick scanning of all tasks.

---

## STEP 5: Process Result

### SUCCESS:

Report to user:
- Task created: TASK_XXX_name.md
- Complexity: {complexity}
- Related files: N found
- Key criteria: criterion 1, criterion 2
- Path: /home/moskalyuk_ruslan/aitasks/todo/TASK_XXX_name.md

### FAILED:

Report to user:
- Task creation failed
- Reason: {reason from subagent}

---

## Integration with /maketasks

When called by `/maketasks` orchestrator:

1. `/maketasks` plans multiple tasks
2. Calls this skill with structured input for EACH task
3. This skill launches subagent for research and writing
4. Returns success or failure
5. `/maketasks` continues with next task

**Important:**
- Each task = separate subagent call
- Subagent has fresh context for each task
- Deep research for each task individually

---

## Failed Attempts

- **Task number collision** - race condition → re-check numbers before writing
- **Empty research results** - wrong paths → verify project exists, use broader patterns
- **Missing domain context** - no CLAUDE.md → proceed with code analysis
- **File write failure** - permission issues → verify directory is writable
- **Subagent timeout** - complex research → break into smaller scope

---

## Sources

- Claude Code CLI documentation: https://docs.anthropic.com/en/docs/claude-code
- Task tool reference: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Glob and Grep tools: https://docs.anthropic.com/en/docs/claude-code/tools
