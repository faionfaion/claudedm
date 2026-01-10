# Example: API List with Filtering
# Source: accounts/tests/test_fobo_account.py

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_fobo_account_filterset_list(authorized_client, source_system, account_type):
    baker.make(
        "accounts.FoboAccount",
        number="ABC123",
        source_system=source_system,
        account_type=account_type,
    )
    baker.make(
        "accounts.FoboAccount",
        number="123123ASD",
        source_system=source_system,
        account_type=account_type,
    )

    url = reverse("fobo-account-filterset-list")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 2 + 1  # +1 for __unknown__ (pk=-1)
    assert set(response.data["results"][0]) == {
        "system_name",
        "account_name",
        "account_id",
    }
