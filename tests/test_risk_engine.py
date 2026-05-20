import pandas as pd

from utils.risk_engine import (
    add_risk_columns,
    calculate_days_in_current_stage,
    calculate_days_open,
    calculate_risk_score,
    calculate_sla_status,
    calculate_stage_aging_status,
    get_escalation_reasons,
)


def _row(**k):
    base = {
        "intake_date": "2026-05-01",
        "stage_entered_date": "2026-05-10",
        "executed_date": "",
        "sla_days": 5,
        "request_stage": "Awaiting Legal Review",
        "indemnity_type": "Mutual",
        "liability_cap_type": "Fixed",
        "liability_cap_multiple": "2",
        "governing_law": "Delaware",
        "non_standard_security_clause": False,
        "commercial_owner_assigned": True,
        "salesforce_mismatch": False,
        "filed_in_clm": True,
        "opportunity_amount": 150000,
        "stage_aging_status": "Within Threshold",
    }
    base.update(k)
    return pd.Series(base)


def test_days_open():
    assert calculate_days_open(_row(), "2026-05-19") == 18


def test_days_in_current_stage():
    assert calculate_days_in_current_stage(_row(), "2026-05-19") == 9


def test_sla_breach():
    assert calculate_sla_status(_row(sla_days=3), "2026-05-19") == "Over SLA"


def test_stage_stuck():
    assert calculate_stage_aging_status(_row(request_stage="Awaiting Legal Review", stage_entered_date="2026-05-10"), "2026-05-19") == "Stuck"


def test_risk_scoring_and_reasons():
    r = _row(
        sla_days=3,
        request_stage="Awaiting Business Owner",
        stage_aging_status="Stuck",
        indemnity_type="Uncapped",
        liability_cap_type="Uncapped",
        governing_law="",
        non_standard_security_clause=True,
        commercial_owner_assigned=False,
        salesforce_mismatch=True,
        executed_date="2026-05-18",
        filed_in_clm=False,
    )
    r["sla_status"] = calculate_sla_status(r, "2026-05-19")
    reasons = get_escalation_reasons(r)
    assert "aging_over_sla" in reasons
    assert "executed_agreement_not_filed" in reasons
    r["escalation_reasons"] = reasons
    assert calculate_risk_score(r) > 0


def test_risk_score_cap_100():
    r = _row()
    r["escalation_reasons"] = [
        "aging_over_sla","stuck_in_current_stage","uncapped_indemnity","unusual_liability_cap",
        "missing_governing_law","non_standard_data_security_clause","no_commercial_owner_assigned",
        "salesforce_mismatch","executed_agreement_not_filed","high_value_opportunity_stuck",
    ]
    assert calculate_risk_score(r) == 100


def test_add_risk_columns():
    df = pd.DataFrame([_row().to_dict()])
    out = add_risk_columns(df, "2026-05-19")
    assert {"days_open", "days_in_current_stage", "sla_status", "stage_aging_status", "risk_score"}.issubset(out.columns)
