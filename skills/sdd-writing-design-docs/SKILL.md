---
name: sdd-writing-design-docs
description: "SDD Framework: Creates, edits, or updates design.md with technical implementation. Use when user asks to create design, edit design, update design document, write technical design. Triggers on \"design.md\", \"design document\", \"дизайн документ\", \"технічний дизайн\"."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# SDD: Writing Design Documents

**Communication with user: Ukrainian. Design content: Ukrainian.**

---

## SDD Framework Overview

Цей скіл є частиною **Spec-Driven Development (SDD)** фреймворку.

### Філософія SDD

**"Intent is the source of truth"** — специфікація є головним артефактом, код — лише її реалізація.

### SDD Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: SPECIFICATION (Human + AI)                            │
│  → Скіл: sdd-writing-specifications                            │
│  Output: spec.md (status: approved)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: DESIGN (AI-assisted) ← ВИ ТУТ                        │
│                                                                 │
│  1. Прочитати approved spec.md                                 │
│  2. Прочитати constitution.md                                   │
│  3. Дослідити codebase                                          │
│  4. Написати design.md (цей скіл)                              │
│  5. Review & approve                                            │
│                                                                 │
│  Output: design.md (approved)                                   │
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
$HOME/aidocs/sdd/
├── CLAUDE.md                          # SDD overview
├── SDD_WORKFLOW.md                    # Детальний workflow
├── SPEC_TEMPLATE.md                   # Шаблон spec.md
├── DESIGN_TEMPLATE.md                 # Шаблон design.md ← використовуй!
├── CONSTITUTION_TEMPLATE.md           # Шаблон constitution.md
├── TASK_EXECUTION.md                  # Процес виконання тасків
└── {project}/                         # epass, billing, etc.
    ├── constitution.md                # Принципи проекту ← читай!
    └── features/
        └── {feature-name}/            # kebab-case
            ├── spec.md                # ЩО і ЧОМУ ← читай!
            ├── design.md              # ЯК ← створюємо тут
            └── tasks/                 # Задачі
                ├── todo/
                ├── in_progress/
                └── done/
```

### Key SDD Documents

| Document | Призначення | Статус |
|----------|------------|--------|
| `constitution.md` | Принципи проекту | ЧИТАТИ перед design |
| `spec.md` | ЩО і ЧОМУ | ЧИТАТИ, має бути approved |
| `design.md` | ЯК реалізувати | СТВОРЮЄМО цим скілом |
| `TASK_*.md` | Атомарні задачі | Створюються після design |

---

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create design.md for a feature
- Edit/update/change/modify existing design document
- Write technical design based on spec
- Add architecture decisions to design

**Trigger phrases:** "create design", "edit design", "update design.md", "write design document", "створити дизайн", "оновити design.md", "написати технічний дизайн"

---

## Purpose

Creates design.md for a feature based on:
1. Approved spec.md
2. Codebase analysis
3. Project constitution

## Input

- `feature_path` - path to feature directory (contains spec.md)

Or:
- `project` - project name
- `feature` - feature name

## Prerequisites

Before starting, verify:

```bash
SDD_BASE="$HOME/aidocs/sdd"

# 1. spec.md exists with status approved
cat ${SDD_BASE}/{project}/features/{feature}/spec.md | grep -A1 "Status"

# 2. constitution.md exists
cat ${SDD_BASE}/{project}/constitution.md
```

**Required files:**
1. `spec.md` exists with status `approved`
2. Project `constitution.md` exists at `$HOME/aidocs/sdd/{project}/constitution.md`

**If constitution.md doesn't exist:** Use скіл `sdd-writing-constitutions` to create it first.

## Workflow

### Phase 1: Read Specification

Read spec.md completely and extract:
- Problem Statement
- User Stories
- Functional Requirements
- API Contract (if present)
- Data Model (if present)
- Out of Scope

### Phase 2: Read Constitution

Read project principles from constitution.md and extract:
- Architecture patterns
- Code standards
- Testing requirements

### Phase 3: Research Codebase

Use Grep and Glob tools to find related code:
- Similar models in `$HOME/epass/app/applications/`
- Similar services (services.py files)
- Similar views (views.py files)
- Existing patterns

Determine:
- Which components can be reused
- Which patterns are in use
- Where to place new code

### Phase 4: Architecture Decisions

For each key decision:
1. Define context - what problem are we solving
2. List options - minimum 2 alternatives
3. Choose solution - which and why
4. Document rationale - reasoning behind choice

Typical decisions include:
- Business logic placement (new service vs existing)
- Model structure (new vs extend existing)
- Pattern selection
- Error handling approach

### Phase 5: Define Technical Approach

Define:
1. **Components** - new components, interactions, diagrams if complex
2. **Data Flow** - data path through system, validation points, error handling
3. **Files** - CREATE and MODIFY lists with scope

### Phase 6: Define Testing Strategy

Based on constitution:
1. Unit tests - isolated testing targets
2. Integration tests - flow coverage
3. Test data - required fixtures

### Phase 7: Identify Risks

For each risk document:
- Risk description
- Impact (High/Medium/Low)
- Mitigation strategy

### Phase 8: Review with User

Present key decisions:
1. Architecture Decisions - agreement check
2. Technical Approach - better alternatives
3. Risks - completeness check

### Phase 9: Save Design

Save design.md to feature directory: `{feature_path}/design.md`

## Architecture Decision Template

```
### AD-{N}: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen solution}

**Rationale:** {Why this solution, influencing factors}

**Failed Attempts:** {Optional - approaches tried and rejected during analysis}
```

## Files Section Format

```
### Files

app/applications/{app}/models.py           # MODIFY - add {Model}
app/applications/{app}/services.py         # MODIFY - add {Service}
app/applications/{app}/views.py            # MODIFY - add {ViewSet}
app/applications/{app}/serializers.py      # MODIFY - add {Serializer}
app/applications/{app}/tests/test_{x}.py   # CREATE - tests for {x}
```

## Failed Attempts Section

Document approaches that were considered but rejected:

```
### Failed Attempts

1. **{Approach Name}** - {Why it was rejected}
2. **{Approach Name}** - {Why it was rejected}
```

This section helps future developers understand why certain paths were not taken.

## Output

File `design.md` at:
```
$HOME/aidocs/sdd/{project}/features/{feature}/design.md
```

**Next step:** Після approve design.md → використовуй `/maketasks` для створення TASK_*.md файлів

## Checklist Before Completion

- All FR from spec.md covered
- Architecture Decisions have rationale
- Files list is complete
- Testing strategy defined
- Risks identified
- Follows constitution
- User approved

## Sources

- Project spec.md
- Project constitution.md
- Template: `templates/DESIGN_TEMPLATE.md` (in this skill directory)
