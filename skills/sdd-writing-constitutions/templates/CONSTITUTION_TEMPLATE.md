# Constitution Template

Шаблон для `constitution.md` проекту.

---

## Вимоги

**Обов'язкові розділи:**
- **Overview** — що це за проект
- **Technology Stack** — мови, фреймворки, інфра

**Опціональні (бажані):**
- Code Standards
- Architecture Patterns
- Testing Requirements

**Опціональні (за потребою):**
- Стандарти (API, Database, Git, Logging...)
- Обмеження (Security, Rate limits...)
- Нефункціональні вимоги (Performance, Scalability...)

---

## Шаблон

```markdown
# Project Constitution: {Project Name}

> Незмінні принципи проекту

## Overview

{Короткий опис проекту — що це, для кого, основна функція}

---

## Technology Stack

- **Language**: {мова програмування}
- **Framework**: {фреймворк}
- **Database**: {база даних}
- **Cache**: {кеш, якщо є}
- **Queue**: {черга задач, якщо є}
- **API**: {API framework}
- **Containers**: {Docker, K8s...}
- **CI/CD**: {система CI/CD}

---

## Code Standards

{Стиль коду, naming conventions, linters}

---

## Architecture Patterns

{Архітектурні патерни, layered architecture, patterns}

---

## Testing Requirements

{Coverage вимоги, типи тестів, стандарти}

---

## {Інші секції за потребою}

- API Standards
- Database Guidelines
- Security
- Git Workflow
- Logging & Monitoring
- Performance

---

*Last updated: {date}*
```
