import csv
import random
from datetime import date, timedelta
from pathlib import Path

DATA_AS_OF_DATE = date(2026, 5, 19)
SEED = 20260519

random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

CONTRACT_TYPES = ["NDA", "MSA", "Vendor Agreement", "Customer Order Form", "Procurement Contract"]
VALID_STAGES = [
    "Intake Incomplete",
    "Awaiting Legal Review",
    "Awaiting Business Owner",
    "Redline Negotiation",
    "Signature Pending",
    "Metadata QA Failed",
    "Filed/Executed",
]
SF_STAGES = [
    "Prospecting",
    "Qualification",
    "Proposal/Price Quote",
    "Negotiation/Review",
    "Closed Won",
    "Closed Lost",
]
DEPARTMENTS = ["Sales", "Procurement", "IT", "Finance", "Operations", "HR"]
NAMES = ["Alex Kim", "Jordan Lee", "Taylor Singh", "Morgan Patel", "Riley Chen", "Casey Lopez"]
COUNTERPARTIES = [
    "Acme Corp", "Globex LLC", "Initech", "Umbrella Systems", "Wayne Enterprises", "Soylent Labs",
    "Stark Retail", "Wonka Distribution", "Hooli", "Vehement Capital"
]

CONTRACT_FIELDS = [
    "request_id","contract_type","counterparty_name","department","business_owner",
    "commercial_owner_assigned","assigned_legal_reviewer","request_stage","intake_date",
    "stage_entered_date","last_updated_date","effective_date","executed_date","filed_in_clm",
    "renewal_term","termination_rights","governing_law","salesforce_opportunity_id",
    "liability_cap_type","liability_cap_multiple","indemnity_type","data_security_clause",
    "non_standard_security_clause","sla_days","priority","ai_summary"
]

SF_FIELDS = [
    "opportunity_id","account_name","opportunity_name","salesforce_stage","opportunity_amount",
    "opportunity_owner","expected_close_date","closed_date","department"
]


def maybe(value, p_none=0.1):
    return "" if random.random() < p_none else value


def random_date_back(max_days=180):
    return DATA_AS_OF_DATE - timedelta(days=random.randint(0, max_days))


def generate_salesforce_records(n=105):
    records = []
    for i in range(1, n + 1):
        dept = random.choice(DEPARTMENTS)
        stage = random.choice(SF_STAGES)
        expected = random_date_back(120)
        closed = ""
        if stage in {"Closed Won", "Closed Lost"}:
            closed = (expected - timedelta(days=random.randint(0, 20))).isoformat()
        records.append({
            "opportunity_id": f"OPP-{10000+i}",
            "account_name": random.choice(COUNTERPARTIES),
            "opportunity_name": f"{dept} Expansion {i}",
            "salesforce_stage": stage,
            "opportunity_amount": str(random.choice([25000, 50000, 75000, 120000, 300000, 500000, 900000])),
            "opportunity_owner": random.choice(NAMES),
            "expected_close_date": expected.isoformat(),
            "closed_date": closed,
            "department": dept,
        })
    return records


