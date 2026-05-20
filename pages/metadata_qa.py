import streamlit as st

from utils.data_loader import load_contract_requests
from utils.metadata_qa import add_metadata_qa_columns, metadata_completeness_score, metadata_issue_frequency

st.title("Metadata QA")
st.write("Validate extracted fields and quality indicators using synthetic records and QA checks.")

contracts = load_contract_requests()
qa_df = add_metadata_qa_columns(contracts) if not contracts.empty else contracts

score = metadata_completeness_score(contracts) if not contracts.empty else 100.0
st.metric("Metadata Completeness Score", f"{score}%")

st.subheader("Issue Frequency")
freq = metadata_issue_frequency(contracts)
if freq.empty:
    st.info("No metadata issues found.")
else:
    st.bar_chart(freq.set_index("issue")["count"])

st.subheader("Failing Records")
if contracts.empty:
    st.info("No contract data available.")
else:
    failing = qa_df[qa_df["metadata_qa_status"] == "Fail"]
    st.dataframe(failing[["request_id", "contract_type", "request_stage", "metadata_qa_issues"]], use_container_width=True)

st.subheader("Executed but Not Filed")
if contracts.empty:
    st.info("No contract data available.")
else:
    executed_not_filed = qa_df[(qa_df["executed_date"].notna()) & (qa_df["filed_in_clm"] == False)]  # noqa: E712
    st.dataframe(
        executed_not_filed[["request_id", "contract_type", "executed_date", "filed_in_clm", "metadata_qa_issues"]],
        use_container_width=True,
    )

st.subheader("QA Rule Explanation")
st.markdown(
    """
- **missing_counterparty_name**: Counterparty name is blank.
- **missing_effective_date**: Effective date is required for signed/executed records and key contract types.
- **missing_renewal_term**: Renewal term is required for MSA, Vendor Agreement, Customer Order Form, and Procurement Contract.
- **missing_termination_rights**: Termination rights are required for MSA, Vendor Agreement, and Procurement Contract.
- **missing_salesforce_opportunity_id**: Salesforce opportunity ID is required for MSA and Customer Order Form.
- **incorrect_contract_type**: Contract type is not in the allowed canonical list.
- **executed_agreement_not_filed**: Executed date exists while filed_in_clm is false.
"""
)