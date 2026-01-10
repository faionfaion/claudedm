# Example: Dict Fixture Pattern
# Source: accounts/tests/conftest.py

import pytest
from model_bakery import baker


@pytest.fixture
def fobo_account_ownership_dict(db, source_system, account_type):
    """Returns dict with primary and backup ownership records.

    Use this pattern when:
    - You need multiple related objects
    - Tests need to access specific items by key
    - Setup is complex and reused across tests
    """
    fobo_account = baker.make(
        "accounts.FoboAccount",
        source_system=source_system,
        account_type=account_type,
    )

    fao_primary = baker.make(
        "dataQuality.FoboAccountOwnership",
        is_backup_owner=False,
        fobo_account=fobo_account,
    )

    fao_backup = baker.make(
        "dataQuality.FoboAccountOwnership",
        is_backup_owner=True,
        fobo_account=fobo_account,
    )

    return {
        "fao_primary": fao_primary,
        "fao_backup": fao_backup,
        "fobo_account": fobo_account,
    }


@pytest.fixture
def system_preconditions_dict(db, source_system, fobo_account):
    """Common test data as dictionary for complex scenarios."""
    return {
        "source_system": source_system,
        "fobo_account": fobo_account,
        "instrument": baker.make("dataQuality.Instrument", sor_id="12345"),
        "currency": baker.make("generics.Currency", code="USD"),
    }
