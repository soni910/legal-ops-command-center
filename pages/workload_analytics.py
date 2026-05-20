import streamlit as st
import plotly.express as px

from utils.data_loader import load_joined_contract_data
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
st.write("Workload and throughput analytics for synthetic legal-ops operations.")

df = load_joined_contract_data()
if df.empty:
    st.info("No data available.")
    st.stop()

def bar_from_series(series, x, y):
    if series.empty:
        st.info("No data for this view.")
    else:
        s = series.reset_index()
        s.columns = [x, y]
        st.plotly_chart(px.bar(s, x=x, y=y), use_container_width=True)

st.subheader("Open Tickets by Contract Type")
bar_from_series(open_requests_by_contract_type(df), "contract_type", "count")
st.subheader("Open Tickets by Legal Reviewer")
bar_from_series(open_requests_by_legal_reviewer(df), "assigned_legal_reviewer", "count")
st.subheader("Average Cycle Time by Contract Type")
bar_from_series(average_cycle_time_by_contract_type(df), "contract_type", "avg_cycle_days")
st.subheader("Average Cycle Time by Legal Reviewer")
bar_from_series(average_cycle_time_by_legal_reviewer(df), "assigned_legal_reviewer", "avg_cycle_days")
st.subheader("SLA Breach Rate by Department")
bar_from_series(sla_breach_rate_by_department(df), "department", "breach_rate_pct")
st.subheader("SLA Breach Rate by Legal Reviewer")
bar_from_series(sla_breach_rate_by_legal_reviewer(df), "assigned_legal_reviewer", "breach_rate_pct")
st.subheader("Escalation Volume by Reviewer")
bar_from_series(escalations_by_legal_reviewer(df), "assigned_legal_reviewer", "escalations")
st.subheader("Bottleneck Stages")
bar_from_series(bottleneck_stage_counts(df), "request_stage", "count")
