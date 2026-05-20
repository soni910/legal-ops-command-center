"""Salesforce alignment simulation utilities."""

from __future__ import annotations

import pandas as pd

from utils.constants import CUSTOMER_FACING_CONTRACT_TYPES


def get_salesforce_mismatch_reasons(row: pd.Series) -> list[str]:
    reasons = []
    ct = row.get("contract_type")
    sfid = row.get("salesforce_opportunity_id")
    has_sfid = not (pd.isna(sfid) or str(sfid).strip() == "")
    opp_id = row.get("opportunity_id")
    has_opp = not (pd.isna(opp_id) or str(opp_id).strip() == "")

    if ct in CUSTOMER_FACING_CONTRACT_TYPES and not has_sfid:
        reasons.append("missing_opportunity_id")
    if has_sfid and not has_opp:
        reasons.append("invalid_opportunity_id")

    executed = not pd.isna(pd.to_datetime(row.get("executed_date"), errors="coerce"))
    sf_stage = str(row.get("salesforce_stage", "")).strip()
    req_stage = str(row.get("request_stage", "")).strip()

    if executed and sf_stage and sf_stage != "Closed Won":
        reasons.append("executed_but_not_closed_won")
    if req_stage == "Signature Pending" and sf_stage in {"Prospecting", "Qualification"}:
        reasons.append("signature_pending_too_early")
    if req_stage == "Redline Negotiation" and sf_stage == "Prospecting":
        reasons.append("redline_negotiation_too_early")

    amt = pd.to_numeric(row.get("opportunity_amount"), errors="coerce")
    if amt > 100000 and req_stage in {"Intake Incomplete", "Awaiting Business Owner"} and row.get("stage_aging_status") == "Stuck":
        reasons.append("high_value_commercial_urgency")

    if sf_stage == "Closed Lost" and req_stage != "Filed/Executed":
        reasons.append("closed_lost_with_active_contract")

    cp = str(row.get("counterparty_name", "")).strip().lower()
    acct = str(row.get("account_name", "")).strip().lower()
    if cp and acct and cp != acct and cp.split()[0] != acct.split()[0]:
        reasons.append("optional_account_mismatch")

    return reasons


def add_salesforce_alignment_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["salesforce_mismatch_reasons"] = out.apply(get_salesforce_mismatch_reasons, axis=1)
    out["salesforce_mismatch"] = out["salesforce_mismatch_reasons"].map(lambda x: len(x) > 0)
    return out


def salesforce_mismatch_frequency(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["reason", "count"])
    src = df if "salesforce_mismatch_reasons" in df.columns else add_salesforce_alignment_columns(df)
    ex = src["salesforce_mismatch_reasons"].explode().dropna()
    if ex.empty:
        return pd.DataFrame(columns=["reason", "count"])
    return ex.value_counts().rename_axis("reason").reset_index(name="count")
