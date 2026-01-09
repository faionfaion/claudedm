---
name: sdd-writing-specifications
description: "SDD Framework: Creates, edits, or updates spec.md with requirements and user stories. Use when user asks to create spec, edit specification, update spec.md, write requirements. Triggers on \"spec.md\", \"specification\", \"специфікація\", \"вимоги\"."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# SDD: Writing Specifications

**Communication with user: Ukrainian. Spec content: Ukrainian.**

---

## SDD Framework Overview

Цей скіл є частиною **Spec-Driven Development (SDD)** фреймворку.

### Філософія SDD

**"Intent is the source of truth"** — специфікація є головним артефактом, код — лише її реалізація.

### SDD Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: SPECIFICATION (Human + AI) ← ВИ ТУТ                   │
│                                                                 │
│  1. Створити feature directory                                  │
│  2. Написати spec.md (цей скіл)                                │
│  3. Review & approve                                            │
│                                                                 │
│  Output: spec.md (status: approved)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: DESIGN (AI-assisted)                                  │
│  → Скіл: sdd-writing-design-docs                               │
│  Output: design.md                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: TASK CREATION (AI) → /maketasks                      │
│  Output: tasks/todo/TASK_*.md                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: EXECUTION (AI) → /donexttask, /doalltasks            │
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
├── CONSTITUTION_TEMPLATE.md           # Шаблон constitution.md
├── TASK_EXECUTION.md                  # Процес виконання тасків
└── {project}/                         # epass, billing, etc.
    ├── constitution.md                # Принципи проекту
    └── features/
        └── {feature-name}/            # kebab-case
            ├── spec.md                # ЩО і ЧОМУ ← створюємо тут
            ├── design.md              # ЯК (архітектура)
            └── tasks/                 # Задачі
                ├── todo/
                ├── in_progress/
                └── done/
```

### Key SDD Documents

| Document | Призначення | Створюється |
|----------|------------|-------------|
| `constitution.md` | Принципи проекту, стандарти | Один раз на проект |
| `spec.md` | ЩО і ЧОМУ (бізнес вимоги) | Для кожної фічі (цей скіл) |
| `design.md` | ЯК (технічна реалізація) | Після approve spec.md |
| `TASK_*.md` | Атомарні задачі | Після approve design.md |

---

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create spec.md for a feature
- Edit/update/change/modify existing specification
- Write requirements document
- Conduct requirements interview

**Trigger phrases:** "create spec", "edit specification", "update spec.md", "write requirements", "створити специфікацію", "оновити spec.md", "написати вимоги"

---

## Purpose

Creates comprehensive spec.md for features through stakeholder interviews, codebase research, and structured specification generation.

---

## Input

- `feature_name` - feature name (kebab-case)
- `project` - project name (default: epass)
- Or free-form feature description from user

---

## Workflow

### Phase 1: Initial Understanding

Gather from user:

1. **Problem Statement:** What problem? Who suffers? Consequences of not solving?
2. **User Stories:** Roles, goals, expected value
3. **Scope:** Must-have for v1 vs. deferred items

### Phase 2: Research Codebase

Investigate existing code to identify:
- Related models and their relationships
- Existing services and architectural patterns
- Similar feature implementations

Key locations:
- Models: `epass/app/applications/`
- Services: `services.py` files in application directories
- Project conventions: `epass/app/CLAUDE.md`

### Phase 3: Clarify Details

Technical clarification questions:

1. **API:** Endpoints, data format, access control
2. **Data Model:** Stored data, relationships to existing models
3. **Integration:** External systems, third-party APIs
4. **Non-Functional:** Load expectations, performance, security

### Phase 4: Draft Specification

Generate spec.md following template structure:
- Metadata (status, priority, date)
- Problem Statement
- User Stories (As a {role}, I want {goal}, so that {benefit})
- Functional Requirements (testable, numbered)
- Out of Scope

### Phase 5: Review and Refine

Present draft to user:
1. Verify understanding
2. Clarify ambiguities
3. Add missing items
4. Remove unnecessary items

### Phase 6: Save Specification

Create directory structure and save:

```bash
# Базовий шлях
SDD_BASE="aidocs/sdd"

# Створити директорії
mkdir -p ${SDD_BASE}/{project}/features/{feature_name}/tasks/{todo,in_progress,done}

# Зберегти spec.md
# ${SDD_BASE}/{project}/features/{feature_name}/spec.md
```

**Повний шлях:** `aidocs/sdd/{project}/features/{feature_name}/spec.md`

---

## Output

File `spec.md` at:
```
aidocs/sdd/{project}/features/{feature_name}/spec.md
```

**Next step:** Після approve spec.md → використовуй скіл `sdd-writing-design-docs` для створення design.md

---

## Requirements Elicitation Techniques

### Interview Methods
- Open questions: "Describe the problem..."
- Closed questions: "Is authorization required?"
- Clarifying: "What do you mean by...?"

### User Stories Format
```
As a [role]
I want [goal]
So that [benefit]
```

### MoSCoW Prioritization
- **Must have** - feature non-functional without it
- **Should have** - important but deferrable
- **Could have** - nice to have
- **Won't have** - explicitly excluded

### Five Whys
For deeper problem understanding - ask "why" up to 5 times to reach root cause.

---

## Questions Checklist

Before completion verify:
- Problem Statement clear
- All user roles identified
- User Stories specific
- Functional Requirements testable
- Out of Scope defined
- API Contract included (if needed)
- Data Model included (if needed)
- Open Questions resolved

---

## Degrees of Freedom

The skill implementer decides:
- Interview depth based on feature complexity
- Which codebase areas to research
- Level of technical detail in specification
- Whether to include Data Model and API Contract sections
- Task breakdown granularity

---

## Failed Attempts

Common mistakes to avoid:

1. **Starting specification before understanding problem** - Always complete Phase 1 interview before drafting
2. **Skipping codebase research** - Leads to specs that ignore existing patterns or duplicate functionality
3. **Writing vague requirements** - "Should work fast" is not testable; "Response time under 200ms" is
4. **Mixing Must-have with Nice-to-have** - Use MoSCoW strictly to prevent scope creep
5. **Not defining Out of Scope** - Absence of explicit exclusions causes endless feature expansion
6. **Creating spec without user review** - Always validate draft before saving

---

## Sources

- Template: `templates/SPEC_TEMPLATE.md` (in this skill directory)