def generate_contract_records(sf_records, n=155):
    sf_ids = [r["opportunity_id"] for r in sf_records]
    records = []
    for i in range(1, n + 1):
        intake = random_date_back(210)
        stage = random.choice(VALID_STAGES)
        stage_entered = intake + timedelta(days=random.randint(0, 30))
        last_updated = stage_entered + timedelta(days=random.randint(0, 20))
        executed_date = ""
        effective_date = maybe((intake + timedelta(days=random.randint(10, 40))).isoformat(), 0.15)
        filed_in_clm = random.choice(["Yes", "No"])
        if stage == "Filed/Executed":
            executed = intake + timedelta(days=random.randint(20, 90))
            executed_date = executed.isoformat()
            if random.random() < 0.25:
                filed_in_clm = "No"  # executed agreements not filed
            else:
                filed_in_clm = "Yes"

        contract_type = random.choice(CONTRACT_TYPES)
        if random.random() < 0.08:
            contract_type = random.choice(["SOW", "Partner Paper", "UNKNOWN", "Amendmnt"])

        opp_id = ""
        if random.random() < 0.15:
            opp_id = ""
        elif random.random() < 0.12:
            opp_id = f"BAD-{random.randint(100,999)}"
        else:
            opp_id = random.choice(sf_ids)

        indemnity = random.choice(["Mutual", "One-way", "None", "Uncapped"])
        cap_type = random.choice(["Fixed", "Multiple", "Uncapped", "None"])
        cap_multiple = ""
        if cap_type == "Multiple":
            cap_multiple = str(random.choice([1, 1.5, 2, 3, 10]))
        elif cap_type == "Fixed":
            cap_multiple = str(random.choice([50000, 100000, 250000, 1000000]))
        elif cap_type == "Uncapped":
            cap_multiple = str(random.choice(["", 99]))

        record = {
            "request_id": f"REQ-{20000+i}",
            "contract_type": contract_type,
            "counterparty_name": maybe(random.choice(COUNTERPARTIES), 0.09),
            "department": random.choice(DEPARTMENTS),
            "business_owner": random.choice(NAMES),
            "commercial_owner_assigned": random.choice(["Yes", "No"]),
            "assigned_legal_reviewer": random.choice(NAMES),
            "request_stage": stage,
            "intake_date": intake.isoformat(),
            "stage_entered_date": stage_entered.isoformat(),
            "last_updated_date": last_updated.isoformat(),
            "effective_date": effective_date,
            "executed_date": executed_date,
            "filed_in_clm": filed_in_clm,
            "renewal_term": maybe(random.choice(["12 months", "24 months", "36 months", "Auto-renew"]), 0.2),
            "termination_rights": maybe(random.choice(["30-day", "60-day", "For cause", "None"]), 0.18),
            "governing_law": maybe(random.choice(["Delaware", "California", "New York", "Texas"]), 0.15),
            "salesforce_opportunity_id": opp_id,
            "liability_cap_type": cap_type,
            "liability_cap_multiple": cap_multiple,
            "indemnity_type": indemnity,
            "data_security_clause": random.choice(["Standard", "Enhanced", "Minimal", "Missing"]),
            "non_standard_security_clause": random.choice(["Yes", "No"]),
            "sla_days": str(random.choice([2, 3, 5, 7, 10])),
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "ai_summary": random.choice([
                "Template variance detected in indemnity wording.",
                "Pending business owner turnaround.",
                "Security clause requires privacy counsel review.",
                "Counterparty requested unusual cap carve-out.",
            ]),
        }
        records.append(record)

    # Force specific dirty scenarios
    for rec in records[:8]:
        rec["request_stage"] = random.choice(["Intake Incomplete", "Awaiting Business Owner"])
        rec["sla_days"] = "2"
    for rec in records[8:14]:
        rec["indemnity_type"] = "Uncapped"
        rec["liability_cap_type"] = "Uncapped"
    for rec in records[14:20]:
        rec["salesforce_opportunity_id"] = ""
    return records


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_other_files():
    (DATA_DIR / "contract_type_sla.csv").write_text(
        "contract_type,default_sla_days\n"
        "NDA,2\nMSA,7\nVendor Agreement,7\nCustomer Order Form,5\nProcurement Contract,10\n",
        encoding="utf-8",
    )
    (DATA_DIR / "risk_rules.yaml").write_text(
        "data_as_of_date: '2026-05-19'\n"
        "rules:\n"
        "  - name: missing_counterparty\n    points: 20\n"
        "  - name: invalid_contract_type\n    points: 25\n"
        "  - name: uncapped_indemnity\n    points: 35\n"
        "  - name: executed_not_filed\n    points: 30\n",
        encoding="utf-8",
    )
    (DATA_DIR / "data_dictionary.csv").write_text(
        "dataset,field,description\n"
        "synthetic_contract_requests,request_id,Unique synthetic legal request identifier\n"
        "synthetic_contract_requests,request_stage,Current workflow stage\n"
        "synthetic_salesforce_opportunities,opportunity_id,Unique synthetic Salesforce opportunity ID\n"
        "synthetic_salesforce_opportunities,salesforce_stage,Opportunity stage in Salesforce alignment simulation\n",
        encoding="utf-8",
    )


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    sf_records = generate_salesforce_records()
    contract_records = generate_contract_records(sf_records)
    write_csv(DATA_DIR / "synthetic_salesforce_opportunities.csv", SF_FIELDS, sf_records)
    write_csv(DATA_DIR / "synthetic_contract_requests.csv", CONTRACT_FIELDS, contract_records)
    write_other_files()
    print(f"Generated {len(contract_records)} contract records and {len(sf_records)} Salesforce records.")


if __name__ == "__main__":
    main()
