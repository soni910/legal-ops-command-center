import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.metrics import (
    average_days_in_stage_by_stage,
    bottleneck_stage_counts,
    contract_volume_by_department,
    escalations_by_legal_reviewer,
    metadata_completeness_score,
    metadata_issue_frequency,
    open_requests_by_department,
    open_requests_by_legal_reviewer,
    open_requests_by_stage,
    salesforce_mismatch_frequency,
    sla_breach_rate_by_department,
)

st.title("Workload Analytics")
st.write("Analyze synthetic workload volume, throughput, and trends to support staffing decisions.")

df = load_joined_contract_data()
if df.empty:
    st.info("No contract data available.")
else:
    st.subheader("Open Requests by Stage")
    st.bar_chart(open_requests_by_stage(df))

    st.subheader("Open Requests by Department")
    st.bar_chart(open_requests_by_department(df))

    st.subheader("Open Requests by Legal Reviewer")
    st.bar_chart(open_requests_by_legal_reviewer(df))

    st.subheader("Contract Volume by Department")
    st.bar_chart(contract_volume_by_department(df))

    st.subheader("SLA Breach Rate by Department")
    st.bar_chart(sla_breach_rate_by_department(df))

    st.subheader("Escalations by Legal Reviewer")
    st.bar_chart(escalations_by_legal_reviewer(df))

    st.subheader("Bottleneck Stage Counts")
    st.bar_chart(bottleneck_stage_counts(df))

    st.subheader("Average Days in Stage")
    st.bar_chart(average_days_in_stage_by_stage(df))

    st.subheader("Metadata QA")
    st.metric("Metadata Completeness Score", f"{metadata_completeness_score(df):.1f}%")
    mif = metadata_issue_frequency(df)
    if not mif.empty:
        st.bar_chart(mif.set_index("issue")["count"])

    st.subheader("Salesforce Mismatch Frequency")
    smf = salesforce_mismatch_frequency(df)
    if not smf.empty:
        st.bar_chart(smf.set_index("reason")["count"])
