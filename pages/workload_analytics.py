import plotly.express as px
import streamlit as st

from utils.dashboard_data import get_joined_enriched_data
from utils.metrics import (
    average_cycle_time_by_contract_type,
    average_cycle_time_by_legal_reviewer,
    bottleneck_stage_counts,
    escalations_by_legal_reviewer,
    open_requests_by_contract_type,
    open_requests_by_legal_reviewer,
    sla_breach_rate_by_department,
    sla_breach_rate_by_legal_reviewer,
)

st.title("Workload Analytics")
st.markdown("Operational workload, throughput, and bottleneck analysis for synthetic legal-ops data.")

df = get_joined_enriched_data()
if df.empty:
    st.info("No data available.")
    st.stop()


def bar(series, x, y, color):
    if series.empty:
        st.info("No data for this view.")
        return
    d = series.reset_index()
    d.columns = [x, y]
    fig = px.bar(d, x=x, y=y, color=y, color_continuous_scale=color)
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Open Tickets by Contract Type")
    bar(open_requests_by_contract_type(df), "contract_type", "count", "Blues")
with c2:
    st.subheader("Open Tickets by Legal Reviewer")
    bar(open_requests_by_legal_reviewer(df), "assigned_legal_reviewer", "count", "Greens")

c3, c4 = st.columns(2)
with c3:
    st.subheader("Avg Cycle Time by Contract Type")
    bar(average_cycle_time_by_contract_type(df), "contract_type", "avg_cycle_days", "Oranges")
with c4:
    st.subheader("Avg Cycle Time by Legal Reviewer")
    bar(average_cycle_time_by_legal_reviewer(df), "assigned_legal_reviewer", "avg_cycle_days", "Oranges")

c5, c6 = st.columns(2)
with c5:
    st.subheader("SLA Breach Rate by Department")
    bar(sla_breach_rate_by_department(df), "department", "breach_rate_pct", "Reds")
with c6:
    st.subheader("SLA Breach Rate by Legal Reviewer")
    bar(sla_breach_rate_by_legal_reviewer(df), "assigned_legal_reviewer", "breach_rate_pct", "Reds")

c7, c8 = st.columns(2)
with c7:
    st.subheader("Escalation Volume by Reviewer")
    bar(escalations_by_legal_reviewer(df), "assigned_legal_reviewer", "escalations", "Purples")
with c8:
    st.subheader("Bottleneck Stages")
    bar(bottleneck_stage_counts(df), "request_stage", "count", "Teal")
