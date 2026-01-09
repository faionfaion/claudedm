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

Run the discovery scripts with base path:

```bash
BASE_PATH="$HOME"  # or specific path if needed
bash .claude/skills/donexttask/scripts/find-tasks.sh "$BASE_PATH"
bash .claude/skills/donexttask/scripts/read-task-summaries.sh "$BASE_PATH"
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

## PHASE 2.5: Read SDD Context (for feature tasks)

**If SOURCE is a feature (not global), read SDD documents BEFORE execution:**

```bash
PROJECT="epass"
FEATURE="<feature-name>"
SDD_BASE="aidocs/sdd/${PROJECT}"
```

### Read in this order:

1. **Constitution (project standards):**
   ```bash
   cat "${SDD_BASE}/constitution.md"
   ```

2. **Feature specification (requirements):**
   ```bash
   cat "${SDD_BASE}/features/${FEATURE}/spec.md"
   ```

3. **Feature design (technical design):**
   ```bash
   cat "${SDD_BASE}/features/${FEATURE}/design.md"
   ```

Store this context - it will be passed to subagents for each task.

---

## PHASE 2.7: Clarifying Questions (BEFORE execution!)

**ВСІ уточнюючі питання задаються ДО початку виконання!**

After reading tasks and SDD context, identify ANY ambiguities:

1. Review each task for unclear requirements
2. Check if SDD documents have conflicting information
3. Identify missing dependencies or prerequisites

**If questions exist:**
- Use AskUserQuestion tool to ask ALL questions at once
- Wait for user answers
- Document decisions for subagents

**If no questions:**
- Proceed directly to PHASE 3

**CRITICAL: After this phase, NO more questions until all tasks complete!**

---

## PHASE 3: Create Feature Branch

**Check current state:**

```bash
cd epass
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

### Execute Loop - КОЖЕН ТАСК В ОКРЕМОМУ САБАГЕНТІ!

**CRITICAL: Ви ПОВИННІ використовувати Task tool для КОЖНОГО таску!**

For each task in the selected source:

1. `TASK_START=$(date +%s)`
2. Report: "[N/total] Виконую TASK_XXX..."
3. **ОБОВ'ЯЗКОВО: Launch Task tool with subagent_type="general-purpose"**
4. **WAIT for subagent to complete before continuing**
5. `TASK_END=$(date +%s)`
6. `DURATION=$((TASK_END - TASK_START))`
7. Convert: `MIN=$((DURATION / 60))` `SEC=$((DURATION % 60))`
8. Report: "TASK_XXX завершено за ${MIN}m ${SEC}s"
9. **ONLY THEN proceed to next task**

### Task Tool Call Format (MANDATORY!)

For each task, you MUST call:

```
Task tool:
  subagent_type: "general-purpose"
  description: "Execute TASK_XXX"
  prompt: |
    You are executing a task from the E-Pass task queue.

    TASK SOURCE: {SOURCE}
    TASKS_DIR: {TASKS_DIR}

    ## SDD Context (for feature tasks):
    {Include constitution.md, spec.md, design.md content here if feature task}

    ## Clarifications from user:
    {Include any answers from PHASE 2.7 here}

    Execute this task using the /donexttask skill:
    1. Call Skill tool with skill="donexttask" and args="{SOURCE}"
    2. Wait for full completion
    3. Return the result

    CRITICAL RULES:
    - Work fully autonomously - do NOT ask user questions
    - If blocked, return BLOCKED status with reason - do NOT ask user
    - Complete the task including commit and moving to done
    - Follow SDD constitution and design patterns
```

---

### ⚠️ AUTONOMOUS EXECUTION MODE

**Під час виконання тасків (PHASE 4) НЕ ЗУПИНЯЄМОСЬ!**

- Сабагенти працюють автономно без питань до користувача
- Якщо таск має проблему - повертається статус BLOCKED/FAILED
- Оркестратор переходить до наступного таску
- Питання збираються в кінці, а не під час виконання
- Зупинка лише при КРИТИЧНІЙ блокуючій проблемі (git conflict, build broken)

