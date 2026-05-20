"""Shared constants for the Legal Ops Command Center simulation."""

VALID_CONTRACT_TYPES = [
    "NDA",
    "MSA",
    "Vendor Agreement",
    "Customer Order Form",
    "Procurement Contract",
]

CUSTOMER_FACING_CONTRACT_TYPES = [
    "MSA",
    "Customer Order Form",
]

RENEWAL_TERM_REQUIRED_TYPES = [
    "MSA",
    "Vendor Agreement",
    "Customer Order Form",
    "Procurement Contract",
]

TERMINATION_RIGHTS_REQUIRED_TYPES = [
    "MSA",
    "Vendor Agreement",
    "Procurement Contract",
]

DATA_SECURITY_REVIEW_TYPES = [
    "MSA",
    "Vendor Agreement",
    "Customer Order Form",
    "Procurement Contract",
]

VALID_WORKFLOW_STAGES = [
    "Intake Incomplete",
    "Awaiting Legal Review",
    "Awaiting Business Owner",
    "Redline Negotiation",
    "Signature Pending",
    "Metadata QA Failed",
    "Filed/Executed",
]

CLOSED_STAGE = "Filed/Executed"

VALID_SALESFORCE_STAGES = [
    "Prospecting",
    "Qualification",
    "Proposal/Price Quote",
    "Negotiation/Review",
    "Closed Won",
    "Closed Lost",
]

STAGE_STUCK_THRESHOLDS = {
    "Intake Incomplete": 2,
    "Awaiting Legal Review": 3,
    "Awaiting Business Owner": 5,
    "Redline Negotiation": 10,
    "Signature Pending": 3,
    "Metadata QA Failed": 2,
    "Filed/Executed": None,
}

DATA_AS_OF_DATE = "2026-05-19"
