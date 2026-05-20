import streamlit as st
import plotly.express as px

from utils.data_loader import load_joined_contract_data
from utils.risk_engine import add_risk_columns
from utils.salesforce_alignment import add_salesforce_alignment_columns, salesforce_mismatch_frequency

st.title("Salesforce Alignment")
st.write("Salesforce alignment simulation checks for contract/opportunity consistency.")

df = load_joined_contract_data()
if df.empty:
    st.info("No data available.")
    st.stop()

aligned = add_salesforce_alignment_columns(add_risk_columns(df))

linked = aligned[aligned["opportunity_id"].notna()]
missing = aligned[(aligned["salesforce_opportunity_id"].isna()) | (aligned["salesforce_opportunity_id"].astype(str).str.strip() == "")]
invalid = aligned[(aligned["salesforce_opportunity_id"].notna()) & (aligned["salesforce_opportunity_id"].astype(str).str.strip() != "") & (aligned["opportunity_id"].isna())]
stage = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda r: any(x in r for x in ["executed_but_not_closed_won", "signature_pending_too_early", "redline_negotiation_too_early"]))]
high = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda r: "high_value_commercial_urgency" in r)]
closed_lost = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda r: "closed_lost_with_active_contract" in r)]

c1, c2, c3 = st.columns(3)
c1.metric("Linked Opportunities", len(linked))
c2.metric("Missing Opportunity IDs", len(missing))
c3.metric("Invalid Opportunity IDs", len(invalid))
c4, c5, c6 = st.columns(3)
c4.metric("Stage Mismatches", len(stage))
c5.metric("High-Value Mismatches", len(high))
c6.metric("Closed-Lost Active Contracts", len(closed_lost))

st.subheader("Mismatch Reason Frequency")
freq = salesforce_mismatch_frequency(aligned)
if not freq.empty:
    st.plotly_chart(px.bar(freq, x="reason", y="count"), use_container_width=True)

st.subheader("Mismatch Table")
st.dataframe(aligned[aligned["salesforce_mismatch"]], use_container_width=True)
