# Git Flow та Branch Protection

## Branch Strategy

### Main Branch (`main`)

- **Призначення:** Стабільна версія для production
- **Захист:** Тільки через Merge Request
- **Хто мерджить:** Maintainers
- **Пайплайн:** Обов'язково успішний для мерджу

### Feature Branches (`feature/*`)

- **Призначення:** Розробка нових функцій
- **Naming:** `feature/short-description`
- **Створюють:** Developers та Maintainers
- **Мерджаться в:** `main` через MR

### Bugfix Branches (`bugfix/*`)

- **Призначення:** Виправлення багів
- **Naming:** `bugfix/issue-description`
- **Мерджаться в:** `main` через MR

---

## Права доступу

| Роль | Push до main | Створення MR | Мердж MR | Push feature/* |
|------|--------------|--------------|----------|----------------|
| Developer | ❌ | ✅ | ❌ | ✅ |
| Maintainer | ❌ | ✅ | ✅ | ✅ |

**Важливо:** Навіть Maintainers не можуть пушити напряму в `main` - тільки через MR.

---

## Workflow

### Для Developer

```bash
# 1. Оновити main
git checkout main
git pull origin main

# 2. Створити feature branch
git checkout -b feature/my-feature

# 3. Розробка + коміти
git add .
git commit -m "feat: add new feature"

# 4. Запушити branch
git push -u origin feature/my-feature

# 5. Створити MR через GitLab UI або CLI
glab mr create --title "Add new feature" --target-branch main
```

### Для Maintainer (Code Review)

```bash
# 1. Переглянути MR
glab mr view <MR_NUMBER>

# 2. Checkout MR локально (optional)
glab mr checkout <MR_NUMBER>

# 3. Якщо все OK - мердж через UI або CLI
glab mr merge <MR_NUMBER> --squash --remove-source-branch
```

---

## Налаштування Branch Protection

### GitLab API

```bash
# Захистити main branch
glab api -X POST projects/GROUP%2FPROJECT/protected_branches \
  -f name=main \
  -f push_access_level=0 \
  -f merge_access_level=40 \
  -f allow_force_push=false

# Увімкнути обов'язковий пайплайн
glab api -X PUT projects/GROUP%2FPROJECT \
  -f only_allow_merge_if_pipeline_succeeds=true \
  -f remove_source_branch_after_merge=true
```

### Access Levels

| Level | Опис |
|-------|------|
| 0 | No one |
| 30 | Developers + Maintainers |
| 40 | Maintainers only |

### Перевірка налаштувань

```bash
# Branch protection
glab api projects/GROUP%2FPROJECT/protected_branches

# Project settings
glab api projects/GROUP%2FPROJECT | jq '{
  default_branch,
  only_allow_merge_if_pipeline_succeeds,
  remove_source_branch_after_merge
}'
```

---

## Merge Request Pipeline

### Triggers

```yaml
# Запуск на MR до main
rules:
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "main"'
```

### Типовий MR Pipeline

1. **Lint** - Перевірка коду (flake8, eslint)
2. **Test** - Unit та integration тести
3. **Coverage** - Перевірка покриття
4. **Review** - Code review від Maintainer
5. **Merge** - Автоматичне видалення source branch

---

## Commit Convention

### Format

```
<type>: <short description>

[optional body]

[optional footer]
```

### Types

| Type | Опис |
|------|------|
| `feat` | Нова функціональність |
| `fix` | Виправлення бага |
| `refactor` | Рефакторинг (без зміни поведінки) |
| `docs` | Документація |
| `test` | Тести |
| `chore` | Build, CI, dependencies |

### Приклади

```bash
feat: add user authentication
fix: resolve memory leak in cache service
refactor: simplify validation logic
docs: update API documentation
test: add integration tests for payments
chore: upgrade Django to 4.2
```

---

## Rename master to main

### Локально

```bash
git branch -m master main
git push -u origin main
```

### GitLab

```bash
# Встановити main як default
glab api -X PUT projects/GROUP%2FPROJECT -f default_branch=main

# Зняти захист з master
glab api -X DELETE projects/GROUP%2FPROJECT/protected_branches/master

# Видалити master
git push origin --delete master

# Захистити main
glab api -X POST projects/GROUP%2FPROJECT/protected_branches \
  -f name=main \
  -f push_access_level=0 \
  -f merge_access_level=40
```

---

## Troubleshooting

### "You can only delete protected branches using web interface"

```bash
# Зняти захист через API
glab api -X DELETE projects/GROUP%2FPROJECT/protected_branches/BRANCH_NAME
```

### MR не можна змерджити

**Перевірити:**
1. Pipeline успішний?
2. Всі discussions resolved?
3. Є approval від Maintainer?

```bash
glab ci status
glab mr view <MR_NUMBER>
```

### Немає прав на push

**Developer** може пушити тільки в feature branches, не в main.

```bash
# Правильно
git push origin feature/my-feature

# Помилка - немає прав
git push origin main  # ❌
```
