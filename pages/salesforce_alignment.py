import plotly.express as px
import streamlit as st

from utils.dashboard_data import get_joined_enriched_data
from utils.salesforce_alignment import salesforce_mismatch_frequency

st.title("Salesforce Alignment")
st.markdown("Consistency checks between synthetic contract workflow records and Salesforce opportunity data.")

df = get_joined_enriched_data()
if df.empty:
    st.info("No data available.")
    st.stop()

aligned = df

linked = aligned[aligned["opportunity_id"].notna()]
missing = aligned[(aligned["salesforce_opportunity_id"].isna()) | (aligned["salesforce_opportunity_id"].astype(str).str.strip() == "")]
invalid = aligned[(aligned["salesforce_opportunity_id"].notna()) & (aligned["salesforce_opportunity_id"].astype(str).str.strip() != "") & (aligned["opportunity_id"].isna())]
stage = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda r: any(x in r for x in ["executed_but_not_closed_won", "signature_pending_too_early", "redline_negotiation_too_early"]))]
high = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda r: "high_value_commercial_urgency" in r)]
closed_lost = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda r: "closed_lost_with_active_contract" in r)]

r1 = st.columns(3)
r1[0].metric("Linked Opportunities", len(linked))
r1[1].metric("Missing Opportunity IDs", len(missing))
r1[2].metric("Invalid Opportunity IDs", len(invalid))
r2 = st.columns(3)
r2[0].metric("Stage Mismatches", len(stage))
r2[1].metric("High-Value Mismatches", len(high))
r2[2].metric("Closed-Lost Active Contracts", len(closed_lost))

st.subheader("Mismatch Reason Frequency")
freq = salesforce_mismatch_frequency(aligned)
if not freq.empty:
    fig = px.bar(freq, x="reason", y="count", color="count", color_continuous_scale="Purples")
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Mismatch Table")
st.dataframe(aligned[aligned["salesforce_mismatch"]], use_container_width=True, height=520)

st.caption("This is a Salesforce alignment simulation, not a live production integration.")
