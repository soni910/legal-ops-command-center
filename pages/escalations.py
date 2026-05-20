import streamlit as st
import plotly.express as px

from utils.data_loader import load_joined_contract_data
from utils.risk_engine import add_risk_columns, escalation_reason_frequency

st.title("Escalations")
st.write("Escalation monitoring for the Salesforce alignment simulation.")

df = load_joined_contract_data()
if df.empty:
    st.info("No data available.")
    st.stop()

risk_df = add_risk_columns(df)
esc = risk_df[risk_df["escalation_required"]]

st.subheader("Risk Score Distribution")
fig = px.histogram(risk_df, x="risk_score", nbins=20)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Escalation Reason Frequency")
freq = escalation_reason_frequency(risk_df)
if not freq.empty:
    st.plotly_chart(px.bar(freq, x="reason", y="count"), use_container_width=True)

st.subheader("Escalated Records Table")
st.dataframe(
    esc[["request_id", "contract_type", "request_stage", "risk_score", "escalation_reasons", "assigned_legal_reviewer", "department"]],
    use_container_width=True,
)
