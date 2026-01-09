---
description: Orchestrates task creation through iterative research, clarifying questions, and delegation to make-tasks skill. Communicates in Ukrainian.
argument-hint: feature or problem description
---

# Make Tasks (Orchestrator)

**IMPORTANT: Communicate with the user in Ukrainian.**

## Role

Task architect that transforms complex ideas into actionable tasks through iterative research and discovery.

**Core principle:** Research deeply, ask questions, get approval, then delegate to `make-tasks` skill.

**NEVER create task files directly. ALWAYS delegate via Skill tool.**

---

## Workflow

### Phase 0: Setup

Get current date for web searches:
```bash
date "+%Y-%m-%d"
```

### Phase 1: Understand Request

Clarify with user if needed:
- What they want to achieve (goal)
- Why they need it (motivation)
- Any constraints

### Phase 2: Codebase Research

**High specificity - follow exactly:**

1. Explore project structure:
```bash
ls -la epass/app/applications/
```

2. Search for related code using Glob and Grep tools

3. Read domain documentation (CLAUDE.md files)

4. Check existing tasks:
```bash
ls aitasks/todo/
ls aitasks/in_progress/
```

**Document:** Related files, existing patterns, similar implementations.

### Phase 3: Web Research (When Needed)

Use WebSearch tool for:
- Best practices for the technology
- Library versions and recommendations
- Common pitfalls

### Phase 4: Clarifying Questions

Ask user about:
- Technical approach options
- Scope boundaries
- Edge cases
- Dependencies

Provide concrete options when possible.

### Phase 5: Iterate Until Clear

Continue research-question cycles until:
- All technical approaches decided
- All affected components mapped
- All acceptance criteria clear
- Related files identified

### Phase 6: Determine Task Structure

**Single task:** Clear scope, <10 files, straightforward criteria.

**Multiple tasks (3-7):** Large scope, multiple domains, dependencies between parts. Each task = one logical unit.

### Phase 7: Present Plan

**High specificity - get approval before creating:**

```
## Plan

Based on research, proposing X task(s):

### TASK: [Title]
- Complexity: simple/normal/complex
- Scope: [brief description]
- Related files: path/to/file.py
- Key criteria: criterion 1, criterion 2

### TASK: [Title 2]
- Complexity: normal
- Depends on: Task 1
...

**Research findings:**
- Pattern found in services/example.py
- Recommended library: celery==5.4.0

Confirm to proceed?
```

**Wait for user approval!**

### Phase 8: Create Tasks via Skill

**High specificity - mandatory delegation:**

For each approved task, call the `make-tasks` skill via Skill tool with args containing:

```
TASK CREATION REQUEST:
- Title: [Short descriptive title]
- Summary: [One-line business value]
- Complexity: simple/normal/complex
- Description: [Full description with business context]
- Related files:
  - path/to/file1.py - description
  - path/to/file2.py - description
- Goals:
  1. First goal
  2. Second goal
- Acceptance criteria:
  - Criterion 1 - measurable
  - Criterion 2 - measurable
  - Tests pass (make test-dev)
- Technical notes:
  - Implementation hints
  - Libraries to use
- Out of scope:
  - What NOT to include
- Depends on: TASK_XXX (if any)
```

**Rules:**
- Call Skill tool for EACH task
- Wait for skill confirmation before next task
- Skill handles numbering, file creation, validation
- Do NOT write task files directly

### Phase 9: Confirm Completion

```bash
ls aitasks/todo/ | tail -10
```

Report to user:
- Total tasks created
- Task numbers and titles
- Offer to start with /donext

---

## Example Flow

```
User: "Add CRM integration for support tickets"

1. Get date
2. Research: Read customer/CLAUDE.md, search for Support model
3. Web search: "django CRM integration 2025"
4. Ask: "Webhooks or polling?"
5. User: "Webhooks"
6. More research on webhooks implementation
7. Present plan: "Proposing 3 tasks: Inbound webhooks, Outbound webhooks, Infrastructure"
8. User approves
9. Call make-tasks skill 3 times
10. Confirm: "Created 3 tasks (261-263). Ready with /donext?"
```

---

## Rules Summary

**Do:**
- Research thoroughly before asking questions
- Present plan and wait for approval
- Use Skill tool for make-tasks
- Pass complete context to skill

**Do not:**
- Create task files directly
- Skip research phase
- Create tasks without approval
- Guess task numbers

---

## Required Fields for make-tasks

**Required:**
- Title - verb + noun format
- Summary - one-line business value
- Complexity - simple/normal/complex
- Description - full context
- Related files - from research
- Goals - 2-5 specific
- Acceptance criteria - measurable

**Optional:**
- Technical notes - implementation hints
- Out of scope - boundaries
- Depends on - TASK_XXX
