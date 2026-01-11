---
user-invocable: true
name: make-docs
description: Creates, edits, updates, or modifies AGENTS.md/CLAUDE.md documentation for Django modules. Use when user asks to create docs, edit docs, update documentation, document module, add AGENTS.md. Triggers on "AGENTS.md", "CLAUDE.md", "documentation", "документація".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*), Bash(ln:*), Bash(ls:*), Bash(wc:*)
---

# Creating or Updating AI Documents

**Communication with user: Ukrainian. Document content: English.**

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create AGENTS.md for a module
- Edit/update/change/modify existing documentation
- Create CLAUDE.md symlink
- Update module documentation
- Document a Django app

**Trigger phrases:** "create AGENTS.md", "edit documentation", "update docs", "document module", "створити документацію", "оновити AGENTS.md", "задокументувати модуль"

---

## Purpose

Creates standardized AI-readable documentation for Django modules following E-Pass conventions:
- AGENTS.md (main navigation)
- Symlinks (CLAUDE.md, GEMINI.md)
- Supporting docs (MODELS.md, PROCESSES.md, API.md)

---

## Input

- `module_path` - path to Django module (e.g., `app/applications/customer`)
- Or module name for discovery

---

## Document Types

**Required in `module/`:**
- AGENTS.md - navigation hub
- CLAUDE.md - symlink to AGENTS.md
- GEMINI.md - symlink to AGENTS.md

**Optional in `module/docs/`:**
- MODELS.md - model details (if models exist)
- PROCESSES.md - business processes (if services exist)
- API.md - API endpoints (if views exist)

---

## Size Limits

- Root AGENTS.md: 100-150 lines (max 200)
- Domain AGENTS.md: 80-120 lines (max 150)
- docs/*.md: 50-150 lines (max 200)

**Key principle:** Context window is shared resource. Every line must earn its place.

---

## Workflow

### Phase 1: Analyze Module

Research the module to understand:

1. **Models** - Read `models.py` or `models/` directory
2. **Services** - Read `services.py` or `services/` directory
3. **Views/API** - Read `views.py`, `viewsets.py`
4. **Tasks** - Read `tasks.py` for Celery tasks
5. **Constants** - Read `constants.py`

Document findings before writing.

### Phase 2: Create Directory Structure

```bash
mkdir -p {module_path}/docs
```

### Phase 3: Write AGENTS.md

Follow template structure (see below). Include only:
- Purpose (1-2 sentences)
- Business value (2-3 points)
- Documentation links table
- Key models table (name + one-line purpose)
- Key processes (numbered, with flow arrows)
- Celery tasks table (if any)
- Import examples

### Phase 4: Create Symlinks

```bash
cd {module_path}
ln -sf AGENTS.md CLAUDE.md
ln -sf AGENTS.md GEMINI.md
```

### Phase 5: Write Supporting Docs

Create only needed docs based on module content:

- **MODELS.md** - if module has models
- **PROCESSES.md** - if module has services/business logic
- **API.md** - if module has API endpoints

### Phase 6: Verify

Check:
- All symlinks work
- Line counts within limits
- Tables render correctly
- Links are valid

---

## AGENTS.md Template

```markdown
# {Module Name} - Short description (max 10 words)

## Purpose
1-2 sentences explaining what this module does.

## Business Value
- Value point 1
- Value point 2
- Value point 3

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/MODELS.md](docs/MODELS.md) | Model fields and relationships |
| [docs/PROCESSES.md](docs/PROCESSES.md) | Business processes and workflows |
| [docs/API.md](docs/API.md) | API endpoints documentation |

---

## Key Models

| Model | Purpose |
|-------|---------|
| **ModelName** | One-line description |
| **OtherModel** | One-line description |

---

## Key Processes

1. **Process Name** → step1 → step2 → result
2. **Other Process** → action → validation → outcome

---

## Celery Tasks

| Task | Description |
|------|-------------|
| `task_name` | What it does |

---

## Imports

\`\`\`python
from applications.{module} import models as {module}_models
from applications.{module} import constants as {module}_constants
from applications.{module} import services as {module}_services
\`\`\`
```

---

## docs/MODELS.md Template

```markdown
# {Module} Models

## ModelName (Українська назва)

**Purpose**: One sentence explaining the model's role.

| Field | Type | Description |
|-------|------|-------------|
| `field_name` | FieldType | Short description |
| `other_field` | ForeignKey | Link to OtherModel |

**Key Features**:
- Feature 1
- Feature 2

**Indexes**: `field1`, `(field1, field2)`

---

## OtherModel (Українська назва)

...
```

---

## docs/PROCESSES.md Template

```markdown
# {Module} Business Processes

## Process Name

**Function**: `service_function()`
**File**: `services/{file}.py:line`

\`\`\`
Input → Validation → Processing → Result
\`\`\`

### Steps:
1. Step description
2. Step description
3. Step description

### Edge Cases:
- Case 1: handling
- Case 2: handling

---

## Other Process

...
```

---

## docs/API.md Template

```markdown
# {Module} API Endpoints

## POST /api/v1/{resource}/

**Purpose**: What this endpoint does

**Request**:
\`\`\`json
{
  "field": "value"
}
\`\`\`

**Response** (200):
\`\`\`json
{
  "id": 1,
  "status": "success"
}
\`\`\`

**Errors**:
- 400: Validation error
- 404: Resource not found

---

## GET /api/v1/{resource}/{id}/

...
```

---

## Degrees of Freedom

The skill implementer decides:
- **High**: Which processes to document (select most important)
- **Medium**: Level of detail in model descriptions
- **Low**: Template structure and symlink creation (must follow exactly)

---

## Failed Attempts

- **Copying all model fields** - AGENTS.md too long → only key fields, full list in MODELS.md
- **Documenting implementation** - changes fast, outdates → document purpose and flow
- **Skipping symlinks** - Claude/Gemini can't find → always create both
- **One huge AGENTS.md** - exceeds budget → split into docs/ files
- **Duplicating parent info** - wastes tokens → reference parent, don't repeat

---

## What NOT to Include in AGENTS.md

- AI tool instructions (already in system prompt)
- Complete code examples (put in docs/)
- Parent-level information (avoid duplication)
- Operational workflows (separate files)
- Full command lists (use README.md)

---

## Verification Checklist

Before completion:
- [ ] AGENTS.md exists and follows template
- [ ] CLAUDE.md symlink works (`ls -la` shows `-> AGENTS.md`)
- [ ] GEMINI.md symlink works
- [ ] docs/ directory created
- [ ] MODELS.md created (if models exist)
- [ ] PROCESSES.md created (if services exist)
- [ ] API.md created (if endpoints exist)
- [ ] Line counts within limits
- [ ] All internal links valid

---

## Output

Files created in module directory:
```
{module_path}/
├── AGENTS.md           # Main documentation
├── CLAUDE.md           # Symlink → AGENTS.md
├── GEMINI.md           # Symlink → AGENTS.md
└── docs/
    ├── MODELS.md       # Model details
    ├── PROCESSES.md    # Business processes
    └── API.md          # API endpoints
```

---

## Sources

- Guidelines: `epass/DOCUMENTATION_GUIDELINES.md`
- Example: `epass/app/applications/customer/AGENTS.md`
- E-Pass conventions: `epass/AGENTS.md`
