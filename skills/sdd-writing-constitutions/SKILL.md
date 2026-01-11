---
name: sdd-writing-constitutions
user-invocable: false
description: "SDD Framework: Creates, edits, or updates constitution.md with project principles and standards. Use when user asks to create constitution, edit constitution, update project standards. Triggers on \"constitution.md\", \"constitution\", \"конституція проекту\", \"стандарти проекту\"."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Bash(cat:*), Bash(git log:*)
---

# SDD: Writing Constitutions

**Communication with user: Ukrainian. Constitution content: Ukrainian.**

---

## SDD Framework Overview

Цей скіл є частиною **Spec-Driven Development (SDD)** фреймворку.

### Філософія SDD

**"Intent is the source of truth"** — специфікація є головним артефактом, код — лише її реалізація.

### SDD Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 0: CONSTITUTION (One-time per project) ← ВИ ТУТ         │
│                                                                 │
│  1. Проаналізувати codebase                                     │
│  2. Створити constitution.md (цей скіл)                        │
│  3. Review & approve                                            │
│                                                                 │
│  Output: constitution.md (project standards)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: SPECIFICATION (per feature)                           │
│  → Скіл: sdd-writing-specifications                            │
│  Output: spec.md                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: DESIGN (per feature)                                  │
│  → Скіл: sdd-writing-design-docs                               │
│  Output: design.md                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3-4: TASKS + EXECUTION                                   │
│  → /maketasks, /donexttask, /doalltasks                        │
│  Output: Code + Tests + Commits                                │
└─────────────────────────────────────────────────────────────────┘
```

### SDD Directory Structure

```
aidocs/sdd/
├── CLAUDE.md                          # SDD overview
├── SDD_WORKFLOW.md                    # Детальний workflow
├── SPEC_TEMPLATE.md                   # Шаблон spec.md
├── DESIGN_TEMPLATE.md                 # Шаблон design.md
├── CONSTITUTION_TEMPLATE.md           # Шаблон constitution.md ← використовуй!
├── TASK_EXECUTION.md                  # Процес виконання тасків
└── {project}/                         # epass, billing, etc.
    ├── constitution.md                # Принципи проекту ← створюємо тут
    └── features/
        └── {feature-name}/
            ├── spec.md
            ├── design.md
            └── tasks/
```

### Роль Constitution

**Constitution.md — незмінні принципи проекту, які діють для ВСІХ фіч.**

Він визначає:
- Technology stack
- Code standards (linters, formatters, naming)
- Architecture patterns
- Testing requirements
- Git workflow
- API standards

**Кожен design.md та task ПОВИНЕН відповідати constitution!**

---

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create constitution.md for a project
- Edit/update/change/modify project constitution
- Define project standards and principles
- Analyze codebase for conventions

**Trigger phrases:** "create constitution", "edit constitution", "update constitution.md", "project standards", "створити конституцію", "оновити конституцію", "стандарти проекту"

---

## Purpose

This skill creates constitution.md for a project by:
1. Deep analysis of existing codebase
2. Identifying patterns and conventions
3. Documenting standards and principles

---

## Input

- `project_name` - project name
- `project_path` - path to codebase

---

## Workflow

### Phase 1: Analyze Project Structure

The assistant examines the project structure:
- General directory layout (2 levels deep)
- CLAUDE.md and README.md files
- Configuration files (py, toml, yaml)

### Phase 2: Identify Technology Stack

The assistant determines technologies:
- Python version from pyproject.toml or setup.py
- Framework version from requirements or pyproject.toml
- Database configuration from settings
- Key dependencies from requirements files

### Phase 3: Analyze Code Standards

The assistant identifies code style:
- Linter configurations (pyproject.toml, .flake8, setup.cfg)
- Makefile commands for quality checks
- Naming conventions from models.py and services.py files

### Phase 4: Identify Architecture Patterns

The assistant investigates architecture:
- Application structure and organization
- Typical files in each app
- Layer patterns (views, services, repositories, models)
- Domain-driven design indicators

### Phase 5: Analyze Testing Practices

The assistant examines tests:
- Test directory structure
- Test file patterns and styles
- Coverage configuration

### Phase 6: Identify Git Workflow

The assistant investigates git practices:
- Recent commit message style
- Branch naming conventions
- CI/CD configuration files

### Phase 7: Draft Constitution

The assistant creates constitution.md using the template from `/aidocs/sdd/CONSTITUTION_TEMPLATE.md`

**Required sections:**
- Overview
- Technology Stack

**Recommended sections (if identified):**
- Code Standards
- Architecture Patterns
- Testing Requirements

**Optional sections (if relevant):**
- API Standards
- Database Guidelines
- Security
- Git Workflow
- Logging and Monitoring
- Performance

### Phase 8: Review with User

The assistant presents the draft:
1. Asks if everything is correct
2. Clarifies disputed points
3. Adds project-specific details

### Phase 9: Save Constitution

The assistant saves the file to:
```
aidocs/sdd/{project_name}/constitution.md
```

Create directory if needed:
```bash
mkdir -p aidocs/sdd/{project_name}
```

---

## Analysis Checklist

```
[ ] Project structure understood?
[ ] Technology stack identified?
[ ] Code style detected (linters, formatters)?
[ ] Naming conventions documented?
[ ] Architecture patterns described?
[ ] Testing practices clear?
[ ] Git workflow determined?
[ ] CI/CD process documented?
```

---

## Output

File `constitution.md` at:
```
aidocs/sdd/{project_name}/constitution.md
```

**Next step:** Після approve constitution.md → створюй фічі:
1. Створи директорію фічі: `mkdir -p aidocs/sdd/{project}/features/{feature}/tasks/{todo,in_progress,done}`
2. Використай скіл `sdd-writing-specifications` для створення spec.md

---

## Example Analysis Output

```
Analysis of E-Pass project:

1. Structure:
   - Django project in app/
   - Applications in app/applications/
   - Config in config/

2. Tech Stack:
   - Python 3.11+
   - Django 4.2+
   - PostgreSQL
   - Redis, RabbitMQ

3. Code Standards:
   - black + isort + flake8
   - Type hints
   - Docstrings

4. Architecture:
   - Layered: views -> services -> models
   - Each app: models, views, services, serializers

5. Testing:
   - pytest
   - Factory Boy
   - 80%+ coverage

6. Git:
   - Conventional commits
   - Feature branches
   - GitLab CI/CD
```

---

## Failed Attempts

Common issues when creating constitutions:

- **Incomplete analysis**: Skipping phases leads to missing important patterns. Always complete all phases.
- **Assumptions without evidence**: Do not assume patterns exist without finding concrete examples in the codebase.
- **Over-documenting**: Constitution should capture what IS, not what SHOULD BE. Avoid prescriptive rules not supported by existing code.
- **Missing user review**: Always show draft to user before finalizing. Project-specific knowledge is essential.

---

## Sources

- Template: `templates/CONSTITUTION_TEMPLATE.md` (in this skill directory)
