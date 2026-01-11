---
name: sdd-writing-specifications
user-invocable: false
description: "SDD Framework: Creates spec.md through Socratic dialogue and brainstorming. Iterative refinement of ideas through questions and alternatives. Triggers on \"spec.md\", \"specification\", \"специфікація\", \"вимоги\"."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# SDD: Writing Specifications

**Communication with user: Ukrainian. Spec content: Ukrainian.**

---

## Філософія

**"Intent is the source of truth"** — специфікація є головним артефактом.

**Сократівський діалог** — через правильні питання користувач сам формулює вимоги.

**Brainstorming** — ітеративне уточнення ідей через альтернативи та trade-offs.

---

## Workflow Overview

```
PHASE 1: Brainstorm → уточнення ідеї через питання
PHASE 2: Research  → аналіз існуючого коду
PHASE 3: Clarify   → технічні деталі через діалог
PHASE 4: Draft     → секція за секцією з валідацією
PHASE 5: Review    → фінальне затвердження
```

---

## PHASE 1: Brainstorming (Сократівський діалог)

**Мета:** Витягти справжні вимоги через правильні питання.

### 1.1 Початкове розуміння

Почни з відкритого питання:
> "Розкажи про проблему, яку хочеш вирішити. Хто страждає і як?"

**НЕ переходь до рішень** — спочатку зрозумій проблему.

### 1.2 Five Whys (5 Чому)

Для кожної відповіді питай "Чому?":
```
User: "Потрібен експорт звітів"
→ Чому потрібен експорт?
User: "Бо менеджери просять дані"
→ Чому вони просять дані?
User: "Для звітності керівництву"
→ Чому не можуть дивитись в системі?
User: "Не мають доступу / незручно"
→ Ага, справжня проблема: доступ або UX
```

### 1.3 Explore Alternatives

Для кожної ідеї запропонуй альтернативи:

```markdown
**Варіант A:** {підхід 1}
- ✅ Переваги: ...
- ❌ Недоліки: ...

**Варіант B:** {підхід 2}
- ✅ Переваги: ...
- ❌ Недоліки: ...

**Варіант C:** {підхід 3}
- ✅ Переваги: ...
- ❌ Недоліки: ...

Який варіант ближче до твого бачення?
```

### 1.4 Challenge Assumptions

Питання для перевірки припущень:
- "Чи точно це потрібно для v1, чи можна відкласти?"
- "Що станеться, якщо цього НЕ робити?"
- "Хто конкретно буде цим користуватись?"
- "Як часто? Скільки даних?"
- "Що вже є в системі, що можна перевикористати?"

### 1.5 Validate Understanding

Після кожного блоку — підсумок для валідації:

```markdown
**Моє розуміння:**
1. Проблема: {X}
2. Користувачі: {Y}
3. Очікуваний результат: {Z}

Це правильно? Що пропустив?
```

---

## PHASE 2: Research Codebase

**Мета:** Знайти існуючі паттерни та уникнути дублювання.

### 2.1 Пошук релевантного коду

```bash
# Моделі
Glob: **/models.py
Grep: class.*Model

# Сервіси
Glob: **/services.py
Grep: def.*{feature_keyword}

# Існуючі фічі
Glob: aidocs/sdd/**/spec.md
```

### 2.2 Аналіз паттернів

Запитай себе:
- Чи є схожа функціональність?
- Які паттерни використовуються?
- Що можна перевикористати?

### 2.3 Поділись знахідками

```markdown
**Знайшов у codebase:**
- `app/models/Report.py` — вже є базова модель звітів
- `app/services/export.py` — існуючий експорт в CSV
- Схожа фіча: `aidocs/sdd/epass/features/analytics/`

Це впливає на наш підхід?
```

---

## PHASE 3: Clarify Details (Сократівський діалог)

**Мета:** Уточнити технічні деталі через питання, не припущення.

### 3.1 User Stories Workshop

Для кожної ролі:
```markdown
**Роль: {role}**

Як {role}, я хочу {goal}, щоб {benefit}.

Питання:
1. Як часто {role} буде це робити?
2. Що {role} робить зараз без цієї фічі?
3. Що станеться, якщо {role} не зможе це зробити?
```

