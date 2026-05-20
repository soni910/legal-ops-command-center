"""Predeploy repository validation checks for the Legal Ops Command Center simulation."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "app.py",
    "requirements.txt",
    "README.md",
    "data/synthetic_contract_requests.csv",
    "data/synthetic_salesforce_opportunities.csv",
    "data/contract_type_sla.csv",
    "data/risk_rules.yaml",
    "data/data_dictionary.csv",
]

REQUIRED_CONTRACT_COLUMNS = [
    "request_id",
    "contract_type",
    "counterparty_name",
    "department",
    "business_owner",
    "commercial_owner_assigned",
    "assigned_legal_reviewer",
    "request_stage",
    "intake_date",
    "stage_entered_date",
    "last_updated_date",
    "effective_date",
    "executed_date",
    "filed_in_clm",
    "renewal_term",
    "termination_rights",
    "governing_law",
    "salesforce_opportunity_id",
    "liability_cap_type",
    "liability_cap_multiple",
    "indemnity_type",
    "data_security_clause",
    "non_standard_security_clause",
    "sla_days",
    "priority",
    "ai_summary",
]

REQUIRED_SF_COLUMNS = [
    "opportunity_id",
    "account_name",
    "opportunity_name",
    "salesforce_stage",
    "opportunity_amount",
    "opportunity_owner",
    "expected_close_date",
    "closed_date",
    "department",
]


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def _ok(msg: str) -> None:
    print(f"[OK] {msg}")


def verify_required_files() -> None:
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            _fail(f"Required file missing: {rel}")
    _ok("All required files exist")


def _read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            _fail(f"CSV has no header: {path.relative_to(ROOT)}")
        rows = list(reader)
        return reader.fieldnames, rows


def verify_columns_and_rows() -> None:
    contract_path = ROOT / "data/synthetic_contract_requests.csv"
    sf_path = ROOT / "data/synthetic_salesforce_opportunities.csv"

    contract_cols, contract_rows = _read_rows(contract_path)
    sf_cols, sf_rows = _read_rows(sf_path)

    missing_contract = [c for c in REQUIRED_CONTRACT_COLUMNS if c not in contract_cols]
    if missing_contract:
        _fail(f"Missing contract CSV columns: {missing_contract}")

    missing_sf = [c for c in REQUIRED_SF_COLUMNS if c not in sf_cols]
    if missing_sf:
        _fail(f"Missing Salesforce CSV columns: {missing_sf}")

    if not contract_rows:
        _fail("Contract CSV is empty")
    if not sf_rows:
        _fail("Salesforce CSV is empty")

    _ok("CSV required columns exist and files are non-empty")

    request_ids = [r.get("request_id", "") for r in contract_rows]
    if len(set(request_ids)) != len(request_ids):
        _fail("request_id is not unique")
    _ok("request_id is unique")

    opportunity_ids = [r.get("opportunity_id", "") for r in sf_rows]
    if len(set(opportunity_ids)) != len(opportunity_ids):
        _fail("opportunity_id is not unique")
    _ok("opportunity_id is unique")


def run_compile_checks() -> None:
    cmd = [sys.executable, "-m", "compileall", "app.py", "pages", "utils", "scripts", "tests"]
    proc = subprocess.run(cmd, cwd=ROOT, check=False)
    if proc.returncode != 0:
        _fail("Compile checks failed")
    _ok("Compile checks passed")


def main() -> None:
    verify_required_files()
    verify_columns_and_rows()
    run_compile_checks()
    print("Predeploy checks completed successfully.")


if __name__ == "__main__":
    main()
