---
description: "Do All Tasks (Orchestrator)"
argument-hint: "[global|feature-name|partial-name]"
---

# Do All Tasks (Orchestrator)

**Communicate with the user in Ukrainian.**

---

## ⏱️ CRITICAL: TIMING IS MANDATORY

**You MUST track execution time for EVERY task. This is NOT optional.**

Before executing any task:
1. Record `TASK_START=$(date +%s)`
2. After task completes: `TASK_END=$(date +%s)`
3. Calculate duration: `DURATION=$((TASK_END - TASK_START))`
4. Store for final report

**Final report MUST include per-task timing list and total time. Without timing data, the execution is considered INCOMPLETE.**

---

## Purpose

Orchestrator for sequential task execution:
1. Find all tasks (global + feature-specific)
2. Let user choose via menu OR parse text command
3. Execute selected tasks autonomously via subagents
4. **Track execution time for each task**
5. NO push, NO merge - local work only

## Input Handling

- `/doalltasks` - show selection menu
- `/doalltasks notifications` - find feature containing "notifications"
- `/doalltasks epass/feature-name` - specific feature
- `/doalltasks global` - global tasks only

---

## PHASE 1: Find All Tasks

Run the discovery scripts:

```bash
bash ~/.claude/skills/donexttask/scripts/find-tasks.sh
bash ~/.claude/skills/donexttask/scripts/read-task-summaries.sh
```

If no tasks found, report "Черга тасків порожня!" and STOP.

---

## PHASE 2: Determine What to Execute

**If argument provided:**
- `global` - set SOURCE="global"
- `epass/feature-name` - set SOURCE="feature:epass/feature-name"
- `partial-name` - search for matching feature directory

**If no argument:**
Present interactive menu showing:
- Global tasks count and list
- Each feature with task counts
- "Execute all sequentially" option

Result: SOURCE = selected source

---

## PHASE 3: Create Feature Branch

**Check current state:**

```bash
cd /home/moskalyuk_ruslan/epass
git rev-parse --abbrev-ref HEAD
git status --short
```

If uncommitted changes exist, stash them automatically.

**Create meaningful branch name:**

Based on task summaries (first 6 lines of each), determine:
- Domain/theme (billing, controller, customer, etc.)
- Key action (tests, refactor, api, validation, etc.)

Format: `feature/<domain>-<description>`

Examples:
- `feature/billing-integration-tests`
- `feature/controller-validation-refactor`
- `feature/customer-api-improvements`

If on main, pull latest then create branch. Report the branch name and reasoning.

---

## PHASE 4: Execute Tasks via Subagents

### ⏱️ TIMING SETUP (DO THIS FIRST!)

```bash
BATCH_START=$(date +%s)
```

### Execute Loop

For each task in the selected source:

1. `TASK_START=$(date +%s)`
2. Report: "[N/total] Виконую TASK_XXX..."
3. Launch subagent via Task tool
4. `TASK_END=$(date +%s)`
5. `DURATION=$((TASK_END - TASK_START))`
6. Convert: `MIN=$((DURATION / 60))` `SEC=$((DURATION % 60))`
7. Report: "TASK_XXX завершено за ${MIN}m ${SEC}s"

**Subagent prompt:**
- "Execute task from SOURCE using /donexttask skill"
- "Work fully autonomously - do not ask user questions"
- "Complete the task including commit and moving to done"

**Key behaviors:**
- Subagent calls `/donexttask {SOURCE}` and handles everything
- Subagent creates commit and moves task to done
- Orchestrator tracks progress, timing, and launches next agent
- Never ask user for input during execution

---

## PHASE 5: Final Report

### ⏱️ TIMING SUMMARY (REQUIRED!)

```bash
BATCH_END=$(date +%s)
TOTAL_DURATION=$((BATCH_END - BATCH_START))
TOTAL_MIN=$((TOTAL_DURATION / 60))
TOTAL_SEC=$((TOTAL_DURATION % 60))
```

### Report Structure

**⏱️ TIMING LIST (MANDATORY - DO NOT SKIP!):**

```
## Час виконання

- TASK_527_cleanup_compose - 3m 42s
- TASK_528_fix_secret - 5m 18s
- TASK_529_add_queue - 8m 15s
- TASK_530_git_workflow - 4m 55s

**Загальний час: 22m 10s**
```

**Git summary:**
```bash
git log main..HEAD --oneline
git diff main..HEAD --stat
```

**Full report format:**
1. **⏱️ Загальний час виконання** (e.g., "Загальний час: 22m 10s")
2. **⏱️ Per-task timing list** (see above - THIS IS REQUIRED)
3. Total tasks completed
4. Branch name
5. Commit count and hashes
6. Changed files summary
7. Next steps: `git push -u origin <branch>` and `glab mr create --fill`

**Do NOT push, merge, or ask user for confirmation.**

---

## Architecture Summary

**Orchestrator responsibilities:**
- Read task summaries
- Create meaningful branch name
- Launch Task subagents sequentially
- **⏱️ Track execution time for EACH task**
- Track progress
- **⏱️ Generate final report WITH timing list and total time**

**Subagent responsibilities:**
- Call /donexttask skill
- Execute task fully
- Create commit
- Move task to done
- Return summary

---

## Safety Features

1. Branch isolation - all work on feature branch
2. Per-task commits - easy to revert individual tasks
3. No remote changes - nothing pushed automatically
4. Auto-stash - preserves uncommitted work
5. Complete reporting - detailed summary at end
