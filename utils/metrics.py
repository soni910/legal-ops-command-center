"""Portfolio metrics for the Legal Ops Command Center simulation."""

from __future__ import annotations

import pandas as pd

from utils.metadata_qa import metadata_completeness_score, metadata_issue_frequency
from utils.risk_engine import add_risk_columns
from utils.salesforce_alignment import salesforce_mismatch_frequency

CLOSED_STAGE = "Filed/Executed"


def _open(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["request_stage"] != CLOSED_STAGE]


def _closed(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["request_stage"] == CLOSED_STAGE]


def total_requests(df: pd.DataFrame) -> int:
    return int(len(df))


def open_requests(df: pd.DataFrame) -> int:
    return int(len(_open(df)))


def closed_requests(df: pd.DataFrame) -> int:
    return int(len(_closed(df)))


def open_requests_by_contract_type(df: pd.DataFrame) -> pd.Series:
    return _open(df)["contract_type"].value_counts()


def open_requests_by_stage(df: pd.DataFrame) -> pd.Series:
    return _open(df)["request_stage"].value_counts()


def open_requests_by_legal_reviewer(df: pd.DataFrame) -> pd.Series:
    return _open(df)["assigned_legal_reviewer"].value_counts()


def open_requests_by_department(df: pd.DataFrame) -> pd.Series:
    return _open(df)["department"].value_counts()


def average_cycle_time(df: pd.DataFrame) -> float:
    c = _closed(df).copy()
    if c.empty:
        return 0.0
    c["cycle_time_days"] = (pd.to_datetime(c["executed_date"], errors="coerce") - pd.to_datetime(c["intake_date"], errors="coerce")).dt.days
    return float(c["cycle_time_days"].dropna().mean() or 0.0)


def average_cycle_time_by_contract_type(df: pd.DataFrame) -> pd.Series:
    c = _closed(df).copy()
    c["cycle_time_days"] = (pd.to_datetime(c["executed_date"], errors="coerce") - pd.to_datetime(c["intake_date"], errors="coerce")).dt.days
    return c.groupby("contract_type")["cycle_time_days"].mean().dropna().sort_values(ascending=False)


def average_cycle_time_by_legal_reviewer(df: pd.DataFrame) -> pd.Series:
    c = _closed(df).copy()
    c["cycle_time_days"] = (pd.to_datetime(c["executed_date"], errors="coerce") - pd.to_datetime(c["intake_date"], errors="coerce")).dt.days
    return c.groupby("assigned_legal_reviewer")["cycle_time_days"].mean().dropna().sort_values(ascending=False)


def sla_breach_rate(df: pd.DataFrame) -> float:
    r = add_risk_columns(df)
    o = _open(r)
    if o.empty:
        return 0.0
    return float((o["sla_status"] == "Over SLA").mean() * 100)


def sla_breach_rate_by_department(df: pd.DataFrame) -> pd.Series:
    r = _open(add_risk_columns(df))
    return (r.assign(breach=r["sla_status"] == "Over SLA").groupby("department")["breach"].mean() * 100).sort_values(ascending=False)


def sla_breach_rate_by_legal_reviewer(df: pd.DataFrame) -> pd.Series:
    r = _open(add_risk_columns(df))
    return (r.assign(breach=r["sla_status"] == "Over SLA").groupby("assigned_legal_reviewer")["breach"].mean() * 100).sort_values(ascending=False)


def number_of_escalations(df: pd.DataFrame) -> int:
    r = add_risk_columns(df)
    return int(r["escalation_required"].sum())


def escalations_by_legal_reviewer(df: pd.DataFrame) -> pd.Series:
    r = add_risk_columns(df)
    return r[r["escalation_required"]].groupby("assigned_legal_reviewer").size().sort_values(ascending=False)


def contract_volume_by_department(df: pd.DataFrame) -> pd.Series:
    return df.groupby("department").size().sort_values(ascending=False)


def high_risk_clauses_by_frequency(df: pd.DataFrame) -> pd.Series:
    r = add_risk_columns(df)
    reasons = r["escalation_reasons"].explode().dropna()
    return reasons[reasons.isin(["uncapped_indemnity", "unusual_liability_cap", "non_standard_data_security_clause"])].value_counts()


def bottleneck_stage_counts(df: pd.DataFrame) -> pd.Series:
    r = add_risk_columns(df)
    return r[r["stage_aging_status"] == "Stuck"]["request_stage"].value_counts()


def average_days_in_stage_by_stage(df: pd.DataFrame) -> pd.Series:
    r = add_risk_columns(df)
    return r.groupby("request_stage")["days_in_current_stage"].mean().sort_values(ascending=False)
