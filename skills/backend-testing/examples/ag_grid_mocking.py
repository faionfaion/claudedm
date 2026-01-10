# Example: AG Grid with Mocking
# Source: accounts/tests/test_ag_grid.py

from unittest.mock import patch
from django.urls import reverse
from model_bakery import baker


@patch("accounts.views.balance_type.BalanceTypeViewSet.ag_grid_consumption_layer_class")
def test_balance_ag_grid(
    ag_grid_consumption_layer_mock,
    authorized_client,
    pnl_balance_type,
    bs_balance_type,
    subledger_types,
    financial_statement_types,
):
    baker.make(
        "accounts.BalanceType",
        subledger_type=subledger_types[0],
        financial_statement_type=financial_statement_types["balance_sheet"],
        balance_type_mapping=pnl_balance_type,
    )

    page_size = 10
    list_response = authorized_client.get(
        reverse("balance-type-list"), data={"page_size": page_size}
    )
    assert list_response.status_code == 200
    assert len(list_response.data["results"]) == 4 + 1  # + __unknown__

    mock_instance = ag_grid_consumption_layer_mock.return_value
    mock_instance.total_count.return_value = 4 + 1
    mock_instance.data.return_value = list_response.data["results"]

    ag_grid_data = {
        "startRow": 0,
        "endRow": page_size,
        "rowGroupCols": [],
        "valueCols": [],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": [],
    }
    ag_grid_response = authorized_client.post(
        reverse("balance-type-ag-grid"), data=ag_grid_data
    )
    assert ag_grid_response.status_code == 200
    assert len(ag_grid_response.data["results"]) == 4 + 1
