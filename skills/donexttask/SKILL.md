---
name: donexttask
description: Executes next task from queue fully autonomously via subagent. Picks task, moves to in_progress, executes, documents, commits, moves to done. Returns summary only.
---

# Execute Next Task (Autonomous Subagent)

Communicate with the user in Ukrainian.

## Overview

Autonomous task execution workflow:
- Subagent determines which task to pick
- Subagent moves task to in_progress
- Subagent executes, documents, commits
- Subagent moves task to done
- Orchestrator receives only summary

## Input Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `global` | Global tasks from /aitasks/ | `/donexttask global` |
| `feature:project/name` | Feature-specific tasks | `/donexttask feature:epass/notifications` |
| (none) | Ask user for source | `/donexttask` |

Task paths:
- Global: `aitasks/`
- Feature: `aidocs/sdd/{project}/features/{feature}/tasks/`

## Failed Attempts

| Approach | Why It Fails | Use Instead |
|----------|--------------|-------------|
| Batch file operations | Context lost between phases | Single-phase execution per subtask |
| Skip research phase | Missing dependencies, wrong patterns | Always read existing code first |
| Modify multiple files blindly | Breaks related functionality | Read, understand, then modify |
| Run tests only at end | Large fixes needed late | Test after each significant change |
| Generic commit messages | Hard to track/revert | Descriptive commits with task ID |

## Degrees of Freedom

Subagent decides autonomously:
- **File structure**: Follow existing patterns in codebase
- **Implementation details**: Choose approach based on research
- **Test scope**: Cover acceptance criteria at minimum
- **Commit granularity**: One commit per task (required)

Subagent must NOT:
- Change task acceptance criteria
- Skip quality checks (make fix, make test-dev)
- Leave task in in_progress without documentation
- Push to remote or create merge requests

## Orchestrator Workflow

### Step 1: Determine Task Source

If parameter provided:
- `global` -> TASKS_DIR="aitasks"
- `feature:epass/x` -> TASKS_DIR="aidocs/sdd/epass/features/x/tasks"

If no parameter, run discovery script and ask user to select source.

### Step 2: Launch Subagent

Pass TASKS_DIR to subagent with autonomous execution instructions.

### Step 3: Report Result

Output subagent summary to user.

## Subagent Instructions

Project context:
- Project: E-Pass electronic transport payment system
- Working directory: `epass`
- Tech stack: Django 4.2+, Python 3.11+, PostgreSQL, pytest
- Tasks directory: `{TASKS_DIR}` (from orchestrator)

### Phase 1: Pick Task

Check in_progress first. If empty, take lowest numbered from todo. If no tasks available, return NO_TASKS status and stop.

### Phase 2: Move to In Progress

Move selected task file from todo/ to in_progress/.

### Phase 3: Research

1. Read task file completely
2. Research codebase using Glob, Grep, Read
3. Read relevant CLAUDE.md files
4. For feature tasks, read spec.md and design.md

### Phase 4: Plan

Update Subtasks section in task file with specific implementation steps.

### Phase 5: Execute and Document

For each subtask:
1. Execute (write code, tests)
2. Mark `[x]` in task file
3. Add details to Implementation section

Document immediately after each subtask completion.

### Phase 6: Quality

Run quality checks:
- `make fix` (autoflake + isort + black + flake8)
- `make test-dev` (pytest in Docker)

Fix failures, document fixes, rerun until passing.

### Phase 7: Finalize Task File

Add Summary section with:
- What was done
- Key decisions
- Files changed (with line counts)
- Test results

### Phase 8: Commit

Create commit with format: `TASK_XXX: Brief description`

Save commit hash for result.

### Phase 9: Move to Done

Move task file from in_progress/ to done/.

## Output Format

Success:
```
STATUS: SUCCESS
TASK: TASK_XXX_short_name
TITLE: Human readable title
SOURCE: {global|feature:project/feature-name}
SUMMARY: (2-3 bullet points)
FILES_CHANGED: (list with created/modified)
TESTS: N added, all pass
COMMIT: <hash>
```

Failed:
```
STATUS: FAILED
TASK: TASK_XXX_short_name
SOURCE: {global|feature:project/feature-name}
REASON: Short description
PROGRESS: N/M subtasks completed
LOCATION: Still in in_progress/
```

No tasks:
```
STATUS: NO_TASKS
MESSAGE: Task queue empty
```

Blocked:
```
STATUS: BLOCKED
TASK: TASK_XXX_short_name
SOURCE: {global|feature:project/feature-name}
BLOCKER: What is blocking
SUGGESTION: What is needed to unblock
LOCATION: Still in in_progress/
```

## Error Handling

- **Tests fail**: Try to fix (up to 3 attempts), then FAILED status
- **Task unclear**: Document uncertainty, BLOCKED status with suggestion
- **Timeout/crash**: Task remains in in_progress, progress saved in task file

## Quality Checklist

Before marking done:
- All subtasks marked `[x]`
- All acceptance criteria met
- `make test-dev` passes
- Implementation section filled
- Summary written
- Changes committed
- Task moved to done/
