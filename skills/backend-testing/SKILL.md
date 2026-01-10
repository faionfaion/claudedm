---
name: backend-testing
description: Use when writing pytest tests for Django backend. Handles API tests, model tests, fixtures with model-bakery, entitlements, AG Grid, multi-database tests.
---

# Backend Testing Skill

Write pytest tests following FinRay backend conventions.

## Testing Stack

- **Framework**: pytest + pytest-django
- **Factory**: model-bakery (`baker.make()`)
- **API Client**: DRF `APIClient`
- **Mocking**: `unittest.mock` (patch, MagicMock)

## File Structure

Tests live inside each Django app:
```
{app}/tests/
├── conftest.py          # App-specific fixtures
├── fixtures.py          # Complex fixture definitions (optional)
├── __init__.py
├── test_{feature}.py    # Test files
└── test_{feature2}.py
```

## Core Fixtures (from root conftest.py)

Always available:
```python
@pytest.fixture
def api_client():
    """Unauthenticated API client"""
    return APIClient()

@pytest.fixture
def user(db):
    """User with full entitlements and hierarchy access"""
    # Creates user with UserEntitlement, EntitlementToHierarchy

@pytest.fixture
def authorized_client(api_client, user):
    """Pre-authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client
```

## Database Markers

```python
# Single database (default)
@pytest.mark.django_db
def test_simple(authorized_client):
    pass

# Multi-database (when using metamodel models)
@pytest.mark.django_db(databases=["default", "metamodel"])
def test_with_metamodel(authorized_client, data_asset):
    pass
```

Note: Root conftest auto-adds `metamodel` database to all tests using `db` fixture.

## Test Patterns

### API List/Filter Test
```python
@pytest.mark.django_db
def test_fobo_account_list(authorized_client, source_system, account_type):
    # Arrange
    baker.make("accounts.FoboAccount",
               number="ABC123",
               source_system=source_system,
               account_type=account_type)

    # Act
    url = reverse("fobo-account-list")
    response = authorized_client.get(url)

    # Assert
    assert response.status_code == 200
    assert len(response.data["results"]) >= 1
```

### AG Grid POST Test
```python
@pytest.mark.django_db
def test_balance_ag_grid(authorized_client, balance_type):
    ag_grid_data = {
        "startRow": 0,
        "endRow": 10,
        "rowGroupCols": [],
        "valueCols": [],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": [],
    }

    response = authorized_client.post(
        reverse("balance-type-ag-grid"),
        data=ag_grid_data
    )

    assert response.status_code == 200
    assert "results" in response.data
```

### Parametrized Test
```python
from datetime import timedelta
from django.utils import timezone

testdata = [
    (timezone.now() - timedelta(days=10), None, "ACTIVE"),
    (timezone.now() + timedelta(days=10), None, "SCHEDULED"),
    (timezone.now() - timedelta(days=10), timezone.now() - timedelta(days=5), "EXPIRED"),
]

@pytest.mark.django_db
@pytest.mark.parametrize("start_date,end_date,expected_status", testdata)
def test_ownership_status(authorized_client, start_date, end_date, expected_status):
    ownership = baker.make(
        "dataQuality.FoboAccountOwnership",
        start_date=start_date,
        end_date=end_date,
    )
    assert ownership.status == expected_status
```

### Model Test with Bakery
```python
@pytest.mark.django_db
def test_account_str(account_type):
    account = baker.make(
        "accounts.FoboAccount",
        number="TEST-001",
        account_type=account_type,
    )
    assert str(account) == "TEST-001"
```

### Test with Mocking
```python
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
@patch("accounts.views.MyViewSet.some_method")
def test_with_mock(mock_method, authorized_client):
    mock_method.return_value = {"key": "value"}

    response = authorized_client.get(reverse("my-endpoint"))

    assert response.status_code == 200
    mock_method.assert_called_once()
```

## Model Bakery Usage

```python
from model_bakery import baker
from model_bakery.recipe import seq

# Simple creation
account = baker.make("accounts.FoboAccount")

# With specific fields
account = baker.make("accounts.FoboAccount",
                     number="ABC123",
                     source_system_id=-1)

# Bulk creation
accounts = baker.make("accounts.FoboAccount", _quantity=5)

# Bulk with SQL optimization
baker.make("accounts.Transaction", _quantity=100, _bulk_create=True)

# Sequential values
baker.make("metamodel.MmAttribute", name=seq("Attr_"), _quantity=3)
# Creates: Attr_1, Attr_2, Attr_3

# With related objects (auto-creates)
position = baker.make("accounts.Position",
    portfolio=baker.make("accounts.Portfolio"),
    fobo_account=baker.make("accounts.FoboAccount"),
)
```

