import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.metadata_qa import add_metadata_qa_columns
from utils.risk_engine import add_risk_columns
from utils.salesforce_alignment import add_salesforce_alignment_columns

st.title("Request Queue")
st.write("Operational queue view with filters for triage and workload management.")

df = load_joined_contract_data()
if df.empty:
    st.info("No queue data available.")
    st.stop()

df = add_salesforce_alignment_columns(add_metadata_qa_columns(add_risk_columns(df)))

f1, f2, f3 = st.columns(3)
contract_types = f1.multiselect("Contract Type", sorted(df["contract_type"].dropna().unique()))
departments = f2.multiselect("Department", sorted(df["department"].dropna().unique()))
reviewers = f3.multiselect("Legal Reviewer", sorted(df["assigned_legal_reviewer"].dropna().unique()))

f4, f5, f6 = st.columns(3)
stages = f4.multiselect("Request Stage", sorted(df["request_stage"].dropna().unique()))
sla_status = f5.multiselect("SLA Status", sorted(df["sla_status"].dropna().unique()))
stage_aging = f6.multiselect("Stage Aging Status", sorted(df["stage_aging_status"].dropna().unique()))

f7, f8, f9, f10 = st.columns(4)
escalation_status = f7.multiselect("Escalation Status", [True, False])
metadata_status = f8.multiselect("Metadata QA Status", sorted(df["metadata_qa_status"].dropna().unique()))
sf_mismatch = f9.multiselect("Salesforce Mismatch", [True, False])
priority = f10.multiselect("Priority", sorted(df["priority"].dropna().unique()))

filtered = df.copy()
for col, vals in [
    ("contract_type", contract_types),
    ("department", departments),
    ("assigned_legal_reviewer", reviewers),
    ("request_stage", stages),
    ("sla_status", sla_status),
    ("stage_aging_status", stage_aging),
    ("escalation_required", escalation_status),
    ("metadata_qa_status", metadata_status),
    ("salesforce_mismatch", sf_mismatch),
    ("priority", priority),
]:
    if vals:
        filtered = filtered[filtered[col].isin(vals)]

st.subheader("Operational Table")
st.dataframe(filtered, use_container_width=True)
