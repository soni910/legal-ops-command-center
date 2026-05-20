"""Metadata QA utilities for source contract request records."""

from __future__ import annotations

from typing import Any

import pandas as pd

from utils.constants import (
    CUSTOMER_FACING_CONTRACT_TYPES,
    RENEWAL_TERM_REQUIRED_TYPES,
    TERMINATION_RIGHTS_REQUIRED_TYPES,
    VALID_CONTRACT_TYPES,
)

EFFECTIVE_DATE_REQUIRED_TYPES = {
    "MSA",
    "Vendor Agreement",
    "Procurement Contract",
    "Customer Order Form",
}


def _missing(value: Any) -> bool:
    return pd.isna(value) or str(value).strip() == ""


def _is_executed(row: pd.Series) -> bool:
    return not _missing(row.get("executed_date")) or str(row.get("request_stage", "")).strip() == "Filed/Executed"


def get_metadata_qa_issues(row: pd.Series) -> list[str]:
    issues: list[str] = []
    contract_type = row.get("contract_type")

    if _missing(row.get("counterparty_name")):
        issues.append("missing_counterparty_name")

    if contract_type not in VALID_CONTRACT_TYPES:
        issues.append("incorrect_contract_type")

    effective_required = _is_executed(row) or contract_type in EFFECTIVE_DATE_REQUIRED_TYPES
    if effective_required and _missing(row.get("effective_date")):
        issues.append("missing_effective_date")

    if contract_type in RENEWAL_TERM_REQUIRED_TYPES and _missing(row.get("renewal_term")):
        issues.append("missing_renewal_term")

    if contract_type in TERMINATION_RIGHTS_REQUIRED_TYPES and _missing(row.get("termination_rights")):
        issues.append("missing_termination_rights")

    if contract_type in CUSTOMER_FACING_CONTRACT_TYPES and _missing(row.get("salesforce_opportunity_id")):
        issues.append("missing_salesforce_opportunity_id")

    filed = row.get("filed_in_clm")
    filed_bool = bool(filed) if isinstance(filed, bool) else str(filed).strip().lower() in {"true", "yes", "1"}
    if not _missing(row.get("executed_date")) and not filed_bool:
        issues.append("executed_agreement_not_filed")

    return issues


def add_metadata_qa_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["metadata_qa_issues"] = out.apply(get_metadata_qa_issues, axis=1)
    out["metadata_qa_status"] = out["metadata_qa_issues"].map(lambda x: "Fail" if len(x) else "Pass")
    return out


def metadata_completeness_score(df: pd.DataFrame) -> float:
    if df.empty:
        return 100.0
    qa = add_metadata_qa_columns(df)
    pass_count = (qa["metadata_qa_status"] == "Pass").sum()
    return round((pass_count / len(qa)) * 100, 2)


def metadata_issue_frequency(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["issue", "count"])
    qa = add_metadata_qa_columns(df)
    exploded = qa["metadata_qa_issues"].explode().dropna()
    if exploded.empty:
        return pd.DataFrame(columns=["issue", "count"])
    return (
        exploded.value_counts()
        .rename_axis("issue")
        .reset_index(name="count")
        .sort_values(["count", "issue"], ascending=[False, True])
        .reset_index(drop=True)
    )