### 3.2 Edge Cases через питання

Замість припущень — питання:
- "Що робити, якщо дані невалідні?"
- "Що робити при великому обсязі (1000+ записів)?"
- "Що робити при одночасному доступі?"
- "Що робити, якщо зовнішній сервіс недоступний?"

### 3.3 Priorities через trade-offs

```markdown
**Trade-off #1:** Швидкість vs Повнота
- A: Швидкий MVP без кастомізації
- B: Повна кастомізація, довше робити

**Trade-off #2:** Простота vs Гнучкість
- A: Жорстка структура, легше підтримувати
- B: Гнучка конфігурація, складніше

Що важливіше для цієї фічі?
```

---

## PHASE 4: Draft Specification (секція за секцією)

**Мета:** Створити spec.md з валідацією кожної секції.

### 4.1 Problem Statement

Напиши та покажи:
```markdown
## Problem Statement

{Опис проблеми}

**Хто страждає:** {ролі}
**Наслідки:** {що станеться без рішення}

---
Це правильно описує проблему?
```

### 4.2 User Stories

Покажи по одній:
```markdown
## User Stories

### US-1: {Назва}
Як {role}, я хочу {goal}, щоб {benefit}.

**Acceptance Criteria:**
- [ ] {criterion 1}
- [ ] {criterion 2}

---
Ця user story правильна? Додати критерії?
```

### 4.3 Functional Requirements

Покажи групами:
```markdown
## Functional Requirements

### Core
- FR-1: {requirement} — {rationale}
- FR-2: {requirement} — {rationale}

### Secondary
- FR-3: {requirement} — {rationale}

---
Вимоги повні? Щось зайве?
```

### 4.4 Out of Scope

Явно визнач межі:
```markdown
## Out of Scope

Ця фіча НЕ включає:
- {exclusion 1} — буде в майбутньому
- {exclusion 2} — окрема фіча
- {exclusion 3} — не потрібно

---
Згоден з межами?
```

---

## PHASE 5: Final Review

### 5.1 Повний документ

Покажи весь spec.md для фінального review.

### 5.2 Checklist

```markdown
**Перевірка:**
- [ ] Problem Statement зрозумілий
- [ ] User Stories конкретні
- [ ] Requirements тестуємі
- [ ] Out of Scope визначений
- [ ] Пріоритети (MoSCoW) розставлені

Готовий до затвердження?
```

### 5.3 Save

```bash
mkdir -p aidocs/sdd/{project}/features/{feature}/tasks/{todo,in_progress,done}
# Write spec.md
```

---

## Сократівські питання (шпаргалка)

**Для розуміння проблеми:**
- Яку проблему вирішуємо?
- Хто від неї страждає?
- Що станеться, якщо не вирішимо?

**Для уточнення вимог:**
- Чому це потрібно?
- Як це працює зараз?
- Що зміниться після впровадження?

**Для пріоритизації:**
- Це обов'язково для v1?
- Що важливіше: X чи Y?
- Що можна відкласти?

**Для валідації:**
- Я правильно зрозумів?
- Що пропустив?
- Що зайве?

---

## Anti-patterns

❌ **Припущення замість питань**
- Погано: "Мабуть, потрібен експорт в PDF"
- Добре: "Який формат експорту потрібен?"

❌ **Рішення до проблеми**
- Погано: "Зробимо REST API для..."
- Добре: "Яку проблему вирішуємо?"

❌ **Великі блоки без валідації**
- Погано: Весь spec одразу
- Добре: Секція → валідація → наступна секція

❌ **Ігнорування "не знаю"**
- Погано: Пропустити питання
- Добре: Записати в Open Questions

---

## Output

```
aidocs/sdd/{project}/features/{feature}/spec.md
```

**Next:** Після approve → `sdd-writing-design-docs`

---

## Self-Updating

Repository: `~/.claude/claudedm/` (faionfaion/claudedm)

```bash
cp -r ~/.claude/claudedm/skills/sdd-writing-specifications ~/.claude/skills/
```

---

## Documentation

- [Skills](https://code.claude.com/docs/en/skills)
- [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
