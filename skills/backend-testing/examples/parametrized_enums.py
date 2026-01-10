# Example: Parametrized with Enums
# Source: accounts/tests/test_fobo_account_ownership.py

from datetime import timedelta
import pytest
from django.utils import timezone
from model_bakery import baker
from rest_framework.reverse import reverse

from accounts.enums.fobo_account import FoboAccountOwnershipStatus


testdata = [
    (timezone.now() - timedelta(days=10), None, FoboAccountOwnershipStatus.ACTIVE),
    (timezone.now() + timedelta(days=10), None, FoboAccountOwnershipStatus.SCHEDULED),
    (
        timezone.now() - timedelta(days=10),
        timezone.now() + timedelta(days=10),
        FoboAccountOwnershipStatus.ACTIVE,
    ),
    (
        timezone.now() - timedelta(days=10),
        timezone.now() - timedelta(days=10),
        FoboAccountOwnershipStatus.EXPIRED,
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("start_date,end_date,status", testdata)
def test_fobo_account_ownership_status(
    authorized_client, start_date, end_date, status, account_type
):
    source_system = baker.make("system.SourceSystem", name="blablabla")
    fobo_account = baker.make(
        "accounts.FoboAccount",
        source_system=source_system,
        account_type=account_type,
    )

    fobo_account_ownership = baker.make(
        "dataQuality.FoboAccountOwnership",
        is_backup_owner=True,
        start_date=start_date,
        end_date=end_date,
        fobo_account=fobo_account,
    )

    url = reverse("fobo_account_ownership-detail", args=[fobo_account_ownership.id])
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.data["status"] == status.value
