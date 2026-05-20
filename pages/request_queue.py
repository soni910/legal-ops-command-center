import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.metadata_qa import add_metadata_qa_columns
from utils.risk_engine import add_risk_columns
from utils.salesforce_alignment import add_salesforce_alignment_columns

st.title("Request Queue")
st.markdown("Operational triage console for filtering, prioritizing, and reviewing synthetic request records.")

df = load_joined_contract_data()
if df.empty:
    st.info("No queue data available.")
    st.stop()

df = add_salesforce_alignment_columns(add_metadata_qa_columns(add_risk_columns(df)))

with st.expander("Filters", expanded=True):
    r1 = st.columns(3)
    contract_types = r1[0].multiselect("Contract Type", sorted(df["contract_type"].dropna().unique()))
    departments = r1[1].multiselect("Department", sorted(df["department"].dropna().unique()))
    reviewers = r1[2].multiselect("Legal Reviewer", sorted(df["assigned_legal_reviewer"].dropna().unique()))

    r2 = st.columns(3)
    stages = r2[0].multiselect("Request Stage", sorted(df["request_stage"].dropna().unique()))
    sla_status = r2[1].multiselect("SLA Status", sorted(df["sla_status"].dropna().unique()))
    stage_aging = r2[2].multiselect("Stage Aging Status", sorted(df["stage_aging_status"].dropna().unique()))

    r3 = st.columns(4)
    escalation_status = r3[0].multiselect("Escalation Status", [True, False])
    metadata_status = r3[1].multiselect("Metadata QA Status", sorted(df["metadata_qa_status"].dropna().unique()))
    sf_mismatch = r3[2].multiselect("Salesforce Mismatch", [True, False])
    priority = r3[3].multiselect("Priority", sorted(df["priority"].dropna().unique()))

filtered = df.copy()
for col, vals in [("contract_type", contract_types), ("department", departments), ("assigned_legal_reviewer", reviewers), ("request_stage", stages), ("sla_status", sla_status), ("stage_aging_status", stage_aging), ("escalation_required", escalation_status), ("metadata_qa_status", metadata_status), ("salesforce_mismatch", sf_mismatch), ("priority", priority)]:
    if vals:
        filtered = filtered[filtered[col].isin(vals)]

st.caption(f"Showing **{len(filtered)}** of **{len(df)}** requests")
st.dataframe(filtered, use_container_width=True, height=600)
