import streamlit as st
import plotly.express as px

from utils.data_loader import load_joined_contract_data
from utils.metrics import (
    average_cycle_time,
    bottleneck_stage_counts,
    metadata_completeness_score,
    number_of_escalations,
    open_requests,
    sla_breach_rate,
)
from utils.risk_engine import add_risk_columns, escalation_reason_frequency
from utils.salesforce_alignment import add_salesforce_alignment_columns

st.title("Command Center")
st.caption("Salesforce alignment simulation dashboard for synthetic legal-ops operations data.")

base_df = load_joined_contract_data()
if base_df.empty:
    st.info("No data available. Run synthetic data generation first.")
    st.stop()

risk_df = add_risk_columns(base_df)
aligned_df = add_salesforce_alignment_columns(risk_df)

mismatch_count = int(aligned_df["salesforce_mismatch"].sum())

c1, c2, c3 = st.columns(3)
c1.metric("Open Requests", open_requests(base_df))
c2.metric("Escalations", number_of_escalations(base_df))
c3.metric("SLA Breach Rate", f"{sla_breach_rate(base_df):.1f}%")

c4, c5, c6 = st.columns(3)
c4.metric("Metadata Completeness", f"{metadata_completeness_score(base_df):.1f}%")
c5.metric("Salesforce Mismatch Count", mismatch_count)
c6.metric("Average Cycle Time", f"{average_cycle_time(base_df):.1f} days")

left, right = st.columns(2)
with left:
    st.subheader("Top Stuck Stages")
    stuck = bottleneck_stage_counts(base_df).head(7)
    if not stuck.empty:
        fig = px.bar(stuck.reset_index(), x="request_stage", y="count", labels={"request_stage": "Stage", "count": "Stuck Count"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No stuck stages detected.")

with right:
    st.subheader("Top Escalation Reasons")
    reasons = escalation_reason_frequency(risk_df).head(8)
    if not reasons.empty:
        fig = px.bar(reasons, x="reason", y="count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No escalation reasons detected.")

st.subheader("Executive Snapshot")
st.dataframe(
    aligned_df.sort_values(["risk_score", "days_open"], ascending=[False, False])[
        [
            "request_id",
            "contract_type",
            "department",
            "request_stage",
            "assigned_legal_reviewer",
            "risk_score",
            "sla_status",
            "stage_aging_status",
            "salesforce_mismatch",
        ]
    ].head(25),
    use_container_width=True,
)

st.caption("Disclaimer: Synthetic-data portfolio demo only. No live Salesforce or CLM integration.")
