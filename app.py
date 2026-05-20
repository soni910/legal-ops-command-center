import streamlit as st

st.set_page_config(page_title="Legal Ops Command Center", layout="wide")

st.sidebar.info(
    "Synthetic-data portfolio demo. No real contracts, no client data, no live Salesforce or CLM integration, and no legal advice."
)

pg = st.navigation(
    [
        st.Page("pages/command_center.py", title="Command Center", icon=":material/dashboard:"),
        st.Page("pages/request_queue.py", title="Request Queue", icon=":material/inbox:"),
        st.Page("pages/escalations.py", title="Escalations", icon=":material/priority_high:"),
        st.Page("pages/metadata_qa.py", title="Metadata QA", icon=":material/fact_check:"),
        st.Page("pages/salesforce_alignment.py", title="Salesforce Alignment", icon=":material/sync_alt:"),
        st.Page("pages/workload_analytics.py", title="Workload Analytics", icon=":material/insights:"),
        st.Page("pages/methodology_case_study.py", title="Methodology & Case Study", icon=":material/menu_book:"),
    ]
)

pg.run()
