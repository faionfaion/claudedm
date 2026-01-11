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

### 3.2 Detect Project Type

Use AskUserQuestion:

**Question:** "Чи існує вже codebase для цього проекту?"

**Options:**
- "Так, є існуючий код" → MODE 1: Analysis
- "Ні, це новий проект з нуля" → MODE 2: Brainstorming

### 3.3a MODE 1: Existing Codebase

Ask user for path to codebase, then call Skill tool:
```
skill: "sdd-writing-constitutions"
args: "{project_name} {codebase_path}"
```

The skill will:
- Analyze project structure
- Identify tech stack, patterns, standards
- Draft constitution based on findings
- Review with user

### 3.3b MODE 2: New Project (Brainstorming)

Call Skill tool:
```
skill: "sdd-writing-constitutions"
args: "{project_name}"
```

The skill will use Socratic dialogue to explore:

**Vision (Five Whys):**
- Яку проблему вирішуємо?
- Хто цільова аудиторія?
- Чому саме цей підхід?

**Tech Choices (Alternatives):**
- Backend: Django vs FastAPI vs NestJS
- Database: PostgreSQL vs MongoDB vs SQLite
- Frontend: React vs Vue vs vanilla

**Architecture (Trade-offs):**
- Monolith vs Microservices
- REST vs GraphQL
- ORM vs Raw SQL

**Standards:**
- Linter, formatter, types
- Testing requirements
- Git workflow

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

### 5.2 Create Specification (Socratic Dialogue)

Call Skill tool:
```
skill: "sdd-writing-specifications"
args: "{project} {feature_name}"
```

The skill uses Socratic dialogue:

**Brainstorming Phase:**
- "Яку проблему вирішуємо?" + Five Whys
- "Хто страждає і як?"
- Explore alternatives for each solution
- Challenge assumptions

**Research Phase:**
- Find related code in codebase
- Identify reusable patterns
- Check existing similar features

**Clarification Phase:**
- User Stories workshop (roles, goals)
- Edge cases through questions
- Trade-offs for priorities

**Draft Phase:**
- Section-by-section with validation
- Problem Statement → validate
- User Stories → validate
- Requirements → validate
- Out of Scope → validate

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

## Example Flows

### Example 1: New Project (Brainstorming)

```
User: /sdd

Claude: З яким проектом працюємо?
[ ] epass
[ ] + Новий проект

User: + Новий проект

Claude: Назва нового проекту?
User: marketplace

Claude: Чи існує вже codebase для цього проекту?
[ ] Так, є існуючий код
[ ] Ні, це новий проект з нуля

User: Ні, це новий проект з нуля

Claude: [Socratic dialogue for constitution]
        "Розкажи про проект. Яку проблему він вирішує?"

User: B2B маркетплейс для оптових закупівель

Claude: "Чому потрібен новий маркетплейс? Існуючі не підходять?"

User: Немає локального рішення з інтеграцією з 1С

Claude: [Explores tech alternatives with trade-offs]
        "Backend Framework:
         A: Django - batteries included, ORM, admin
         B: FastAPI - швидкий, async, modern
         Який підхід ближче?"

User: Django

Claude: [Continues brainstorming...]
        [Creates constitution.md with standards]

Claude: Constitution готова. Яка перша фіча?
```

### Example 2: Existing Project + New Feature

```
User: /sdd

Claude: З яким проектом працюємо?
[ ] epass
[ ] marketplace
[ ] + Новий проект

User: epass

Claude: Яка фіча?
[ ] crm-integration
[ ] + Нова фіча

User: + Нова фіча

Claude: Назва нової фічі?
User: payment-refunds

Claude: [Socratic dialogue for spec]
        "Яку проблему вирішуємо? Хто страждає?"

User: Клієнти не можуть отримати рефанд

Claude: "Чому не можуть? Що заважає?"
        [Five Whys continues...]

Claude: "Варіанти рішення:
         A: Повний рефанд одразу
         B: Частковий рефанд
         C: Рефанд через запит
         Що потрібно?"

User: B + C

Claude: [Draft spec section by section]
        "Problem Statement:
         Клієнти не можуть...
         Це правильно?"

User: Так

Claude: [Continues with User Stories, Requirements...]
        [Creates spec.md]

Claude: Специфікацію затверджено?
User: Так

Claude: [Creates design.md through analysis]
Claude: [Creates tasks]

Claude: Готово!
        - spec.md: aidocs/sdd/epass/features/payment-refunds/spec.md
        - design.md: aidocs/sdd/epass/features/payment-refunds/design.md
        - Створено 5 тасків

        Щоб виконати: /doalltasks epass/payment-refunds
```
