# TASK_111: Add crm_allowed field to SupportStatus
<!-- SUMMARY: Додати поле crm_allowed до SupportStatus для фільтрації статусів доступних CRM -->
## Complexity: simple
## Created: 2025-12-06
## Project: $HOME/epass/app/applications/customer

## Description
Додати boolean поле `crm_allowed` до моделі SupportStatus для визначення які статуси можуть бути встановлені через CRM API.

**Бізнес-цінність:**
- Контроль які статуси доступні для зовнішньої CRM
- Запобігання встановленню internal-only статусів через API

## Context
- **Related files:**
  - `app/applications/customer/models/support_status.py` - SupportStatus model
  - `app/applications/endpoints/v0/crm/views/` - CRM endpoints
  - `app/applications/customer/admin.py` - SupportStatusAdmin

- **Existing fields in SupportStatus:**
  - `name`, `category`, `process_status`, `is_active`, `order`

## Goals
1. Додати поле `crm_allowed = models.BooleanField(default=True)`
2. Створити migration
3. Додати в admin list_display та list_filter
4. Використати в CRM status validation

## Acceptance Criteria
- [ ] Поле `crm_allowed` додано до SupportStatus
- [ ] Migration створено та працює
- [ ] Admin відображає та фільтрує по полю
- [ ] CRM endpoint валідує `crm_allowed=True`
- [ ] All tests pass (`make test-dev`)

## Technical Notes

### Model Change
```python
class SupportStatus(CoreModel):
    # ... existing fields ...
    crm_allowed = models.BooleanField(
        default=True,
        verbose_name='Доступний для CRM',
        help_text='Чи може цей статус бути встановлений через CRM API'
    )
```

### Migration
```bash
docker exec app python manage.py makemigrations customer --name add_crm_allowed_to_supportstatus
```

### Admin Update
```python
class SupportStatusAdmin(admin.ModelAdmin):
    list_display = [..., 'crm_allowed']
    list_filter = [..., 'crm_allowed']
```

## Out of Scope
- UI для вибору статусу в CRM
- Validation messages customization

## Subtasks
<!-- To be filled by executor -->
- [ ] 01. TBD

## Implementation
<!-- To be filled by executor -->

## Summary
<!-- To be filled after completion -->
