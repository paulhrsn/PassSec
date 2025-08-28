# seed/seed_lab_data.py
import os
import sys
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.getcwd())

from app import create_app
from app.extensions import db
from app.models.lab import LabScenario

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    labs = [
    # ─────────────────────  DOMAIN 1 – ATTACKS, THREATS & VULNERABILITIES  ─────────────────────
    LabScenario(
        domain="Attacks, Threats & Vulnerabilities",
        title="Suspicious Email Header Analysis",
        log_data="""
Received: from attacker.example.com (203.0.113.77) by mail.corp.com
Subject: Urgent – Reset Your Password
DKIM-Signature: none
""".strip(),
        question="Which attack technique is MOST likely in play?",
        choices=["Phishing", "Vishing", "Smishing", "Whaling"],
        answer="Phishing"
    ),
    LabScenario(
        domain="Attacks, Threats & Vulnerabilities",
        title="Web Server SQL Injection Attempt",
        log_data='''GET /login.php?user=admin'-- HTTP/1.1''',
        question="Which control BEST mitigates this?",
        choices=["Parameterized Queries", "WAF Rate Limiting", "Input Blacklisting", "Disabling TLS 1.0"],
        answer="Parameterized Queries"
    ),
    LabScenario(
        domain="Attacks, Threats & Vulnerabilities",
        title="Port-Scan Detection in Firewall Logs",
        log_data="IN=eth0 SRC=192.168.1.222 DST=192.168.1.10 PROTO=TCP DPT=1-1024",
        question="What kind of reconnaissance is occurring?",
        choices=["Port Scanning", "DDoS", "ARP Spoofing", "DNS Poisoning"],
        answer="Port Scanning"
    ),

    # ─────────────────────────  DOMAIN 2 – ARCHITECTURE & DESIGN  ─────────────────────────
    LabScenario(
        domain="Architecture & Design",
        title="Public Cloud Storage Misconfiguration",
        log_data="aws s3api get-bucket-acl --bucket finance-reports",
        question="Which security principle is violated here?",
        choices=["Least Privilege", "Zero Trust", "Separation of Duties", "Fail Closed"],
        answer="Least Privilege"
    ),
    LabScenario(
        domain="Architecture & Design",
        title="TLS Certificate Common-Name Mismatch",
        log_data="chrome: NET::ERR_CERT_COMMON_NAME_INVALID for *.evil.com",
        question="Which concept is intended to prevent this issue?",
        choices=["Certificate Pinning", "OCSP Stapling", "Key Escrow", "DNSSEC"],
        answer="Certificate Pinning"
    ),

    # ─────────────────────────────  DOMAIN 3 – IMPLEMENTATION  ─────────────────────────────
    LabScenario(
        domain="Implementation",
        title="LDAP Secure Bind Verification",
        log_data="389 → 636 STARTTLS success",
        question="Which port is being used for secure LDAP?",
        choices=["636", "389", "3269", "88"],
        answer="636"
    ),
    LabScenario(
        domain="Implementation",
        title="Wi-Fi WPA3 SAE Handshake",
        log_data="hostapd: SAE commit from 00:11:22:33:44:55",
        question="Which attack does SAE primarily mitigate?",
        choices=["Offline Dictionary Attack", "Evil Twin", "KRACK", "Beacon Flood"],
        answer="Offline Dictionary Attack"
    ),

    # ───────────────────────────  DOMAIN 4 – OPERATIONS & IR  ───────────────────────────
    LabScenario(
        domain="Operations & Incident Response",
        title="Brute-Force SSH Followed by Account Lockout",
        log_data="sshd[1024]: Failed password for root from 10.0.0.7 port 55844",
        question="Which FIRST response should a SOC analyst take?",
        choices=["Isolate the host", "Reset all passwords", "Disable SSH", "Collect volatile memory"],
        answer="Isolate the host"
    ),
    LabScenario(
        domain="Operations & Incident Response",
        title="SIEM Correlation – Multiple 4625 then 4740 Events",
        log_data="eventID 4625 ×20 for user jsmith followed by 4740",
        question="Which incident-response phase are you in?",
        choices=["Detection & Analysis", "Preparation", "Eradication", "Recovery"],
        answer="Detection & Analysis"
    ),

    # ────────────────────────  DOMAIN 5 – GOVERNANCE, RISK & COMPLIANCE  ────────────────────────
    LabScenario(
        domain="Governance, Risk & Compliance",
        title="PCI DSS Log-Retention Requirement",
        log_data="SIEM retention set to 13 months",
        question="Which framework mandates a 12-month audit-log minimum?",
        choices=["PCI DSS", "HIPAA", "SOX", "GDPR"],
        answer="PCI DSS"
    ),
    LabScenario(
        domain="Governance, Risk & Compliance",
        title="GDPR Data-Subject Erasure Request",
        log_data="Ticket #884: Right to Erasure – user jean@eu.example",
        question="Which party is RESPONSIBLE for fulfilling this request?",
        choices=["Data Controller", "Data Processor", "DPO", "Supervisor Authority"],
        answer="Data Controller"
    ),
]


    db.session.add_all(labs)
    db.session.commit()
    print("✅ Lab scenario seeded.")
