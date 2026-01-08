# TASK_085: Implement Timeline Event Services and Triggers
<!-- SUMMARY: Створити сервіси для генерації Timeline подій та інтегрувати в trigger points -->
## Complexity: normal
## Created: 2025-11-28
## Project: /home/moskalyuk_ruslan/epass

## Description
Створити сервіси для генерації Timeline подій та інтегрувати їх у всі точки в коді де відбуваються відповідні події.

**Бізнес-цінність:**
- Audit trail для всіх дій з клієнтами
- Історія змін статусів звернень
- Відстеження lifecycle карток

**Scope:**
- 15 типів подій (customer, support, card lifecycle)
- Auto-generation descriptions
- Integration з existing signals та admin actions

## Context
- **Depends on:** TASK_082 (Timeline model)

- **Related files:**
  - `app/applications/customer/models/customer.py` - Customer creation/group changes
  - `app/applications/customer/models/card_nfc.py` - NFC card lifecycle
  - `app/applications/customer/models/support.py` - Support lifecycle
  - `app/applications/customer/admin.py` - Admin actions

- **Existing patterns:**
  - Functional services: `app/applications/*/services/`
  - Django signals для post_save events

## Goals
1. Створити `timeline_service.py` з функціями для всіх event types
2. Auto-generation description для кожного типу
3. Інтегрувати STATUS_CHANGED в SupportAdmin
4. Підготувати integration points для майбутнього

## Acceptance Criteria
- [ ] Створено `app/applications/customer/services/timeline_service.py`
- [ ] 15 service functions з docstrings та type hints:
  - `create_customer_created_event(customer, created_by_email, text='')`
  - `create_group_changed_event(customer, old_group, new_group, ...)`
  - `create_status_changed_event(support, old_status, new_status, ...)`
  - `create_card_blocked_event(card, reason, blocked_by_email, ...)`
  - (... решта функцій)
- [ ] Helper function `_get_card_display_info(card)`
- [ ] Logging для кожної події
- [ ] STATUS_CHANGED інтегровано в SupportAdmin
- [ ] Компіляція проходить (`python -m compileall`)
- [ ] All tests pass (`make test-dev`)

## Technical Notes

### Service Function Pattern
```python
def create_status_changed_event(
    support: customer_models.Support,
    old_status: customer_models.SupportStatus,
    new_status: customer_models.SupportStatus,
    changed_by_email: str = '',
    text: str = '',
) -> customer_models.Timeline:
    """Create STATUS_CHANGED event.

    Args:
        support: Support instance
        old_status: Previous status
        new_status: New status
        changed_by_email: Email of user who changed
        text: Optional comment

    Returns:
        Timeline event
    """
    description = f"Статус змінено: {old_status.name} → {new_status.name}"

    event = customer_models.Timeline.objects.create(
        customer=support.customer,
        support=support,
        event_type=customer_models.Timeline.EVENT_TYPE.STATUS_CHANGED,
        description=description,
        text=text,
        author_email=changed_by_email,
        metadata={...}
    )

    logger.info(f"Timeline event: STATUS_CHANGED for support {support.uid}")
    return event
```

### Integration Example
```python
# In SupportAdmin.save_model
if old_status != obj.status:
    timeline_service.create_status_changed_event(
        support=obj,
        old_status=old_status,
        new_status=obj.status,
        changed_by_email=request.user.email,
        text=request.POST.get('status_change_message', ''),
    )
```

## Out of Scope
- Frontend UI для Timeline
- Real-time notifications
- Export Timeline to CSV

## Subtasks
<!-- To be filled by executor -->
- [ ] 01. TBD

## Implementation
<!-- To be filled by executor -->

## Summary
<!-- To be filled after completion -->
