import pandas as pd

from utils.metrics import (
    average_cycle_time,
    closed_requests,
    open_requests,
    sla_breach_rate,
    total_requests,
)


def _df():
    return pd.DataFrame([
        {
            "request_stage": "Filed/Executed", "intake_date": "2026-05-01", "executed_date": "2026-05-11", "sla_days": 5,
            "stage_entered_date": "2026-05-09", "assigned_legal_reviewer": "A", "department": "Sales", "contract_type": "MSA",
            "indemnity_type": "Mutual", "liability_cap_type": "Fixed", "liability_cap_multiple": "2", "governing_law": "Delaware",
            "non_standard_security_clause": False, "commercial_owner_assigned": True, "salesforce_mismatch": False, "filed_in_clm": True,
        },
        {
            "request_stage": "Awaiting Legal Review", "intake_date": "2026-05-01", "executed_date": "", "sla_days": 3,
            "stage_entered_date": "2026-05-10", "assigned_legal_reviewer": "B", "department": "IT", "contract_type": "NDA",
            "indemnity_type": "Mutual", "liability_cap_type": "Fixed", "liability_cap_multiple": "2", "governing_law": "Delaware",
            "non_standard_security_clause": False, "commercial_owner_assigned": True, "salesforce_mismatch": False, "filed_in_clm": False,
        },
    ])


def test_basic_counts_and_cycle_time():
    df = _df()
    assert total_requests(df) == 2
    assert open_requests(df) == 1
    assert closed_requests(df) == 1
    assert average_cycle_time(df) == 10.0


def test_sla_breach_rate():
    df = _df()
    assert sla_breach_rate(df) >= 0
