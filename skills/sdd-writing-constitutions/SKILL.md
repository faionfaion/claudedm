---
name: sdd-writing-constitutions
user-invocable: false
description: "SDD Framework: Creates constitution.md through codebase analysis OR Socratic dialogue for new projects. Triggers on \"constitution.md\", \"constitution\", \"конституція проекту\", \"стандарти проекту\"."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Bash(cat:*), Bash(git log:*), AskUserQuestion
---

# SDD: Writing Constitutions

**Communication with user: Ukrainian. Constitution content: Ukrainian.**

---

## Філософія

**Constitution.md** — незмінні принципи проекту для ВСІХ фіч.

**Два режими:**
1. **Existing Project** → аналіз codebase
2. **New Project** → Сократівський діалог + brainstorming

---

## Workflow Overview

```
┌─ Existing codebase? ─┐
│                      │
▼ YES                  ▼ NO
ANALYZE                BRAINSTORM
├─ Structure           ├─ Vision
├─ Tech Stack          ├─ Tech choices
├─ Patterns            ├─ Architecture
├─ Standards           ├─ Standards
└─ Draft               └─ Draft
        │                    │
        └──────┬─────────────┘
               ▼
          REVIEW & SAVE
```

---

## MODE 1: Existing Project (Аналіз)

### Phase 1: Detect Project

```bash
# Check if codebase exists
ls {project_path}/
```

Якщо є код → MODE 1 (аналіз)
Якщо немає → MODE 2 (brainstorm)

### Phase 2: Analyze Structure

- Directory layout (2 levels)
- CLAUDE.md, README.md
- Config files (pyproject.toml, package.json, etc.)

### Phase 3: Identify Tech Stack

- Language version
- Framework version
- Database
- Key dependencies

### Phase 4: Analyze Patterns

- Architecture (layers, DDD, etc.)
- Naming conventions
- Linters, formatters
- Testing practices

### Phase 5: Draft from Analysis

Покажи знахідки та склади constitution:
```markdown
**Аналіз {project}:**

1. Tech Stack: Python 3.11, Django 4.2, PostgreSQL
2. Architecture: Layered (views → services → models)
3. Standards: black + isort + flake8
4. Testing: pytest, 80%+ coverage

Це відповідає реальності? Що додати/змінити?
```

---

## MODE 2: New Project (Brainstorming)

### Phase 1: Vision (Сократівський діалог)

Почни з відкритого питання:
> "Розкажи про проект, який плануєш. Яку проблему він вирішує?"

**Five Whys:**
```
User: "Це буде CRM система"
→ Чому потрібна нова CRM?
User: "Існуючі не підходять"
→ Чому не підходять?
User: "Немає інтеграції з X"
→ Що конкретно потрібно від інтеграції?
```

### Phase 2: Tech Choices (Alternatives)

Для кожного рішення — альтернативи:

```markdown
**Backend Framework:**

A: **Django** (Python)
   ✅ Batteries included, ORM, admin
   ❌ Monolithic, може бути повільним

B: **FastAPI** (Python)
   ✅ Швидкий, async, modern
   ❌ Менше готових рішень

C: **NestJS** (TypeScript)
   ✅ Enterprise patterns, TypeScript
   ❌ Складніший setup

Який підхід ближче?
```

```markdown
**Database:**

A: **PostgreSQL**
   ✅ Надійний, JSON support, розширення
   ❌ Складніший ніж SQLite

B: **MongoDB**
   ✅ Гнучка схема, швидкий старт
   ❌ Складні транзакції

C: **SQLite**
   ✅ Zero config, embedded
   ❌ Не для production з навантаженням

Який вибір?
```

### Phase 3: Architecture (Trade-offs)

```markdown
**Trade-off #1:** Monolith vs Microservices
- A: Monolith — простіше, швидший старт
- B: Microservices — масштабованість, складніше

**Trade-off #2:** REST vs GraphQL
- A: REST — простіше, стандарт
- B: GraphQL — гнучкість, один endpoint

**Trade-off #3:** ORM vs Raw SQL
- A: ORM — швидша розробка
- B: Raw SQL — повний контроль

Що обираєш?
```

### Phase 4: Standards (Питання)

```markdown
**Code Style:**
- Який linter? (eslint, flake8, none)
- Який formatter? (prettier, black, none)
- Type hints обов'язкові?

**Testing:**
- Який рівень coverage потрібен?
- Unit tests обов'язкові?
- E2E tests?

**Git:**
- Conventional commits?
- Branch naming?
- PR reviews обов'язкові?
```

### Phase 5: Validate Vision

```markdown
**Моє розуміння проекту:**

1. **Мета:** {what problem it solves}
2. **Tech Stack:** {chosen technologies}
3. **Architecture:** {chosen patterns}
4. **Standards:** {coding standards}

Це правильно? Що пропустив?
```

---

## Draft Constitution (обидва режими)

### Секція за секцією з валідацією

**Overview:**
```markdown
## Overview

**Тип:** {project type}
**Мета:** {purpose}
**Власник:** {owner}

---
Правильно?
```

**Technology Stack:**
```markdown
## Technology Stack

| Технологія | Версія | Призначення |
|------------|--------|-------------|
| {lang} | {ver} | Core |
| {framework} | {ver} | Backend |
| {db} | {ver} | Database |

---
Все вказано?
```

**Architecture:**
```markdown
## Architecture Patterns

- **Pattern:** {layered/DDD/microservices}
- **Structure:** {description}

---
Відповідає баченню?
```

**Standards:**
```markdown
## Code Standards

- **Linter:** {tool}
- **Formatter:** {tool}
- **Types:** {required/optional}
- **Testing:** {requirements}

---
Згоден?
```

---

## Final Review

```markdown
**Checklist:**
- [ ] Overview зрозумілий
- [ ] Tech Stack повний
- [ ] Architecture визначена
- [ ] Standards конкретні
- [ ] Testing requirements є

Готовий до затвердження?
```

---

## Save

```bash
mkdir -p aidocs/sdd/{project_name}
# Write constitution.md
```

---

## Сократівські питання (шпаргалка)

**Для нового проекту:**
- Яку проблему вирішуємо?
- Хто буде користуватись?
- Які обмеження (бюджет, час, команда)?
- Чому саме ця технологія?
- Що буде через рік?

**Для existing проекту:**
- Чому обрали цей паттерн?
- Що працює добре?
- Що хотіли б змінити?
- Які болючі точки?

---

## Anti-patterns

❌ **Копіювання без розуміння**
- Погано: "Візьмемо як в іншому проекті"
- Добре: "Чому цей підхід підходить саме нам?"

❌ **Over-engineering на старті**
- Погано: "Microservices з перших днів"
- Добре: "Почнемо з monolith, розділимо коли потрібно"

❌ **Ігнорування команди**
- Погано: "Візьмемо Rust" (ніхто не знає)
- Добре: "Яка експертиза в команді?"

---

## Output

```
aidocs/sdd/{project_name}/constitution.md
```

**Next:** → `sdd-writing-specifications` для першої фічі

---

## Self-Updating

Repository: `~/.claude/claudedm/` (faionfaion/claudedm)

```bash
cp -r ~/.claude/claudedm/skills/sdd-writing-constitutions ~/.claude/skills/
```

---

## Documentation

- [Skills](https://code.claude.com/docs/en/skills)
- [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
