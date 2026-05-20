# Legal Ops Command Center

## Live demo
> _Live demo link placeholder: add deployed URL here._

## Overview
Legal Ops Command Center is a portfolio-grade Streamlit application for operational analytics across a legal request workflow.

**This is a synthetic-data legal operations workflow simulation. It does not connect to Salesforce, a CLM platform, or any real contract repository.**

## What problem this simulates
Legal operations teams often need a single view to answer:
- what is currently open,
- which records are at risk,
- where SLA breaches are accumulating,
- whether metadata quality is acceptable,
- and whether contract workflow state is aligned with CRM opportunity state.

This project simulates those needs using deterministic synthetic records and explicit QA/risk/alignment rules.

## What the dashboard answers
The dashboard is designed to quickly answer:
- How many requests are open vs closed?
- Which requests are escalated and why?
- Where are stage bottlenecks forming?
- Which metadata issues are most frequent?
- Which records are mismatched against Salesforce opportunity context?
- Which reviewers/departments have the highest SLA pressure?

## Pages
1. **Command Center** — executive KPIs, stuck stages, escalation drivers, snapshot table.
2. **Request Queue** — filterable operational worklist for triage.
3. **Escalations** — risk score distribution, escalation reasons, escalated records.
4. **Metadata QA** — completeness score, issue frequency, failed records.
5. **Salesforce Alignment** — mismatch categories, frequency, and impacted records.
6. **Workload Analytics** — reviewer/department workload and SLA views.
7. **Methodology & Case Study** — assumptions, rule model, limitations, and roadmap.

## Data model
Primary synthetic datasets:
- `data/synthetic_contract_requests.csv`
- `data/synthetic_salesforce_opportunities.csv`

Supporting artifacts:
- `data/contract_type_sla.csv`
- `data/risk_rules.yaml`
- `data/data_dictionary.csv`

The app intentionally keeps raw CSVs as source data and computes derived analytics in Python utilities.

## Rules and methodology
Core rule modules:
- `utils/metadata_qa.py` — missing/invalid metadata checks by contract type and lifecycle.
- `utils/risk_engine.py` — stage aging, SLA status, escalation reasons, risk scoring.
- `utils/salesforce_alignment.py` — mismatch detection between request and opportunity states.
- `utils/metrics.py` — portfolio, SLA, escalation, and throughput metrics.
- `utils/data_loader.py` and `utils/dashboard_data.py` — loading, normalization, and shared enrichment pipeline.

## Technology stack
- **Python 3.12**
- **Streamlit** for UI
- **Pandas** for tabular processing
- **Plotly** for visualizations
- **PyYAML** for rules configuration
- **Pytest** for tests
- **GitHub Actions** for predeploy CI checks

## How to run locally
Use the following commands exactly:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
python scripts/generate_synthetic_data.py
python scripts/predeploy_check.py
pytest -q
streamlit run app.py
```

## How to regenerate synthetic data
To refresh deterministic datasets:

```bash
python scripts/generate_synthetic_data.py
```

## Tests and predeploy checks
Local quality commands:

```bash
python scripts/predeploy_check.py
pytest -q
```

CI workflow (`.github/workflows/predeploy.yml`) runs:
- synthetic data generation,
- compile checks,
- predeploy validation,
- and test execution.

## Limitations and disclaimer
This repository is for portfolio demonstration and technical review.

**This is a synthetic-data legal operations workflow simulation. It does not connect to Salesforce, a CLM platform, or any real contract repository.**

It is **not** a Salesforce integration, not legal advice, and not a production system.

## Production roadmap
A production-grade implementation would require:
- secure authentication/authorization and role-based access,
- secrets management and key rotation,
- real data contracts and lineage controls,
- observability and alerting,
- governance/audit logging,
- privacy/security/compliance controls,
- robust deployment architecture and SLO-backed operations.

## What this demonstrates
- Practical architecture decomposition (loader/rules/metrics/pages).
- Deterministic synthetic data generation for reproducible demos.
- Clear separation of source data vs derived analytics.
- Rule-driven QA/risk/alignment reasoning.
- CI-friendly validation and automated test coverage.
- Professional communication of scope boundaries and non-production claims.
