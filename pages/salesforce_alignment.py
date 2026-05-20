import streamlit as st

from utils.data_loader import load_joined_contract_data
from utils.risk_engine import add_risk_columns
from utils.salesforce_alignment import add_salesforce_alignment_columns, salesforce_mismatch_frequency

st.title("Salesforce Alignment")
st.write("Salesforce alignment simulation checks for contract/opportunity linkage and stage consistency.")

df = load_joined_contract_data()
if df.empty:
    st.info("No contract data available.")
else:
    df = add_risk_columns(df)
    aligned = add_salesforce_alignment_columns(df)

    linked = aligned[aligned["opportunity_id"].notna()]
    missing_ids = aligned[(aligned["salesforce_opportunity_id"].isna()) | (aligned["salesforce_opportunity_id"].astype(str).str.strip() == "")]
    invalid_ids = aligned[(aligned["salesforce_opportunity_id"].notna()) & (aligned["salesforce_opportunity_id"].astype(str).str.strip() != "") & (aligned["opportunity_id"].isna())]

    stage_mismatch_reasons = {"executed_but_not_closed_won", "signature_pending_too_early", "redline_negotiation_too_early"}
    stage_mismatches = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda rs: any(r in stage_mismatch_reasons for r in rs))]
    high_value = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda rs: "high_value_commercial_urgency" in rs)]
    closed_lost_active = aligned[aligned["salesforce_mismatch_reasons"].apply(lambda rs: "closed_lost_with_active_contract" in rs)]

    st.subheader("Linked Opportunities")
    st.write(len(linked))
    st.subheader("Missing Opportunity IDs")
    st.write(len(missing_ids))
    st.subheader("Invalid Opportunity IDs")
    st.write(len(invalid_ids))
    st.subheader("Stage Mismatches")
    st.write(len(stage_mismatches))
    st.subheader("High-Value Mismatches")
    st.write(len(high_value))
    st.subheader("Closed-Lost with Active Contract")
    st.write(len(closed_lost_active))

    st.subheader("Mismatch Reason Frequency")
    freq = salesforce_mismatch_frequency(aligned)
    if freq.empty:
        st.info("No mismatch reasons found.")
    else:
        st.bar_chart(freq.set_index("reason")["count"])

    st.subheader("Mismatch Table")
    mismatch = aligned[aligned["salesforce_mismatch"]]
    st.dataframe(
        mismatch[[
            "request_id", "contract_type", "request_stage", "salesforce_opportunity_id", "opportunity_id",
            "salesforce_stage", "opportunity_amount", "salesforce_mismatch_reasons"
        ]],
        use_container_width=True,
    )
