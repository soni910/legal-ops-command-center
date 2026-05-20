import pandas as pd

from utils.metadata_qa import (
    add_metadata_qa_columns,
    get_metadata_qa_issues,
    metadata_completeness_score,
)


def _base_row(**overrides):
    row = {
        "contract_type": "MSA",
        "counterparty_name": "Acme",
        "effective_date": "2026-05-01",
        "renewal_term": "12 months",
        "termination_rights": "30-day",
        "salesforce_opportunity_id": "OPP-10001",
        "executed_date": "",
        "filed_in_clm": True,
        "request_stage": "Awaiting Legal Review",
    }
    row.update(overrides)
    return pd.Series(row)


def test_missing_counterparty_name_rule():
    issues = get_metadata_qa_issues(_base_row(counterparty_name=""))
    assert "missing_counterparty_name" in issues


def test_missing_effective_date_rule_for_required_type():
    issues = get_metadata_qa_issues(_base_row(effective_date=""))
    assert "missing_effective_date" in issues


def test_missing_effective_date_rule_for_executed_record():
    issues = get_metadata_qa_issues(_base_row(contract_type="NDA", executed_date="2026-05-02", effective_date=""))
    assert "missing_effective_date" in issues


def test_missing_renewal_term_rule():
    issues = get_metadata_qa_issues(_base_row(renewal_term=""))
    assert "missing_renewal_term" in issues


def test_missing_termination_rights_rule():
    issues = get_metadata_qa_issues(_base_row(termination_rights=""))
    assert "missing_termination_rights" in issues


def test_missing_salesforce_opportunity_id_rule():
    issues = get_metadata_qa_issues(_base_row(contract_type="Customer Order Form", salesforce_opportunity_id=""))
    assert "missing_salesforce_opportunity_id" in issues


def test_incorrect_contract_type_rule():
    issues = get_metadata_qa_issues(_base_row(contract_type="SOW"))
    assert "incorrect_contract_type" in issues


def test_executed_agreement_not_filed_rule():
    issues = get_metadata_qa_issues(_base_row(executed_date="2026-05-02", filed_in_clm=False))
    assert "executed_agreement_not_filed" in issues


def test_metadata_completeness_score():
    df = pd.DataFrame([
        _base_row().to_dict(),
        _base_row(counterparty_name="").to_dict(),
    ])
    assert metadata_completeness_score(df) == 50.0


def test_add_metadata_qa_columns_status():
    df = pd.DataFrame([_base_row().to_dict(), _base_row(counterparty_name="").to_dict()])
    out = add_metadata_qa_columns(df)
    assert list(out["metadata_qa_status"]) == ["Pass", "Fail"]
