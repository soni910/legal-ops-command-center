import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.metrics import (
    average_cycle_time,
    closed_requests,
    number_of_escalations,
    open_requests,
    sla_breach_rate,
    total_requests,
)

st.title("Command Center")
st.write("High-level view of legal ops workflow status, SLAs, and key portfolio health metrics.")

df = load_joined_contract_data()
if df.empty:
    st.info("No contract data available.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Requests", total_requests(df))
    c2.metric("Open Requests", open_requests(df))
    c3.metric("Closed Requests", closed_requests(df))
    c4.metric("Escalations", number_of_escalations(df))

    c5, c6 = st.columns(2)
    c5.metric("Avg Cycle Time (days)", f"{average_cycle_time(df):.1f}")
    c6.metric("SLA Breach Rate", f"{sla_breach_rate(df):.1f}%")
