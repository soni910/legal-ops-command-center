import streamlit as st

st.title("Methodology & Case Study")

st.markdown("""
### Project Overview
This portfolio demonstrates a **Salesforce alignment simulation** for legal-ops requests using synthetic data.

### Problem Simulated
Legal teams need visibility into queue health, SLA risk, metadata quality, and CRM workflow consistency.

### Workflow Modeled
The simulation includes intake, review, negotiation, signature, QA, and filed/executed stages.

### Synthetic Data Design
Data is generated deterministically with seeded randomness to include realistic operational noise.

### Metadata QA Rules
Metadata QA checks required fields by contract type and detects executed-not-filed anomalies.

### Salesforce Alignment Rules
Rules flag missing/invalid links, stage inconsistencies, closed-lost conflicts, and urgency mismatches.

### Risk and Escalation Rules
Risk scores combine SLA, stage aging, clause risk, ownership gaps, and alignment risk factors.

### Legal-Ops Metrics
Metrics summarize open load, cycle times, SLA breaches, bottlenecks, and escalation concentrations.

### What This Demonstrates
A structured analytics approach to legal-ops operations using transparent Python utilities and reusable logic.

### What a Production Version Would Require
Secure data pipelines, authentication, governance, monitoring, observability, and deeper integration controls.

### Limitations and Disclaimer
Synthetic-data portfolio demo only. No real contracts, no client data, no live Salesforce or CLM integration, and no legal advice.
""")