**Блокуючі проблеми (зупинити виконання):**
- Git merge conflict
- Build completely broken (can't compile)
- Missing critical dependency
- Security vulnerability discovered

**НЕ блокуючі (продовжувати виконання):**
- One task failed - skip and continue
- Test failures in one task - document and continue
- Unclear requirements - use best judgment, document decision

---

**Key behaviors:**
- КОЖЕН таск виконується в ОКРЕМОМУ сабагенті через Task tool
- Чекаємо завершення сабагента перед запуском наступного
- Subagent calls /donexttask skill and handles everything
- Subagent creates commit and moves task to done
- Orchestrator tracks progress, timing, and launches next agent
- НІКОЛИ не запускаємо наступний таск поки не завершився попередній
- **НЕ зупиняємось для питань - все питання задані в PHASE 2.7**

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
7. **🔍 Review results** (issues found and fixed)
8. **✅ Test results** (pass/fail count)
9. **🔧 Additional fixes** (if any)
10. Next steps: `git push -u origin <branch>` and `glab mr create --fill`

**Do NOT push, merge, or ask user for confirmation.**

---

## PHASE 6: Final Review and Quality Check

### Обов'язкове фінальне ревью після виконання всіх тасків!

After ALL tasks are completed, perform these quality checks:

### 6.1 Code Review

Review all changes made in this batch:

```bash
cd epass
git diff main..HEAD
```

Look for:
- Code style issues
- Potential bugs or logic errors
- Missing imports or broken references
- Security vulnerabilities
- Performance issues

### 6.2 Test Coverage Check

```bash
cd epass
make test-dev
```

If tests fail:
1. Identify which tests are failing
2. Fix the issues
3. Create additional commit: `fix: resolve test failures after batch execution`

### 6.3 Quality Checks

```bash
cd epass
make fix  # autoflake + isort + black + flake8
```

If there are auto-fixes:
1. Review the changes
2. Commit if needed: `style: apply code formatting after batch execution`

### 6.4 Important Issues Fix

If during review you find **critical issues**:
- Missing test coverage for new code
- Obvious bugs that slipped through
- Security vulnerabilities
- Broken functionality

**Fix them immediately** and commit: `fix: address issues found during batch review`

### 6.5 Final Summary Report

Add to final report:
- Review findings (if any)
- Test results (pass/fail count)
- Additional fixes made
- Overall code quality assessment

---

## Architecture Summary

**Orchestrator responsibilities:**
- Read task summaries
- **Read SDD context (constitution, spec, design) for feature tasks**
- **Ask ALL clarifying questions BEFORE execution (PHASE 2.7)**
- Create meaningful branch name
- **Launch Task tool with subagent_type="general-purpose" for EACH task**
- **Pass SDD context and clarifications to each subagent**
- **Wait for each subagent to complete before starting next**
- **⏱️ Track execution time for EACH task**
- Track progress - **continue even if task fails (unless blocking)**
- **After all tasks: run final review and quality checks (PHASE 6)**
- **⏱️ Generate final report WITH timing list and total time**

**Subagent responsibilities (via Task tool):**
- Call /donexttask skill with Skill tool
- Execute task fully
- Create commit
- Move task to done
- Return summary

**Execution flow:**
```
PHASE 1:   Find tasks
PHASE 2:   Select source
PHASE 2.5: Read SDD (constitution, spec, design) - for feature tasks
PHASE 2.7: Ask ALL clarifying questions - BEFORE execution
PHASE 3:   Create branch
PHASE 4:   FOR EACH task (AUTONOMOUS - NO STOPS!):
           -> Task tool (subagent_type="general-purpose")
           -> Pass SDD context + clarifications
           -> Wait for completion
           -> Record timing
           -> Next task (even if previous failed)
PHASE 5:   Generate report
PHASE 6:   Review + Tests + Fix issues
```

**Question timing:**
- PHASE 2.7: ALL questions asked here
- PHASE 4: NO questions, fully autonomous
- PHASE 6: Issues collected, reported at end

---

## Safety Features

1. Branch isolation - all work on feature branch
2. Per-task commits - easy to revert individual tasks
3. No remote changes - nothing pushed automatically
4. Auto-stash - preserves uncommitted work
5. Complete reporting - detailed summary at end
