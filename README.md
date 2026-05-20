# Legal Ops Command Center

A Streamlit-based Salesforce alignment simulation for legal operations workflow monitoring.

## Disclaimer
Synthetic-data portfolio demo. No real contracts, no client data, no live Salesforce or CLM integration, and no legal advice.

## Quickstart
1. Create and activate a Python 3.12 virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## App Navigation
The app uses Streamlit's `st.Page` and `st.navigation` for multipage routing:
- Command Center
- Request Queue
- Escalations
- Metadata QA
- Salesforce Alignment
- Workload Analytics
- Methodology & Case Study
