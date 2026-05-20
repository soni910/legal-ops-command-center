"""Shared page-level data preparation helpers.

These helpers keep Streamlit pages presentation-focused and reduce duplicated
pipeline logic across pages.
"""

from __future__ import annotations

import pandas as pd

from utils.data_loader import load_contract_requests, load_joined_contract_data
from utils.metadata_qa import add_metadata_qa_columns
from utils.risk_engine import add_risk_columns
from utils.salesforce_alignment import add_salesforce_alignment_columns


def get_contracts_with_metadata_qa() -> pd.DataFrame:
    """Load contract requests and append metadata QA outputs."""
    contracts = load_contract_requests()
    if contracts.empty:
        return contracts
    return add_metadata_qa_columns(contracts)


def get_joined_enriched_data() -> pd.DataFrame:
    """Load joined request/opportunity data and append derived columns."""
    joined = load_joined_contract_data()
    if joined.empty:
        return joined

    enriched = add_risk_columns(joined)
    enriched = add_metadata_qa_columns(enriched)
    enriched = add_salesforce_alignment_columns(enriched)
    return enriched
