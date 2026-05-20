# AGENTS.md

## Branch and PR discipline
- Always work from the latest `main` branch.
- Do not stack new work on top of an unmerged Codex branch.
- One task should produce one pull request.
- Do not modify unrelated files.
- Do not create duplicate replacement files such as `app_fixed.py`, `metrics_new.py`, or `final_dashboard.py`.
- If a file needs to be changed, update the existing file.
- Do not merge code manually into `main`.
- Do not store derived fields such as `risk_score`, `escalation_required`, `escalation_reasons`, `metadata_qa_status`, or `salesforce_mismatch` in raw CSV files.
- Compute derived fields in Python utilities.
- Do not use paid APIs, real Salesforce credentials, real CLM credentials, real contracts, client data, or OpenAI API calls.
- Call the project a Salesforce alignment simulation, not a Salesforce integration.
- After changes, run compile checks and tests where possible.
- Summarize exactly which files changed.
