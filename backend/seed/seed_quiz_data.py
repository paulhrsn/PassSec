# seed/seed_quiz_data.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.quiz import QuizQuestion

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    questions = [
        # ───────────────────────── 1. ATTACKS & THREATS ─────────────────────────
        QuizQuestion(
            question="What type of attack involves sending fraudulent emails that resemble reputable sources?",
            choices=["Phishing", "DDoS", "Brute Force", "Man-in-the-middle"],
            answer="Phishing",
            explanation="Phishing uses deceptive emails to trick users into revealing credentials or clicking malicious links."
        ),
        QuizQuestion(
            question="Which attack floods a target with traffic to exhaust bandwidth or resources?",
            choices=["SQL Injection", "DDoS", "Password Spraying", "ARP Spoofing"],
            answer="DDoS",
            explanation="A Distributed Denial of Service (DDoS) attack overwhelms a service with traffic, causing outages."
        ),
        QuizQuestion(
            question="Which technique attempts many password guesses against a single account?",
            choices=["Brute Force", "Phishing", "Social Engineering", "MITM"],
            answer="Brute Force",
            explanation="A brute-force attack systematically tries all possible passwords until one works."
        ),
        QuizQuestion(
            question="What threat intercepts and possibly alters communications between two parties?",
            choices=["Ransomware", "Man-in-the-middle", "Tailgating", "Keylogger"],
            answer="Man-in-the-middle",
            explanation="A MITM attack sits between two endpoints, capturing or modifying transmitted data."
        ),
        QuizQuestion(
            question="Which injection allows attackers to manipulate SQL queries?",
            choices=["XSS", "LDAP Injection", "SQL Injection", "Command Injection"],
            answer="SQL Injection",
            explanation="SQL Injection exploits unsanitized inputs to execute arbitrary database queries."
        ),
        QuizQuestion(
            question="What is the best mitigation against Cross-Site Scripting (XSS)?",
            choices=["Content-Security-Policy header", "Disable cookies", "Use MD5 hashing", "Port scanning"],
            answer="Content-Security-Policy header",
            explanation="CSP restricts the sources from which scripts can be loaded, blocking injected JavaScript."
        ),
        QuizQuestion(
            question="Which control prevents ARP spoofing on a switched network?",
            choices=["Dynamic ARP Inspection", "MAC Filtering", "Port Mirroring", "ACLs"],
            answer="Dynamic ARP Inspection",
            explanation="DAI validates ARP packets against a trusted database to prevent spoofed ARP responses."
        ),
        QuizQuestion(
            question="What technique attempts a small number of common passwords across many accounts?",
            choices=["Credential Stuffing", "Password Spraying", "Brute Force", "Rainbow Table"],
            answer="Password Spraying",
            explanation="Password spraying uses one (or few) passwords against many accounts to avoid lockouts."
        ),
        QuizQuestion(
            question="Which log entry indicates a Slowloris DoS attack?",
            choices=["High UDP flood", "Partial HTTP requests held open", "Mass SYN resets", "Ping flood"],
            answer="Partial HTTP requests held open",
            explanation="Slowloris holds many HTTP connections open by sending headers slowly to exhaust server threads."
        ),
        QuizQuestion(
            question="Which DNS control helps prevent cache poisoning?",
            choices=["DNSSEC", "HTTPS", "SSH", "SNMPv3"],
            answer="DNSSEC",
            explanation="DNSSEC digitally signs DNS records so resolvers can verify their authenticity."
        ),

        # ───────────────────────── 2. ARCHITECTURE & DESIGN ─────────────────────────
        QuizQuestion(
            question="Which principle ensures users only get the permissions needed to do their job?",
            choices=["Separation of Duties", "Least Privilege", "Fail-Open", "High Availability"],
            answer="Least Privilege",
            explanation="Least Privilege restricts user/system rights to the minimum necessary."
        ),
        QuizQuestion(
            question="What concept uses multiple layers of defense to protect assets?",
            choices=["Defense in Depth", "Penalty Box", "Air Gap", "Honeynet"],
            answer="Defense in Depth",
            explanation="Defense in Depth implements overlapping controls so one failure doesn’t expose the system."
        ),
        QuizQuestion(
            question="Which segmentation technique isolates different trust zones at Layer 2?",
            choices=["VLANs", "Subnets", "VPN", "DMZ"],
            answer="VLANs",
            explanation="VLANs partition a switch into logical LANs, limiting broadcast domains and isolating traffic."
        ),
        QuizQuestion(
            question="What design model assumes no implicit trust of any user or device?",
            choices=["Zero Trust", "IPA Model", "Bell-LaPadula", "Clark-Wilson"],
            answer="Zero Trust",
            explanation="Zero Trust never trusts automatically; every access request is continually validated."
        ),
        QuizQuestion(
            question="Which physical control ensures critical servers have no direct Internet connection?",
            choices=["Air Gap", "Port Security", "NAC", "IDS"],
            answer="Air Gap",
            explanation="An air-gapped system is physically isolated from all other networks, including the Internet."
        ),
        QuizQuestion(
            question="Which high-level design principle mandates default deny then allow specific traffic?",
            choices=["Implicit Deny", "Fail-Open", "Least Functionality", "Default Permit"],
            answer="Implicit Deny",
            explanation="Implicit Deny blocks all traffic by default; administrators explicitly allow needed traffic."
        ),
        QuizQuestion(
            question="Which zone typically hosts externally-facing web servers?",
            choices=["DMZ", "Intranet", "Extranet", "Sandbox"],
            answer="DMZ",
            explanation="A DMZ is a buffer zone for public-facing services, separated from the internal network."
        ),
        QuizQuestion(
            question="What is the primary goal of network segmentation?",
            choices=["Reduce broadcast domains", "Improve CPU performance", "Eliminate encryption", "Increase packet size"],
            answer="Reduce broadcast domains",
            explanation="Segmentation limits broadcast traffic and contains potential breaches to smaller network segments."
        ),
        QuizQuestion(
            question="Which model focuses on confidentiality using security labels and clearances?",
            choices=["Bell-LaPadula", "Biba", "Clark-Wilson", "Brewer-Nash"],
            answer="Bell-LaPadula",
            explanation="Bell-LaPadula enforces “no read up, no write down” to protect data confidentiality."
        ),
        QuizQuestion(
            question="Which control type is a security policy, standard, or guideline?",
            choices=["Administrative", "Technical", "Physical", "Logical"],
            answer="Administrative",
            explanation="Administrative controls are documented policies and procedures guiding security behavior."
        ),

        # ───────────────────────── 3. IMPLEMENTATION ────────────────────────────
        QuizQuestion(
            question="Which secure coding practice prevents SQL Injection?",
            choices=["Prepared Statements", "Client-side Validation", "Using AJAX", "MD5 hashing"],
            answer="Prepared Statements",
            explanation="Prepared statements separate code from data, preventing user input from altering SQL logic."
        ),
        QuizQuestion(
            question="What port does HTTPS use by default?",
            choices=["443", "80", "22", "21"],
            answer="443",
            explanation="HTTPS (HTTP over TLS) listens on TCP port 443 by convention."
        ),
        QuizQuestion(
            question="Which protocol secures email in transit using opportunistic TLS?",
            choices=["STARTTLS", "SMB", "SNMP", "ICMP"],
            answer="STARTTLS",
            explanation="STARTTLS upgrades plaintext SMTP connections to encrypted TLS when both ends support it."
        ),
        QuizQuestion(
            question="Which wireless security standard introduced Protected Management Frames?",
            choices=["802.11w", "WPA2-PSK", "WEP", "EAP-TLS"],
            answer="802.11w",
            explanation="802.11w protects management frames (like disassociation) from forging."
        ),
        QuizQuestion(
            question="Which authentication method uses a digital certificate on both client and server?",
            choices=["Mutual TLS", "Pre-Shared Key", "OAuth", "Kerberos"],
            answer="Mutual TLS",
            explanation="Mutual TLS requires both ends to present and verify X.509 certificates."
        ),
        QuizQuestion(
            question="What is the main benefit of using a Web Application Firewall (WAF)?",
            choices=["Blocks common HTTP attacks", "Encrypts data at rest", "Performs backups", "Monitors network latency"],
            answer="Blocks common HTTP attacks",
            explanation="A WAF filters and monitors HTTP(S) traffic to protect web apps from attacks like XSS or SQLi."
        ),
        QuizQuestion(
            question="Which container runtime capability should you drop to prevent escapes?",
            choices=["CAP_SYS_ADMIN", "CAP_NET_RAW", "CAP_CHOWN", "CAP_DAC_READ_SEARCH"],
            answer="CAP_SYS_ADMIN",
            explanation="Dropping CAP_SYS_ADMIN removes broad privileges that attackers can abuse for container escape."
        ),
        QuizQuestion(
            question="Which Identity-as-Code tool can enforce policy on Terraform plans?",
            choices=["Sentinel", "Ansible", "Chef", "Puppet"],
            answer="Sentinel",
            explanation="HashiCorp Sentinel integrates policy checks directly into Terraform plans before apply."
        ),
        QuizQuestion(
            question="Which SAST tool analysis runs at build time to find code flaws?",
            choices=["Static Application Security Testing", "Dynamic Analysis", "Penetration Testing", "Fuzzing"],
            answer="Static Application Security Testing",
            explanation="SAST analyzes source code or binaries without executing them, catching vulnerabilities early."
        ),
        QuizQuestion(
            question="What is the primary function of an Intrusion Prevention System (IPS)?",
            choices=["Block malicious traffic in real-time", "Log all traffic", "Encrypt data", "Scan for viruses"],
            answer="Block malicious traffic in real-time",
            explanation="An IPS actively blocks or rejects traffic identified as malicious."
        ),

        # ───────────────────────── 4. OPERATIONS & INCIDENT RESPONSE ─────────────────
        QuizQuestion(
            question="Which phase of Incident Response includes containment and eradication?",
            choices=["Containment, Eradication & Recovery", "Preparation", "Identification", "Lessons Learned"],
            answer="Containment, Eradication & Recovery",
            explanation="After identifying an incident, the IR team contains, eradicates the threat, then recovers services."
        ),
        QuizQuestion(
            question="What is the first step in Digital Forensics?",
            choices=["Preserve the evidence", "Eradicate malware", "Notify law enforcement", "Restore backups"],
            answer="Preserve the evidence",
            explanation="Chain of custody begins by preserving evidence to maintain integrity and admissibility."
        ),
        QuizQuestion(
            question="Which tool captures a forensic disk image?",
            choices=["dd", "nmap", "Metasploit", "Wireshark"],
            answer="dd",
            explanation="Linux dd can create a bit-for-bit copy of a drive for offline analysis."
        ),
        QuizQuestion(
            question="What control uses behavioral analytics to detect anomalies?",
            choices=["UEBA", "ACLs", "NAC", "WAF"],
            answer="UEBA",
            explanation="User and Entity Behavior Analytics (UEBA) spots deviations from normal baselines."
        ),
        QuizQuestion(
            question="Which backup type only copies changes since the last full backup?",
            choices=["Incremental", "Full", "Differential", "Snapshot"],
            answer="Incremental",
            explanation="Incremental backups copy only the data changed since the last full or incremental backup."
        ),
        QuizQuestion(
            question="What process tests backups by performing a trial restore?",
            choices=["Automated Test Restore", "Data Deduplication", "Snapshot", "Mirroring"],
            answer="Automated Test Restore",
            explanation="Regular test restores confirm backup integrity and the ability to recover data."
        ),

        # ───────────────────────── 5. GOVERNANCE, RISK & COMPLIANCE ────────────────
        QuizQuestion(
            question="Which framework requires protecting cardholder data at rest and in transit?",
            choices=["PCI DSS", "HIPAA", "SOX", "GDPR"],
            answer="PCI DSS",
            explanation="PCI DSS mandates encryption of cardholder data both at rest and over public networks."
        ),
        QuizQuestion(
            question="Under GDPR, what grant gives individuals the right to have their data erased?",
            choices=["Right to Erasure", "Right to Access", "Right to Portability", "Right to Restrict"],
            answer="Right to Erasure",
            explanation="GDPR’s Right to Erasure (Article 17) lets data subjects request deletion of personal data."
        ),
        QuizQuestion(
            question="Which policy documents acceptable technology use by employees?",
            choices=["Acceptable Use Policy", "Business Continuity Plan", "Incident Response Plan", "Configuration Standard"],
            answer="Acceptable Use Policy",
            explanation="AUPs define what users can and cannot do with organizational IT resources."
        ),
        QuizQuestion(
            question="What risk response shares risk with a third party?",
            choices=["Transfer", "Mitigate", "Avoid", "Accept"],
            answer="Transfer",
            explanation="Transferring risk (e.g., via insurance) moves financial exposure to another entity."
        ),
        QuizQuestion(
            question="Which audit type assesses operational effectiveness over time?",
            choices=["SOC 2 Type II", "SOC 1", "PCI SAQ", "HIPAA Audit"],
            answer="SOC 2 Type II",
            explanation="SOC 2 Type II reports test and verify controls over a period rather than at a single point in time."
        ),
        QuizQuestion(
            question="Which metric defines maximum tolerable data loss?",
            choices=["RPO", "RTO", "MTBF", "MTTR"],
            answer="RPO",
            explanation="Recovery Point Objective (RPO) specifies how much data loss (time) is acceptable after a disruption."
        ),

        # ───────────────────────── 6. IDENTITY & ACCESS MANAGEMENT ─────────────────
        QuizQuestion(
            question="Which factor category is something you are?",
            choices=["Biometric", "Token", "Password", "Proximity Card"],
            answer="Biometric",
            explanation="Biometrics (fingerprint, retina) are inherence factors based on physical traits."
        ),
        QuizQuestion(
            question="What protocol enables Single Sign-On in web federations?",
            choices=["SAML", "SSH", "RADIUS", "LDAP"],
            answer="SAML",
            explanation="Security Assertion Markup Language (SAML) exchanges authentication and authorization data."
        ),
        QuizQuestion(
            question="Which service issues and manages digital certificates?",
            choices=["Certificate Authority", "Kerberos", "RADIUS", "TACACS+"],
            answer="Certificate Authority",
            explanation="CAs sign and renew X.509 certificates used for SSL/TLS and other PKI services."
        ),
        QuizQuestion(
            question="What AAA protocol encrypts only the payload and not the entire session?",
            choices=["TACACS+", "RADIUS", "LDAP", "TLS"],
            answer="RADIUS",
            explanation="RADIUS encrypts the user’s password but leaves other parts of the packet in cleartext."
        ),
        QuizQuestion(
            question="Which control enforces a lockout after too many failed logins?",
            choices=["Account Lockout Policy", "Password Complexity", "Idle Timeout", "MFA"],
            answer="Account Lockout Policy",
            explanation="Lockout policies block an account after a set number of failed attempts to slow brute-force attacks."
        ),

        # ───────────────────────── 7. CRYPTOGRAPHY & PKI ──────────────────────────
        QuizQuestion(
            question="Which symmetric algorithm is approved for encrypting data at rest?",
            choices=["AES", "RSA", "SHA-256", "ECC"],
            answer="AES",
            explanation="AES is a widely adopted block cipher for data encryption at rest or in transit."
        ),
        QuizQuestion(
            question="What algorithm is used for hashing messages to ensure integrity?",
            choices=["SHA-256", "RSA", "AES", "3DES"],
            answer="SHA-256",
            explanation="SHA-256 produces a fixed-length hash to verify that data has not been altered."
        ),
        QuizQuestion(
            question="Which asymmetric algorithm is used for digital signatures?",
            choices=["RSA", "MD5", "Blowfish", "RC4"],
            answer="RSA",
            explanation="RSA supports encryption, key exchange, and digital signing using public/private keys."
        ),
        QuizQuestion(
            question="What is the primary purpose of a digital certificate?",
            choices=["Bind a public key to an identity", "Encrypt data at rest", "Block malware", "Hash passwords"],
            answer="Bind a public key to an identity",
            explanation="Certificates issued by a CA vouch for the identity associated with a public key."
        ),
        QuizQuestion(
            question="Which key exchange protocol provides perfect forward secrecy?",
            choices=["Diffie-Hellman Ephemeral (DHE)", "RSA key wrap", "MD5 handshake", "AES-GCM"],
            answer="Diffie-Hellman Ephemeral (DHE)",
            explanation="DHE generates a new session key each handshake, so past sessions can’t be decrypted if the key is compromised."
        ),

        # ───────────────────────── 8. NETWORK HARDENING & SECURITY ────────────────
        QuizQuestion(
            question="Which SNMP version adds encryption and authentication?",
            choices=["SNMPv3", "SNMPv2c", "SNMPv1", "SNMPv2u"],
            answer="SNMPv3",
            explanation="SNMPv3 secures management traffic via user-based authentication and optional encryption."
        ),
        QuizQuestion(
            question="What NTP misconfiguration can lead to authentication failures in Kerberos?",
            choices=["Time drift", "Open UDP port 69", "DNS spoofing", "ARP poisoning"],
            answer="Time drift",
            explanation="Kerberos relies on closely synchronized clocks; NTP drift can cause ticket validation errors."
        ),
        QuizQuestion(
            question="Which device inspects traffic at Layers 2 through 7?",
            choices=["Next-Generation Firewall (NGFW)", "Hub", "Bridge", "Repeater"],
            answer="Next-Generation Firewall (NGFW)",
            explanation="NGFWs combine traditional firewall functions with application-level inspection and intrusion prevention."
        ),
        QuizQuestion(
            question="What is the primary purpose of Network Access Control (NAC)?",
            choices=["Enforce endpoint compliance before granting network access",
                     "Filter outbound email",
                     "Encrypt all VLAN traffic",
                     "Monitor physical access"],
            answer="Enforce endpoint compliance before granting network access",
            explanation="NAC checks device health (patches, AV) and only permits access if policies are met."
        ),
        QuizQuestion(
            question="Which tunneling protocol is used to create a secure site-to-site VPN?",
            choices=["IPsec", "FTP", "SMTP", "ARP"],
            answer="IPsec",
            explanation="IPsec VPNs encrypt and authenticate IP packets between two network endpoints."
        ),

        # ───────────────────────── 9. PHYSICAL & SOCIAL ENGINEERING ───────────────
        QuizQuestion(
            question="What social engineering tactic drops USBs to entice users to plug them in?",
            choices=["USB drop", "Phishing", "Tailgating", "Shoulder surfing"],
            answer="USB drop",
            explanation="Attackers leave infected USB drives hoping curious users will plug them in and execute malware."
        ),
        QuizQuestion(
            question="Which control prevents unauthorized entry by requiring badge reuse on exit before re-entry?",
            choices=["Anti-passback", "Mantrap", "Bollard", "Biometrics"],
            answer="Anti-passback",
            explanation="Anti-passback ensures a badge exit is recorded before it can be used to re-enter."
        ),
        QuizQuestion(
            question="Dumpster diving is a form of which type of attack?",
            choices=["Information gathering", "DDoS", "Ransomware", "Watering hole"],
            answer="Information gathering",
            explanation="Attackers search discarded materials for sensitive info like passwords or network diagrams."
        ),
        QuizQuestion(
            question="What control can prevent piggybacking through a secure door?",
            choices=["Security guard", "Honey Pot", "VPN", "ACL"],
            answer="Security guard",
            explanation="Human security personnel can verify identities and prevent unauthorized follow-ins."
        ),
        QuizQuestion(
            question="Which malicious device emulates a USB keyboard to send commands when plugged in?",
            choices=["Rubber Ducky", "Phantom", "Malbolt", "Keylogger"],
            answer="Rubber Ducky",
            explanation="A USB “Rubber Ducky” injects pre-programmed keystrokes to compromise systems instantly."
        ),
    ]

    # add and commit
    db.session.add_all(questions)
    db.session.commit()
    print("✅ Quiz questions seeded.")
