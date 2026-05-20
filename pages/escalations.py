import plotly.express as px
import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.risk_engine import add_risk_columns, escalation_reason_frequency

st.title("Escalations")
st.markdown("Escalation monitoring for synthetic legal-ops risk signals and resolution prioritization.")

df = load_joined_contract_data()
if df.empty:
    st.info("No data available.")
    st.stop()

risk_df = add_risk_columns(df)
esc = risk_df[risk_df["escalation_required"]]

c1, c2 = st.columns(2)
c1.metric("Escalated Records", len(esc))
c2.metric("Average Risk Score", f"{risk_df['risk_score'].mean():.1f}")

left, right = st.columns(2)
with left:
    st.subheader("Risk Score Distribution")
    fig = px.histogram(risk_df, x="risk_score", nbins=20, color_discrete_sequence=["#5B8FF9"])
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Escalation Reason Frequency")
    freq = escalation_reason_frequency(risk_df)
    if not freq.empty:
        fig = px.bar(freq, x="reason", y="count", color="count", color_continuous_scale="Reds")
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Escalated Records")
st.dataframe(
    esc[["request_id", "contract_type", "request_stage", "risk_score", "escalation_reasons", "assigned_legal_reviewer", "department"]].sort_values("risk_score", ascending=False),
    use_container_width=True,
    height=550,
)
