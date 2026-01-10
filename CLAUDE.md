# FinRay - Claude Code Instructions

## Documentation Standards

### Формати для структурованої інформації

**Використовуй таблиці:**
```markdown
| Компонент | Призначення | Приклад |
|-----------|-------------|---------|
| services/ | Бізнес-логіка | UserService |
| models/ | Доменні моделі | User, Order |
```

**Використовуй ієрархічні списки:**
```markdown
## Архітектура

### Шари
1. **UI Layer** → викликає → Service Layer
2. **Service Layer** → викликає → Repository Layer
3. **Repository Layer** → працює з → Database

### Залежності
- `components/` залежить від `services/`
- `services/` залежить від `lib/`
- `lib/` не має залежностей (портативний)
```

**Використовуй code blocks для структур:**
```markdown
project/
├── src/
│   ├── components/    # UI компоненти
│   ├── services/      # Бізнес-логіка
│   └── lib/           # Портативні утиліти
└── tests/
```

### Заборонені формати

**НЕ використовуй ASCII діаграми:**
```
# ПОГАНО - важко парсити, неоднозначно
┌─────────────┐
│   UI Layer  │
└──────┬──────┘
       │
┌──────▼──────┐
│  Services   │
└─────────────┘
```

**Замість цього:**
```markdown
# ДОБРЕ - чітко і однозначно
## Data Flow
1. UI Layer отримує user input
2. UI викликає Service з параметрами
3. Service обробляє та повертає результат
4. UI відображає результат
```

### Патерни опису архітектури

**Залежності між модулями:**
```markdown
| Модуль | Залежить від | Не залежить від |
|--------|--------------|-----------------|
| UI | Services, Types | Database |
| Services | Lib, Types | UI |
| Lib | Types only | UI, Services, Database |
```

**Flow даних:**
```markdown
## Request Flow
1. `Controller` приймає HTTP request
2. `Controller` → `Service.method(dto)`
3. `Service` → `Repository.query()`
4. `Repository` → Database
5. Response повертається тим же шляхом
```

**Умовна логіка:**
```markdown
## Rule Processing
- IF rule.type = REGULAR → використовуй RegularValidator
- IF rule.type = TRACEABLE → використовуй TraceableValidator
- IF validation.failed → return errors
- ELSE → proceed to generation
```

## SDD Documentation Paths

```
/aidocs/sdd/{project}/
├── constitution.md                        # Принципи проекту
└── features/{feature}/
    ├── spec.md                            # Специфікація
    ├── design.md                          # Технічний дизайн
    └── tasks/{todo,in_progress,done}/     # Задачі
```
