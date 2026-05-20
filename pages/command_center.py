import plotly.express as px
import streamlit as st

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
st.markdown("""High-level executive view of synthetic legal-ops queue health in a **Salesforce alignment simulation**.""")

base_df = load_joined_contract_data()
if base_df.empty:
    st.info("No data available. Run synthetic data generation first.")
    st.stop()

risk_df = add_risk_columns(base_df)
aligned_df = add_salesforce_alignment_columns(risk_df)

st.markdown("---")
a, b, c = st.columns(3)
a.metric("Open Requests", open_requests(base_df))
b.metric("Escalations", number_of_escalations(base_df))
c.metric("SLA Breach Rate", f"{sla_breach_rate(base_df):.1f}%")

d, e, f = st.columns(3)
d.metric("Metadata Completeness", f"{metadata_completeness_score(base_df):.1f}%")
e.metric("Salesforce Mismatch Count", int(aligned_df["salesforce_mismatch"].sum()))
f.metric("Avg Cycle Time", f"{average_cycle_time(base_df):.1f} days")

left, right = st.columns([1, 1])
with left:
    st.subheader("Top Stuck Stages")
    stuck = bottleneck_stage_counts(base_df).head(7)
    if not stuck.empty:
        ds = stuck.reset_index()
        ds.columns = ["Stage", "Count"]
        fig = px.bar(ds, x="Stage", y="Count", color="Count", color_continuous_scale="Blues")
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Top Escalation Reasons")
    reasons = escalation_reason_frequency(risk_df).head(8)
    if not reasons.empty:
        fig = px.bar(reasons, x="reason", y="count", color="count", color_continuous_scale="Oranges")
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Executive Snapshot")
st.dataframe(
    aligned_df.sort_values(["risk_score", "days_open"], ascending=[False, False])[
        ["request_id", "contract_type", "department", "request_stage", "assigned_legal_reviewer", "risk_score", "sla_status", "stage_aging_status", "salesforce_mismatch"]
    ].head(25),
    use_container_width=True,
    height=460,
)

st.caption("Synthetic-data portfolio demo only. No live Salesforce or CLM integration.")
