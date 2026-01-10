# Example: CRUD Operations (POST/PATCH/DELETE)
# Source: accounts/tests/test_fobo_account_ownership.py

from datetime import timedelta
import pytest
from django.utils import timezone
from model_bakery import baker
from rest_framework.reverse import reverse

from dataQuality.models import FoboAccountOwnership


@pytest.mark.django_db
@pytest.mark.parametrize("comment", ["", "Some comment", None])
def test_fobo_account_ownership_create(
    authorized_client, fobo_account_ownership_dict, comment
):
    contact = baker.make("users.Contact", name="some_user_name")

    url = reverse("fobo_account_ownership-add-temporary-owner")
    end_date = (timezone.now() + timedelta(days=10)).date()
    data = {
        "fobo_account_ownership": fobo_account_ownership_dict["fao_primary"].id,
        "contact": contact.id,
        "start_date": "2023-09-20T10:10",
        "end_date": f"{end_date}T07:15:22",
        "ownership_comment": comment,
    }
    response = authorized_client.post(url, data)
    assert response.status_code == 201, response.data
    assert "id" in response.data

    # Verify in database
    account = FoboAccountOwnership.objects.get(pk=response.data.get("id"))
    assert account.ownership_comment == comment


@pytest.mark.django_db
@pytest.mark.parametrize("comment", ["", "Updated comment", None])
def test_fobo_account_ownership_update(
    authorized_client, fobo_account_ownership_dict, comment, account_type
):
    source_system = baker.make("system.SourceSystem", name="test_system")
    fobo_account = baker.make(
        "accounts.FoboAccount",
        source_system=source_system,
        account_type=account_type,
    )

    fobo_account_ownership = baker.make(
        "dataQuality.FoboAccountOwnership",
        is_backup_owner=True,
        start_date="2023-09-11",
        end_date=None,
        fobo_account=fobo_account,
        ownership_comment="Original comment",
    )

    start_date = "2023-09-20"
    end_date = (timezone.now() + timedelta(days=10)).date()
    account_id = fobo_account_ownership.id

    url = reverse("fobo_account_ownership-update-temporary-owner", args=[account_id])
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "ownership_comment": comment,
    }
    response = authorized_client.patch(url, data)
    assert response.status_code == 200, response.data

    # Verify in database
    account = FoboAccountOwnership.objects.get(pk=response.data.get("id"))
    assert account.ownership_comment == comment
