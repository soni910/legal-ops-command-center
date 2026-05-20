"""Data-loading helpers for the Legal Ops Command Center simulation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import yaml

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

CONTRACT_DATE_COLUMNS = [
    "intake_date",
    "stage_entered_date",
    "last_updated_date",
    "effective_date",
    "executed_date",
]

SF_DATE_COLUMNS = ["expected_close_date", "closed_date"]


def _read_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Missing required data file: `{filename}` in `data/`. Please run the data generator script.")
    except Exception as exc:  # pragma: no cover - defensive UX path
        st.error(f"Unable to read `{filename}` from `data/`: {exc}")
    return pd.DataFrame()


def _normalize_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def _normalize_booleans(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    truthy = {"yes", "true", "1", "y", "t"}
    falsy = {"no", "false", "0", "n", "f"}

    for col in columns:
        if col not in df.columns:
            continue

        def _convert(value: Any) -> Any:
            if pd.isna(value) or value == "":
                return pd.NA
            normalized = str(value).strip().lower()
            if normalized in truthy:
                return True
            if normalized in falsy:
                return False
            return pd.NA

        df[col] = df[col].map(_convert).astype("boolean")
    return df


def load_contract_requests() -> pd.DataFrame:
    df = _read_csv("synthetic_contract_requests.csv")
    if df.empty:
        return df
    df = _normalize_dates(df, CONTRACT_DATE_COLUMNS)
    df = _normalize_booleans(df, ["commercial_owner_assigned", "filed_in_clm", "non_standard_security_clause"])
    return df


def load_salesforce_opportunities() -> pd.DataFrame:
    df = _read_csv("synthetic_salesforce_opportunities.csv")
    if df.empty:
        return df
    df = _normalize_dates(df, SF_DATE_COLUMNS)
    return df


def load_contract_type_sla() -> pd.DataFrame:
    return _read_csv("contract_type_sla.csv")


def load_risk_rules() -> dict[str, Any]:
    path = DATA_DIR / "risk_rules.yaml"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if isinstance(data, dict):
                return data
            st.error("`risk_rules.yaml` must contain a YAML mapping/object.")
            return {}
    except FileNotFoundError:
        st.error("Missing required data file: `risk_rules.yaml` in `data/`. Please run the data generator script.")
    except Exception as exc:  # pragma: no cover - defensive UX path
        st.error(f"Unable to read `risk_rules.yaml` from `data/`: {exc}")
    return {}


def load_data_dictionary() -> pd.DataFrame:
    return _read_csv("data_dictionary.csv")


def load_joined_contract_data() -> pd.DataFrame:
    contracts = load_contract_requests()
    opportunities = load_salesforce_opportunities()

    if contracts.empty:
        return contracts
    if opportunities.empty:
        # Preserve raw opportunity ids even when opportunity file is unavailable.
        return contracts.copy()

    joined = contracts.merge(
        opportunities,
        how="left",
        left_on="salesforce_opportunity_id",
        right_on="opportunity_id",
        suffixes=("", "_sf"),
    )
    return joined
