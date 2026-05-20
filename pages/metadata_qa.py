import streamlit as st
import plotly.express as px

from utils.data_loader import load_contract_requests
from utils.metadata_qa import add_metadata_qa_columns, metadata_completeness_score, metadata_issue_frequency

st.title("Metadata QA")
st.write("Source metadata quality checks for synthetic legal request records.")

df = load_contract_requests()
if df.empty:
    st.info("No contract data available.")
    st.stop()

qa = add_metadata_qa_columns(df)

st.metric("Metadata Completeness Score", f"{metadata_completeness_score(df):.1f}%")

st.subheader("Metadata Issue Frequency")
freq = metadata_issue_frequency(df)
if not freq.empty:
    st.plotly_chart(px.bar(freq, x="issue", y="count"), use_container_width=True)

st.subheader("Failed Records")
st.dataframe(qa[qa["metadata_qa_status"] == "Fail"], use_container_width=True)

st.subheader("Executed-Not-Filed Records")
st.dataframe(
    qa[(qa["executed_date"].notna()) & (qa["filed_in_clm"] == False)],  # noqa: E712
    use_container_width=True,
)

st.subheader("QA Rule Explanation")
st.markdown("""
- Missing counterparty name
- Missing effective date (for required types and executed records)
- Missing renewal term for required contract types
- Missing termination rights for required contract types
- Missing Salesforce opportunity ID for customer-facing contract types
- Incorrect contract type
- Executed agreement not filed
""")
