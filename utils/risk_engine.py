"""Risk and escalation calculation utilities."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from utils.constants import DATA_AS_OF_DATE, STAGE_STUCK_THRESHOLDS


UNUSUAL_LIABILITY_MULTIPLES = {"10", "99", "0", ""}


def _as_date(value: Any) -> pd.Timestamp | pd.NaT:
    return pd.to_datetime(value, errors="coerce")


def _as_of(as_of_date: Any = None) -> pd.Timestamp:
    return _as_date(as_of_date if as_of_date is not None else DATA_AS_OF_DATE)


def calculate_days_open(row: pd.Series, as_of_date: Any = None) -> int | None:
    intake = _as_date(row.get("intake_date"))
    if pd.isna(intake):
        return None
    closed = _as_date(row.get("executed_date"))
    end = closed if not pd.isna(closed) else _as_of(as_of_date)
    return max((end.normalize() - intake.normalize()).days, 0)


def calculate_days_in_current_stage(row: pd.Series, as_of_date: Any = None) -> int | None:
    entered = _as_date(row.get("stage_entered_date"))
    if pd.isna(entered):
        return None
    end = _as_of(as_of_date)
    return max((end.normalize() - entered.normalize()).days, 0)


def calculate_sla_status(row: pd.Series, as_of_date: Any = None) -> str:
    days_open = calculate_days_open(row, as_of_date)
    sla = pd.to_numeric(row.get("sla_days"), errors="coerce")
    if days_open is None or pd.isna(sla):
        return "Unknown"
    return "Over SLA" if days_open > int(sla) else "Within SLA"


def calculate_stage_aging_status(row: pd.Series, as_of_date: Any = None) -> str:
    stage = row.get("request_stage")
    threshold = STAGE_STUCK_THRESHOLDS.get(stage)
    if threshold is None:
        return "Not Applicable"
    days_stage = calculate_days_in_current_stage(row, as_of_date)
    if days_stage is None:
        return "Unknown"
    return "Stuck" if days_stage > threshold else "Within Threshold"


def get_escalation_reasons(row: pd.Series) -> list[str]:
    reasons = []
    if row.get("sla_status") == "Over SLA":
        reasons.append("aging_over_sla")
    if row.get("stage_aging_status") == "Stuck":
        reasons.append("stuck_in_current_stage")

    if str(row.get("indemnity_type", "")).strip().lower() == "uncapped":
        reasons.append("uncapped_indemnity")

    cap_type = str(row.get("liability_cap_type", "")).strip().lower()
    cap_mult = str(row.get("liability_cap_multiple", "")).strip()
    if cap_type == "uncapped" or cap_mult in UNUSUAL_LIABILITY_MULTIPLES:
        reasons.append("unusual_liability_cap")

    if pd.isna(row.get("governing_law")) or str(row.get("governing_law", "")).strip() == "":
        reasons.append("missing_governing_law")

    non_standard = row.get("non_standard_security_clause")
    non_standard_bool = bool(non_standard) if isinstance(non_standard, bool) else str(non_standard).strip().lower() in {"true", "yes", "1"}
    if non_standard_bool:
        reasons.append("non_standard_data_security_clause")

    owner = row.get("commercial_owner_assigned")
    owner_bool = bool(owner) if isinstance(owner, bool) else str(owner).strip().lower() in {"true", "yes", "1"}
    if not owner_bool:
        reasons.append("no_commercial_owner_assigned")

    mismatch = row.get("salesforce_mismatch")
    mismatch_bool = bool(mismatch) if isinstance(mismatch, bool) else str(mismatch).strip().lower() in {"true", "yes", "1"}
    if mismatch_bool:
        reasons.append("salesforce_mismatch")

    executed = not pd.isna(_as_date(row.get("executed_date")))
    filed = row.get("filed_in_clm")
    filed_bool = bool(filed) if isinstance(filed, bool) else str(filed).strip().lower() in {"true", "yes", "1"}
    if executed and not filed_bool:
        reasons.append("executed_agreement_not_filed")

    amount = pd.to_numeric(row.get("opportunity_amount"), errors="coerce")
    if amount > 100000 and row.get("request_stage") in {"Intake Incomplete", "Awaiting Business Owner"} and row.get("stage_aging_status") == "Stuck":
        reasons.append("high_value_opportunity_stuck")

    return reasons


def calculate_risk_score(row: pd.Series) -> int:
    weights = {
        "aging_over_sla": 20,
        "stuck_in_current_stage": 15,
        "uncapped_indemnity": 25,
        "unusual_liability_cap": 20,
        "missing_governing_law": 15,
        "non_standard_data_security_clause": 15,
        "no_commercial_owner_assigned": 15,
        "salesforce_mismatch": 10,
        "executed_agreement_not_filed": 20,
        "high_value_opportunity_stuck": 10,
    }
    score = sum(weights[r] for r in row.get("escalation_reasons", []) if r in weights)
    return min(score, 100)


def add_risk_columns(df: pd.DataFrame, as_of_date: Any = None) -> pd.DataFrame:
    out = df.copy()
    out["days_open"] = out.apply(lambda r: calculate_days_open(r, as_of_date), axis=1)
    out["days_in_current_stage"] = out.apply(lambda r: calculate_days_in_current_stage(r, as_of_date), axis=1)
    out["sla_status"] = out.apply(lambda r: calculate_sla_status(r, as_of_date), axis=1)
    out["stage_aging_status"] = out.apply(lambda r: calculate_stage_aging_status(r, as_of_date), axis=1)
    out["escalation_reasons"] = out.apply(get_escalation_reasons, axis=1)
    out["escalation_required"] = out["escalation_reasons"].map(lambda x: len(x) > 0)
    out["risk_score"] = out.apply(calculate_risk_score, axis=1)
    return out


def escalation_reason_frequency(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["reason", "count"])
    src = df if "escalation_reasons" in df.columns else add_risk_columns(df)
    ex = src["escalation_reasons"].explode().dropna()
    if ex.empty:
        return pd.DataFrame(columns=["reason", "count"])
    return ex.value_counts().rename_axis("reason").reset_index(name="count")
