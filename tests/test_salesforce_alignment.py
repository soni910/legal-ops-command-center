import pandas as pd

from utils.salesforce_alignment import get_salesforce_mismatch_reasons


def _row(**k):
    base = {
        "contract_type": "MSA",
        "salesforce_opportunity_id": "OPP-10001",
        "opportunity_id": "OPP-10001",
        "executed_date": "",
        "salesforce_stage": "Negotiation/Review",
        "request_stage": "Awaiting Legal Review",
        "opportunity_amount": 200000,
        "stage_aging_status": "Within Threshold",
        "counterparty_name": "Acme Corp",
        "account_name": "Acme Corp",
    }
    base.update(k)
    return pd.Series(base)


def test_missing_opportunity_id():
    assert "missing_opportunity_id" in get_salesforce_mismatch_reasons(_row(salesforce_opportunity_id=""))


def test_invalid_opportunity_id():
    assert "invalid_opportunity_id" in get_salesforce_mismatch_reasons(_row(opportunity_id=""))


def test_executed_but_not_closed_won():
    assert "executed_but_not_closed_won" in get_salesforce_mismatch_reasons(_row(executed_date="2026-05-01", salesforce_stage="Negotiation/Review"))


def test_signature_pending_too_early():
    assert "signature_pending_too_early" in get_salesforce_mismatch_reasons(_row(request_stage="Signature Pending", salesforce_stage="Prospecting"))


def test_redline_too_early():
    assert "redline_negotiation_too_early" in get_salesforce_mismatch_reasons(_row(request_stage="Redline Negotiation", salesforce_stage="Prospecting"))


def test_high_value_commercial_urgency():
    assert "high_value_commercial_urgency" in get_salesforce_mismatch_reasons(_row(request_stage="Intake Incomplete", stage_aging_status="Stuck", opportunity_amount=150001))


def test_closed_lost_active_contract():
    assert "closed_lost_with_active_contract" in get_salesforce_mismatch_reasons(_row(salesforce_stage="Closed Lost", request_stage="Awaiting Legal Review"))


def test_optional_account_mismatch():
    assert "optional_account_mismatch" in get_salesforce_mismatch_reasons(_row(counterparty_name="Acme Corp", account_name="Globex LLC"))
