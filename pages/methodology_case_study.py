import streamlit as st

st.title("Methodology & Case Study")
st.caption("How this Salesforce alignment simulation portfolio was designed and what it demonstrates.")

sections = {
    "Project Overview": "A synthetic legal-ops analytics portfolio designed to demonstrate workflow visibility and quality controls.",
    "Problem Simulated": "Legal teams often struggle to monitor intake, review, negotiation, and CRM alignment at scale.",
    "Workflow Modeled": "Intake → Legal review → Business owner review → Redline → Signature pending → QA → Filed/Executed.",
    "Synthetic Data Design": "Deterministic seeded data generation includes realistic missing fields, stage misalignment, and risk patterns.",
    "Metadata QA Rules": "Checks include required fields by contract type, invalid contract types, and executed-not-filed anomalies.",
    "Salesforce Alignment Rules": "Mismatch checks cover missing/invalid IDs, stage timing issues, closed-lost conflicts, and urgency gaps.",
    "Risk and Escalation Rules": "Risk combines SLA breach, stage aging, clause risk, ownership gaps, and alignment mismatch indicators.",
    "Legal-Ops Metrics": "Core metrics include queue volume, cycle time, breach rates, bottlenecks, and escalation concentration.",
    "What This Demonstrates": "How structured utilities can power repeatable dashboards and explainable operations reporting.",
    "What a Production Version Would Require": "Identity/access controls, data lineage, secure integrations, observability, and governance workflows.",
    "Limitations and Disclaimer": "Synthetic-data portfolio demo only. No real client data, contracts, or live Salesforce/CLM integration.",
}

for title, body in sections.items():
    with st.container(border=True):
        st.subheader(title)
        st.write(body)
