import plotly.express as px
import streamlit as st

from utils.dashboard_data import get_contracts_with_metadata_qa
from utils.metadata_qa import metadata_completeness_score, metadata_issue_frequency

st.title("Metadata QA")
st.markdown("Data quality controls for source request metadata used in the Salesforce alignment simulation.")

df = get_contracts_with_metadata_qa()
if df.empty:
    st.info("No contract data available.")
    st.stop()

qa = df

st.metric("Metadata Completeness Score", f"{metadata_completeness_score(df):.1f}%")

left, right = st.columns(2)
with left:
    st.subheader("Issue Frequency")
    freq = metadata_issue_frequency(df)
    if not freq.empty:
        fig = px.bar(freq, x="issue", y="count", color="count", color_continuous_scale="Teal")
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Pass/Fail Split")
    status = qa["metadata_qa_status"].value_counts().reset_index()
    status.columns = ["status", "count"]
    fig = px.pie(status, names="status", values="count", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Failed Records")
st.dataframe(qa[qa["metadata_qa_status"] == "Fail"], use_container_width=True, height=360)

st.subheader("Executed-Not-Filed Records")
st.dataframe(qa[(qa["executed_date"].notna()) & (qa["filed_in_clm"] == False)], use_container_width=True, height=250)  # noqa: E712

with st.expander("QA Rule Explanation"):
    st.markdown("""
- Missing counterparty name
- Missing effective date (for required types and executed records)
- Missing renewal term for required contract types
- Missing termination rights for required contract types
- Missing Salesforce opportunity ID for customer-facing contract types
- Incorrect contract type
- Executed agreement not filed
""")
