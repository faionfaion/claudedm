# TASK_104: CRM Inbound Webhooks for Support updates
<!-- SUMMARY: Створити webhook endpoints для прийому оновлень від CRM: нові повідомлення, зміна статусу, призначення -->
## Complexity: complex
## Created: 2025-12-04
## Project: /home/moskalyuk_ruslan/epass/app/applications/endpoints/v0/crm

## Description
Реалізувати систему webhook endpoints для прийому оновлень від зовнішньої CRM системи.

**Бізнес-цінність:**
- Синхронізація статусів звернень між E-Pass та CRM
- Автоматичне оновлення Timeline при діях в CRM
- Audit trail для compliance

**Підтримувані події:**
1. **message.created** - коментар від CRM оператора
2. **status.changed** - зміна статусу звернення
3. **agent.assigned** - призначення відповідального
4. **priority.changed** - зміна пріоритету
5. **tags.updated** - оновлення тегів
(... всього 12 типів подій)

**Безпека:**
- HMAC-SHA256 webhook signature verification
- Idempotency key processing
- Rate limiting (100 req/min per CRM)

## Context
- **Related models**:
  - `app/applications/customer/models/support.py` - Support, SupportStatus
  - `app/applications/customer/models/timeline.py` - Timeline для audit
  - `app/applications/customer/models/crm_exchange_log.py` - логування обміну

- **Existing patterns**:
  - Celery tasks для async processing: `app/applications/customer/tasks/`
  - DRF serializers: `app/applications/endpoints/v0/crm/serializers/`

- **External integration**:
  - CRM API documentation: [internal wiki link]
  - Signature algorithm: HMAC-SHA256(payload + timestamp, secret)

- **Related tasks**:
  - TASK_102 (Support endpoints) - prereq
  - TASK_105 (Outbound webhooks) - follow-up

## Goals
1. POST `/api/v0/crm/webhooks/support/` endpoint
2. Security layer (signature, rate limiting, idempotency)
3. Celery tasks для кожного event type
4. CRMExchangeLog audit trail
5. Error handling з retry logic

## Acceptance Criteria
### Webhook Endpoint
- [ ] POST `/api/v0/crm/webhooks/support/`
- [ ] Authentication: `X-CRM-API-Key` header
- [ ] Signature: `X-CRM-Signature` (HMAC-SHA256)
- [ ] Returns 202 Accepted (async processing)
- [ ] Returns 409 Conflict if duplicate idempotency key
- [ ] Returns 401 Unauthorized if invalid signature
- [ ] Returns 429 Too Many Requests if rate limit exceeded

### Event Processing
- [ ] message.created → Timeline event
- [ ] status.changed → Update Support.status + Timeline
- [ ] agent.assigned → Store in metadata + Timeline
(... для всіх 12 типів)

### Security
- [ ] HMAC-SHA256 signature verification
- [ ] Timestamp validation (reject > 5 min old)
- [ ] Idempotency via Redis (24h TTL)
- [ ] Rate limiting (sliding window)

### Testing
- [ ] Integration tests для всіх event types
- [ ] Security tests (invalid signature, expired, rate limit)
- [ ] All tests pass (`make test-dev`)

## Technical Notes

### Request Flow
```
CRM → Webhook Endpoint → Security Layer → Celery Task → Database → Timeline
```

### Signature Verification
```python
def verify_crm_signature(payload: str, signature: str, timestamp: str) -> bool:
    webhook_time = datetime.fromisoformat(timestamp)
    if (timezone.now() - webhook_time).total_seconds() > 300:
        return False

    secret = settings.CRM_WEBHOOK_SECRET.encode()
    message = f"{payload}{timestamp}".encode()
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()

    return hmac.compare_digest(expected, signature)
```

### Celery Task Pattern
```python
@shared_task(bind=True, max_retries=3, retry_backoff=True)
def process_message_created_webhook(self, webhook_data, log_id):
    try:
        support = Support.objects.get(uid=webhook_data['support_uid'])
        timeline_service.create_comment_event(...)
        CRMExchangeLog.objects.filter(uid=log_id).update(status_code=200)
    except Support.DoesNotExist:
        CRMExchangeLog.objects.filter(uid=log_id).update(status_code=404)
        raise  # Non-retryable
    except Exception as exc:
        raise self.retry(exc=exc)  # Retry with backoff
```

## Out of Scope
- Outbound webhooks (E-Pass → CRM) - TASK_105
- Web UI для monitoring webhooks
- Multi-CRM support

## Subtasks
<!-- To be filled by executor -->
- [ ] 01. TBD

## Implementation
<!-- To be filled by executor as work progresses -->

## Summary
<!-- To be filled after completion -->