## Writing Fixtures

### App-level conftest.py
```python
import pytest
from model_bakery import baker

@pytest.fixture
def source_system(db):
    return baker.make("system.SourceSystem", code="TEST", name="Test System")

@pytest.fixture
def account_type(db):
    return baker.make("accounts.AccountType", code="SAVINGS", name="Savings")

@pytest.fixture
def fobo_account(db, source_system, account_type):
    return baker.make(
        "accounts.FoboAccount",
        number="TEST-001",
        source_system=source_system,
        account_type=account_type,
    )
```

### Complex Fixture with Dict Return
```python
@pytest.fixture
def system_preconditions_dict(db, source_system, fobo_account):
    """Provides common test data as dictionary"""
    return {
        "source_system": source_system,
        "fobo_account": fobo_account,
        "instrument": baker.make("dataQuality.Instrument", sor_id="12345"),
        "currency": baker.make("generics.Currency", code="USD"),
    }
```

## Hierarchy Fixtures

For tests requiring entitlements with hierarchies:
```python
from view_hierarchies.tests.bakery.hierarchy_bakery import (
    bake_business_hierarchies,
    bake_balance_hierarchies,
)

@pytest.fixture
def positions_with_hierarchies(db, fobo_account, balance_type):
    positions = baker.make("accounts.Position", _quantity=5)

    # Create hierarchy caches
    bake_balance_hierarchies(base_member=balance_type)
    bake_business_hierarchies(base_member=fobo_account)

    return positions
```

## Naming Conventions

### Test Files
```
test_{feature}.py              # test_fobo_account.py
test_{feature}_{aspect}.py     # test_fobo_account_ownership.py
```

### Test Methods
```python
def test_{feature}_{action}():                    # test_account_create
def test_{feature}_{action}_{scenario}():         # test_account_create_invalid_data
def test_{viewset}_{endpoint}():                  # test_fobo_account_list
def test_{viewset}_{endpoint}_{filter}():         # test_fobo_account_list_by_status
```

### Fixtures
```python
def {model}(db):                    # def fobo_account(db):
def {model}_{variant}(db):          # def fobo_account_with_balance(db):
def {feature}_dict(db):             # def adjustments_dict(db):
def {feature}_list(db):             # def transactions_list(db):
```

## Running Tests

Tests run inside Docker container via `build.sh`:

```bash
cd backend

# First run - builds Docker image, then runs tests
./build.sh test

# Subsequent runs - uses existing image, mounts source code (faster!)
./build.sh testfast

# Specific test file
./build.sh test src/accounts/tests/test_fobo_account.py
./build.sh testfast src/accounts/tests/test_fobo_account.py

# Specific test function
./build.sh testfast src/accounts/tests/test_fobo_account.py::test_fobo_account_list

# Migration tests (separate)
./build.sh test_migrations
```

**Important**: Always use `test` first to build the image. After that, use `testfast` for faster iteration (it mounts local source code instead of rebuilding).

### What happens under the hood

```bash
# test - builds fresh Docker image each time
docker build -f ./docker/Dockerfile -t test .
docker run --rm test pytest -m "not migrations"

# testfast - reuses image, mounts local source
docker run --rm --mount type=bind,source=$(pwd)/src,target=/src test pytest -m "not migrations"
```

## Common Imports

```python
import pytest
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from model_bakery.recipe import seq
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from datetime import timedelta
```

## Checklist

When writing tests, ensure:

- [ ] Use `@pytest.mark.django_db` (add `databases=["default", "metamodel"]` if using metamodel)
- [ ] Use `authorized_client` fixture for authenticated requests
- [ ] Use `baker.make()` for test data, not `Model.objects.create()`
- [ ] Use `reverse()` for URLs, not hardcoded paths
- [ ] Follow naming: `test_{feature}_{action}_{scenario}`
- [ ] Add fixtures to app's `conftest.py` for reuse
- [ ] Use parametrize for multiple similar test cases
- [ ] Mock external services and slow operations

---

## Examples

Real examples from codebase are in `examples/` folder:

| File | Pattern | Source |
|------|---------|--------|
| `api_list_filtering.py` | API List with GET filtering | test_fobo_account.py |
| `ag_grid_mocking.py` | AG Grid POST with mocking | test_ag_grid.py |
| `parametrized_enums.py` | @parametrize with Enums | test_fobo_account_ownership.py |
| `crud_operations.py` | POST/PATCH operations | test_fobo_account_ownership.py |
| `dict_fixture.py` | Dict fixture pattern | conftest.py |
| `sorting_filtering.py` | Sorting and filter params | test_fobo_account.py |
