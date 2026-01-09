---
description: Code review of current branch against main for specified project
argument-hint: [project-dir]
---

# Code Review Command

Perform a comprehensive code review for the project **$ARGUMENTS**.

## Execution Method

Use the Task tool to spawn a dedicated agent for this code review.

Parameters:
- `subagent_type`: "general-purpose"
- `description`: "Code review for $ARGUMENTS"
- `prompt`: Include all instructions below

This ensures thorough analysis without context limitations.

## Context

1. Navigate to project directory: `$HOME/$ARGUMENTS`
2. Identify current branch and compare it with `main`
3. Get list of all changed files: `git diff main...HEAD --name-only`
4. Get full diff: `git diff main...HEAD`

## Code Review Criteria

Analyze ALL changes according to the following criteria:

---

### 1. CRITICAL

#### 1.1 Code Correctness
- Logic errors and edge cases
- Algorithm and business logic correctness
- Potential runtime errors
- None/null handling

#### 1.2 Test Quality

Tests must test actual code, not just pass.

Check each test for:
- **Real assertions**: does it verify the result of code execution
- **Code connection**: does the test actually call the code being tested
- **Mock abuse**: is too much mocked (test tests mocks, not code)
- **Trivial tests**: `assert True`, `assert response.status_code` without checking value
- **Empty tests**: test exists but verifies nothing

Examples of BAD tests:
```python
# BAD: mocks everything, only tests that mock was called
@patch('module.function')
def test_something(mock_func):
    mock_func.return_value = 'expected'
    result = some_code()
    mock_func.assert_called_once()  # Doesn't check result!

# BAD: trivial assert
def test_view(self):
    response = self.client.get('/api/endpoint/')
    self.assertTrue(response)  # What exactly are we checking?

# BAD: test without assertions
def test_function(self):
    result = calculate_something(5)
    # Where's the assert?
```

Examples of GOOD tests:
```python
# GOOD: checks actual result
def test_calculate_discount(self):
    result = calculate_discount(price=100, percent=20)
    assert result == 80

# GOOD: checks specific data in response
def test_user_detail_api(self):
    response = self.client.get(f'/api/users/{self.user.id}/')
    assert response.status_code == 200
    assert response.data['email'] == 'test@example.com'
    assert 'password' not in response.data
```

Test checklist:
- [ ] Test calls real code (not just mocks)
- [ ] Has assertions that check results
- [ ] Assertions verify specific values
- [ ] Edge cases covered (None, empty list, negative numbers)
- [ ] Test will fail if code breaks

#### 1.3 Security
- SQL injection (raw queries, extra(), RawSQL)
- XSS vulnerabilities (mark_safe, |safe in templates)
- Secrets/credentials in code
- Access rights (permissions, authentication)
- CSRF protection
- Unsafe deserialization

#### 1.4 Breaking Changes
- Changes in API endpoints (URL, methods, parameters)
- Changes in response format
- Removal/renaming of public methods
- Migrations that could break production data

---

### 2. STYLE AND CONVENTIONS

#### 2.1 Code Style
- Compliance with project's black/isort/flake8 configuration
- Line length
- Imports (order, grouping)
- Trailing whitespace, blank lines

#### 2.2 Naming Conventions
- snake_case for functions/variables
- PascalCase for classes
- UPPER_CASE for constants
- Clear, descriptive names (not `x`, `temp`, `data`)
- Consistency with existing code

#### 2.3 Project Architectural Patterns
- Apps structure (models, views, serializers, services)
- Business logic in correct place (not in views)
- Using services for complex logic
- Proper separation of responsibilities

#### 2.4 Django Best Practices
- Optimal ORM queries (select_related, prefetch_related)
- Proper use of managers and querysets
- Signals (are they really needed?)
- Form/Serializer validation
- Proper use of transactions

---

### 3. CODE QUALITY

#### 3.1 Complexity
- Cyclomatic complexity (many if/else)
- Deep nesting (> 3 levels)
- Long functions (> 50 lines)
- Long classes (> 300 lines)
- Many function parameters (> 5)

#### 3.2 Error Handling
- Too broad try/except (bare except)
- Error logging (with sufficient context)
- User-friendly error messages
- Graceful degradation

#### 3.3 Documentation
- Docstrings for public methods/classes
- Comments for non-obvious logic
- README updated if needed
- Type hints for complex functions

---

### 4. PERFORMANCE AND DEVOPS

#### 4.1 N+1 Queries
- Loops with ORM queries inside
- Missing select_related/prefetch_related
- Using .all() where .only()/.defer() needed
- Queries in serializers without optimization

#### 4.2 Migrations
- Are there migrations for model changes
- Reversible migrations (operations vs reverse)
- Data migrations separate from schema migrations
- RunPython with batch processing for large tables
- Indexes for new fields with filtering

#### 4.3 Celery Tasks
- Idempotency (safe to restart?)
- Retry logic with exponential backoff
- Timeouts set
- Error handling and logging
- Atomicity (transactions where needed)

#### 4.4 Dependencies
- New packages in requirements
- Versions pinned (not `>=`, but `==`)
- Package security (known vulnerabilities)
- Is the new dependency really needed

---

### 5. ADDITIONAL

#### 5.1 TODO/FIXME
- Incomplete code with TODO
- FIXME that need attention
- Hacks and temporary solutions
- Commented out code (delete it!)

#### 5.2 Type Hints
- Annotations for public functions
- Consistency (if present - then everywhere)
- Correct types (Optional, Union, etc.)

#### 5.3 API Contracts
- Swagger/OpenAPI documentation updated
- Serializers match API spec
- API versioning (if breaking change)
- Response codes are correct

---

## Response Format

The final report MUST be written in Ukrainian language.

### Резюме
Brief description of what was changed (2-3 sentences).

### Статистика
- Файлів змінено: X
- Рядків додано: +Y
- Рядків видалено: -Z

### Критичні проблеми
Issues that BLOCK merge. Format:
```
[CRITICAL] file:line - problem description
  Причина: why this is critical
  Рішення: how to fix
```

### Важливі зауваження
Issues RECOMMENDED to fix. Format:
```
[IMPORTANT] file:line - description
  Рекомендація: what to do
```

### Незначні зауваження
Suggestions for improvement. Format:
```
[MINOR] file:line - description
```

### Позитивні моменти
What was done well (2-3 points).

### Чеклист перед merge
- [ ] Критичні проблеми виправлені
- [ ] Тести проходять
- [ ] Міграції перевірені
- [ ] Code style відповідає стандартам

---

## Important Notes

- Be specific: specify file and line
- Suggest solutions, not just criticize
- Consider project context (Django, E-Pass)
- Check @$ARGUMENTS/CLAUDE.md for project-specific rules
- If no changes (branch = main), report this
- ALL OUTPUT MUST BE IN UKRAINIAN

---

## Sources

- Claude Code Custom Slash Commands: https://docs.anthropic.com/en/docs/claude-code/tutorials/custom-slash-commands
- Claude Code Best Practices: https://docs.anthropic.com/en/docs/claude-code/best-practices
