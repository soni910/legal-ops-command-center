import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.risk_engine import add_risk_columns, escalation_reason_frequency

st.title("Escalations")
st.write("Review escalated matters and risk drivers in the Salesforce alignment simulation.")

df = load_joined_contract_data()
if df.empty:
    st.info("No contract data available.")
else:
    risk_df = add_risk_columns(df)
    st.metric("Escalation Count", int(risk_df["escalation_required"].sum()))

    st.subheader("Escalation Reason Frequency")
    freq = escalation_reason_frequency(risk_df)
    if freq.empty:
        st.info("No escalation reasons found.")
    else:
        st.bar_chart(freq.set_index("reason")["count"])

    st.subheader("Highest-Risk Records")
    st.dataframe(
        risk_df.sort_values("risk_score", ascending=False)[
            ["request_id", "contract_type", "request_stage", "risk_score", "escalation_reasons", "sla_status", "stage_aging_status"]
        ].head(50),
        use_container_width=True,
    )
