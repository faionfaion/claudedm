---
user-invocable: true
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

## SDD Framework Context

Цей скіл є частиною **Spec-Driven Development (SDD)** фреймворку.

**Філософія SDD:** "Intent is the source of truth" — специфікація є головним артефактом, код — лише її реалізація.

**Workflow:**
```
SPEC (Human) → DESIGN (AI) → TASKS (AI) → CODE (AI)
```

**Структура SDD:**
```
aidocs/sdd/{project}/
├── constitution.md           # Принципи проекту (стандарти, патерни)
└── features/{feature}/
    ├── spec.md               # ЩО і ЧОМУ (бізнес вимоги)
    ├── design.md             # ЯК (технічна реалізація)
    └── tasks/                # Задачі
        ├── todo/             # Очікують виконання
        ├── in_progress/      # В роботі (макс 1)
        └── done/             # Виконані
```

**Два типи тасків:**
1. **Global tasks** — `aitasks/` (загальні задачі проекту)
2. **Feature tasks** — `aidocs/sdd/{project}/features/{feature}/tasks/` (задачі для конкретної фічі)

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

### STEP 2: Get Next Task Number (CRITICAL!)

**Нумерація ПОВИННА бути послідовною!** Не пропускай номери.

#### Для Global Tasks:

```bash
date "+%Y-%m-%d"
ls aitasks/todo/ aitasks/in_progress/ aitasks/done/ 2>/dev/null | grep -oE 'TASK_[0-9]+' | sort -t_ -k2 -n | tail -1
```

**Приклад:** Якщо останній `TASK_260`, наступний `TASK_261`.

#### Для Feature Tasks (SDD):

```bash
date "+%Y-%m-%d"
FEATURE_PATH="aidocs/sdd/{project}/features/{feature}/tasks"
ls ${FEATURE_PATH}/todo/ ${FEATURE_PATH}/in_progress/ ${FEATURE_PATH}/done/ 2>/dev/null | grep -oE 'TASK_[0-9]+' | sort -t_ -k2 -n | tail -1
```

**Приклад:** Якщо в фічі останній `TASK_005`, наступний `TASK_006`.

#### Правила нумерації:

1. **Global tasks**: Глобальна нумерація (TASK_001...TASK_999)
2. **Feature tasks**: Локальна нумерація в межах фічі (TASK_001...TASK_NNN)
3. **Формат номера**: Завжди 3 цифри з leading zeros (001, 010, 100)
4. **НІКОЛИ не пропускай номери** — якщо є 001, 002, 004, наступний 003, а не 005
5. **Перевіряй ВСІ директорії**: todo + in_progress + done

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
- **File Path:** aitasks/todo/{TASK_FILENAME}
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
- **Working directory:** epass
- **Tech stack:** Django 4.2+, Python 3.11+, PostgreSQL, pytest

---

## SDD Context (for Feature Tasks)

If this is a **feature task** (not global), read SDD documents:

1. **Constitution** (project standards):
   ```
   aidocs/sdd/{project}/constitution.md
   ```

2. **Spec** (requirements):
   ```
   aidocs/sdd/{project}/features/{feature}/spec.md
   ```

3. **Design** (technical approach):
   ```
   aidocs/sdd/{project}/features/{feature}/design.md
   ```

**Use this context to:**
- Follow project standards from constitution
- Reference requirements from spec (FR-1, FR-2, etc.)
- Use technical decisions from design (AD-1, AD-2, etc.)
- Link task to specific files from design.md

---

## Execution Phases

### Phase 1: Deep Research

Research the codebase before writing the task.

1. **Find related files** using Glob and Grep tools
2. **Read domain documentation** (app/CLAUDE.md, domain-specific CLAUDE.md files)
3. **Find existing patterns** - how similar features are implemented
4. **Check existing tasks** in todo/done directories
5. **For SDD tasks**: Read constitution, spec, and design documents

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
## Project: epass

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
PATH: aitasks/todo/TASK_XXX_name.md

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
- Path: aitasks/todo/TASK_XXX_name.md

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
