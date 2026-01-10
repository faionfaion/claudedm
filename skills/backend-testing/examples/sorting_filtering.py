# Example: Testing Sorting and Filtering
# Source: accounts/tests/test_fobo_account.py

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_fobo_account_filterset_list_sorting(authorized_client, account_type):
    source_system1 = baker.make("system.SourceSystem", name="bbbb")
    source_system2 = baker.make("system.SourceSystem", name="aaaa")

    baker.make(
        "accounts.FoboAccount",
        number="A3333",
        source_system=source_system2,
        account_type=account_type,
    )
    baker.make(
        "accounts.FoboAccount",
        number="B555",
        source_system=source_system1,
        account_type=account_type,
    )
    baker.make(
        "accounts.FoboAccount",
        number="V111",
        source_system=source_system1,
        account_type=account_type,
    )
    baker.make(
        "accounts.FoboAccount",
        number="F4444",
        source_system=source_system2,
        account_type=account_type,
    )

    url = reverse("fobo-account-filterset-list")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 4 + 1  # +1 for __unknown__

    # Verify sorting order
    assert response.data["results"][0]["account_name"] == "A3333"
    assert response.data["results"][1]["account_name"] == "B555"
    assert response.data["results"][2]["account_name"] == "F4444"
    assert response.data["results"][3]["account_name"] == "V111"

    # Test filter parameter
    response = authorized_client.get(url, {"account_name": "V111"})
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
