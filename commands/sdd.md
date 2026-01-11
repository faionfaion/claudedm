---
description: "SDD Workflow Orchestrator - manage projects, features, specs, designs, tasks"
argument-hint: "[project] or [project/feature]"
---

# SDD Workflow Orchestrator

**Communicate with the user in Ukrainian.**

---

## Purpose

Interactive orchestrator for Spec-Driven Development workflow:
- Create new projects with constitutions
- Create new features with specs, designs, tasks
- Modify existing features

---

## PHASE 1: Discover Projects

Find existing projects:

```bash
ls -d aidocs/sdd/*/ 2>/dev/null | xargs -I{} basename {} | grep -v "^CLAUDE.md$" | grep -v "^.*TEMPLATE.*$"
```

Or check directories:
```bash
for d in aidocs/sdd/*/; do
  [ -f "${d}constitution.md" ] && basename "$d"
done
```

---

## PHASE 2: Select Project

Use AskUserQuestion to ask:

**Question:** "З яким проектом працюємо?"

**Options:**
- Each existing project from PHASE 1 (e.g., "epass", "billing")
- "+ Новий проект" option

If user selects existing project → go to PHASE 4
If user selects new project → go to PHASE 3

---

## PHASE 3: New Project

### 3.1 Get Project Name

Use AskUserQuestion:
- "Назва нового проекту?" (free text input via "Other")

### 3.2 Create Constitution

Call Skill tool:
```
skill: "sdd-writing-constitutions"
args: "{project_name}"
```

The skill will:
- Analyze codebase (ask user for path)
- Interview user about standards
- Create constitution.md

After constitution created → go to PHASE 4 with new project selected

---

## PHASE 4: Select Feature

### 4.1 Discover Features

Find existing features for selected project:

```bash
ls -d aidocs/sdd/{project}/features/*/ 2>/dev/null | xargs -I{} basename {}
```

### 4.2 Ask User

Use AskUserQuestion:

**Question:** "Яка фіча?"

**Options:**
- Each existing feature (e.g., "crm-integration", "notifications")
- "+ Нова фіча" option

If user selects existing feature → go to PHASE 6
If user selects new feature → go to PHASE 5

---

## PHASE 5: New Feature Workflow

### 5.1 Get Feature Name

Use AskUserQuestion:
- "Назва нової фічі? (kebab-case, наприклад: crm-webhooks)"

### 5.2 Create Specification

Call Skill tool:
```
skill: "sdd-writing-specifications"
args: "{project} {feature_name}"
```

The skill will:
- Interview user about requirements
- Research codebase
- Create spec.md

**Wait for user approval of spec.md before continuing!**

### 5.3 Create Design

After spec approved, call Skill tool:
```
skill: "sdd-writing-design-docs"
args: "{project} {feature_name}"
```

The skill will:
- Read spec.md
- Design technical implementation
- Create design.md

**Wait for user approval of design.md before continuing!**

### 5.4 Create Tasks

After design approved, call Skill tool:
```
skill: "make-tasks"
args: "{project} {feature_name}"
```

The skill will:
- Read spec.md and design.md
- Break down into atomic tasks
- Create TASK_*.md files in tasks/todo/

### 5.5 Summary

Report:
- spec.md location
- design.md location
- Number of tasks created
- Next step: `/doalltasks {project}/{feature_name}`

---

## PHASE 6: Existing Feature

### 6.1 Show Feature Status

Read and summarize:
- spec.md status
- design.md status
- Tasks count (todo/in_progress/done)

### 6.2 Ask What to Do

Use AskUserQuestion:

**Question:** "Що зробити з фічею {feature_name}?"

**Options:**
- "Оновити специфікацію" → edit spec.md
- "Оновити дизайн" → edit design.md
- "Додати/змінити таски" → manage tasks
- "Виконати таски" → run /doalltasks

### 6.3 Execute Based on Choice

**If "Оновити специфікацію":**
- Ask what to change
- Call skill: "sdd-writing-specifications" with edit context

**If "Оновити дизайн":**
- Ask what to change
- Call skill: "sdd-writing-design-docs" with edit context

**If "Додати/змінити таски":**
- Call skill: "make-tasks" for new tasks
- Or read existing tasks and ask which to modify

**If "Виконати таски":**
- Call command: `/doalltasks {project}/{feature_name}`

---

## SDD Directory Structure

```
aidocs/sdd/
├── CLAUDE.md
├── SDD_WORKFLOW.md
├── SPEC_TEMPLATE.md
├── DESIGN_TEMPLATE.md
├── CONSTITUTION_TEMPLATE.md
└── {project}/
    ├── constitution.md
    └── features/
        └── {feature}/
            ├── spec.md
            ├── design.md
            └── tasks/
                ├── todo/
                ├── in_progress/
                └── done/
```

---

## Skills Used

- `sdd-writing-constitutions` - create/edit project constitution
- `sdd-writing-specifications` - create/edit feature spec
- `sdd-writing-design-docs` - create/edit feature design
- `make-tasks` - create tasks from spec+design

## Commands Used

- `/doalltasks` - execute all tasks for a feature
- `/donexttask` - execute single next task

---

## Example Flow

```
User: /sdd

Claude: З яким проектом працюємо?
[ ] epass
[ ] billing
[ ] + Новий проект

User: epass

Claude: Яка фіча?
[ ] crm-integration
[ ] notifications
[ ] + Нова фіча

User: + Нова фіча

Claude: Назва нової фічі?
User: payment-refunds

Claude: [Calls sdd-writing-specifications skill]
        [Creates spec.md through interview]

Claude: Специфікацію створено. Переглянь та підтверди.
User: Ок, все добре

Claude: [Calls sdd-writing-design-docs skill]
        [Creates design.md]

Claude: Дизайн створено. Переглянь та підтверди.
User: Додай ще один endpoint для часткового рефанду

Claude: [Updates design.md]

User: Тепер ок

Claude: [Calls make-tasks skill]
        [Creates 5 tasks]

Claude: Готово!
        - spec.md: aidocs/sdd/epass/features/payment-refunds/spec.md
        - design.md: aidocs/sdd/epass/features/payment-refunds/design.md
        - Створено 5 тасків

        Щоб виконати: /doalltasks epass/payment-refunds
```
