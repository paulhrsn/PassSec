import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.quiz import QuizQuestion
from app.models.user_quiz_history import UserQuizHistory

app = create_app()

with app.app_context():
    # Clear quiz data only so user accounts are preserved.
    UserQuizHistory.query.delete()
    QuizQuestion.query.delete()
    db.session.commit()
    db.create_all()

    questions = [
        # Threats
        QuizQuestion(
            domain="Threats",
            question="What type of malware encrypts files and demands payment for decryption?",
            choices=["Ransomware", "Spyware", "Adware", "Rootkit"],
            answer="Ransomware",
            explanation="Ransomware encrypts data or locks systems and asks for payment.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which social engineering attack uses a fabricated scenario to trick a target?",
            choices=["Pretexting", "Phishing", "Tailgating", "Shoulder surfing"],
            answer="Pretexting",
            explanation="Pretexting relies on a believable story to gain trust and extract sensitive data.",
        ),
        QuizQuestion(
            domain="Threats",
            question="What attack uses leaked username/password pairs to attempt logins on other services?",
            choices=["Credential stuffing", "Password spraying", "Brute force", "Replay attack"],
            answer="Credential stuffing",
            explanation="Credential stuffing exploits password reuse across sites.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which attack tricks an authenticated browser into sending an unwanted request?",
            choices=["CSRF", "XSS", "SQL injection", "MITM"],
            answer="CSRF",
            explanation="Cross-site request forgery abuses trust in the browser's active session.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which attack injects malicious script into trusted web content to run in victim browsers?",
            choices=["XSS", "CSRF", "SQL injection", "Command injection"],
            answer="XSS",
            explanation="Cross-site scripting runs attacker-controlled JavaScript in user browsers.",
        ),
        QuizQuestion(
            domain="Threats",
            question="What attack places an adversary between two communicating parties to intercept traffic?",
            choices=["Man-in-the-middle", "DDoS", "Replay", "Buffer overflow"],
            answer="Man-in-the-middle",
            explanation="MITM allows interception and potentially alteration of communications.",
        ),
        QuizQuestion(
            domain="Threats",
            question="What attack sends one common password against many different accounts?",
            choices=["Password spraying", "Credential stuffing", "Brute force", "Dictionary attack"],
            answer="Password spraying",
            explanation="Password spraying avoids lockouts by limiting attempts per account.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which malware type self-replicates across networks without user action?",
            choices=["Worm", "Trojan", "Rootkit", "Adware"],
            answer="Worm",
            explanation="Worms spread automatically by exploiting vulnerabilities.",
        ),

        # Architecture
        QuizQuestion(
            domain="Architecture",
            question="Which principle grants only the minimum permissions required for a task?",
            choices=["Least privilege", "Need to know", "Separation of duties", "Defense in depth"],
            answer="Least privilege",
            explanation="Least privilege reduces blast radius if an account is compromised.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="What model assumes no implicit trust for any user or device?",
            choices=["Zero Trust", "Perimeter model", "RBAC", "DMZ"],
            answer="Zero Trust",
            explanation="Zero Trust requires continuous verification of identity and context.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="What network zone hosts public-facing services while isolating internal systems?",
            choices=["DMZ", "VLAN", "Air gap", "NAT"],
            answer="DMZ",
            explanation="A DMZ reduces risk by separating internet-exposed services from internal assets.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which Layer 2 mechanism creates separate logical broadcast domains on switches?",
            choices=["VLAN", "Subnet", "ACL", "NAT"],
            answer="VLAN",
            explanation="VLANs segment network traffic and improve isolation.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which access model assigns permissions to roles first, then users get roles?",
            choices=["RBAC", "DAC", "MAC", "ABAC"],
            answer="RBAC",
            explanation="Role-based access control scales well in enterprise environments.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="What concept layers multiple controls so one control failure does not expose all assets?",
            choices=["Defense in depth", "Fail open", "Single sign-on", "Flat network"],
            answer="Defense in depth",
            explanation="Layered controls increase attack cost and reduce single points of failure.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which deployment is shared by organizations with similar security/compliance needs?",
            choices=["Community cloud", "Public cloud", "Private cloud", "Hybrid cloud"],
            answer="Community cloud",
            explanation="Community cloud is jointly used by organizations with common requirements.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which technique physically isolates critical systems from any network connection?",
            choices=["Air gap", "VLAN", "NAC", "Proxy"],
            answer="Air gap",
            explanation="Air-gapped systems are disconnected from other networks, including the internet.",
        ),

        # Implementation
        QuizQuestion(
            domain="Implementation",
            question="Which protocol securely provides remote shell access over TCP 22?",
            choices=["SSH", "Telnet", "RDP", "FTP"],
            answer="SSH",
            explanation="SSH encrypts remote administration traffic.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="What protocol secures HTTP traffic with TLS?",
            choices=["HTTPS", "FTPS", "SFTP", "SMB"],
            answer="HTTPS",
            explanation="HTTPS protects web traffic confidentiality and integrity.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which MFA factor category includes fingerprints and facial recognition?",
            choices=["Something you are", "Something you know", "Something you have", "Somewhere you are"],
            answer="Something you are",
            explanation="Biometrics are inherence factors.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which protocol commonly backs 802.1X authentication for wired/wireless access?",
            choices=["RADIUS", "LDAP", "Kerberos", "SNMP"],
            answer="RADIUS",
            explanation="RADIUS provides centralized AAA for network access.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which modern TLS version is recommended and removes many legacy ciphers?",
            choices=["TLS 1.3", "TLS 1.0", "SSL 3.0", "TLS 1.1"],
            answer="TLS 1.3",
            explanation="TLS 1.3 improves security and handshake efficiency.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which DNS control adds signatures to records to detect tampering?",
            choices=["DNSSEC", "DoH", "DoT", "NAT"],
            answer="DNSSEC",
            explanation="DNSSEC validates DNS data authenticity and integrity.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="What email control lists authorized sending hosts in DNS?",
            choices=["SPF", "DKIM", "DMARC", "MX"],
            answer="SPF",
            explanation="SPF helps prevent spoofed sender domains.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which wireless security protocol uses SAE and improves over WPA2-PSK?",
            choices=["WPA3", "WEP", "TKIP", "WPA"],
            answer="WPA3",
            explanation="WPA3 strengthens key exchange and resists offline guessing attacks.",
        ),

        # Operations
        QuizQuestion(
            domain="Operations",
            question="Which platform centralizes and correlates logs for detection and investigation?",
            choices=["SIEM", "IDS", "Firewall", "DLP"],
            answer="SIEM",
            explanation="SIEM tools aggregate and analyze events from multiple systems.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which security control sits inline and actively blocks malicious network traffic?",
            choices=["IPS", "IDS", "Syslog", "Proxy"],
            answer="IPS",
            explanation="An IPS can drop packets and stop attacks in real time.",
        ),
        QuizQuestion(
            domain="Operations",
            question="What term describes a vulnerability exploited before an official patch is available?",
            choices=["Zero-day", "Known issue", "Misconfiguration", "False positive"],
            answer="Zero-day",
            explanation="Zero-day vulnerabilities have no vendor patch at time of exploitation.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which assessment attempts real exploitation with approval to validate impact?",
            choices=["Penetration testing", "Vulnerability scan", "Risk register", "Patch management"],
            answer="Penetration testing",
            explanation="Pen testing simulates attackers to confirm exploitability and risk.",
        ),
        QuizQuestion(
            domain="Operations",
            question="What decoy system is intentionally exposed to attract and study attackers?",
            choices=["Honeypot", "Jump box", "Bastion host", "SOAR"],
            answer="Honeypot",
            explanation="Honeypots gather attacker behavior and provide early warning.",
        ),
        QuizQuestion(
            domain="Operations",
            question="What process ensures forensic evidence handling is traceable and admissible?",
            choices=["Chain of custody", "Order of volatility", "Data minimization", "Tokenization"],
            answer="Chain of custody",
            explanation="Chain of custody documents who handled evidence and when.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which backup type saves only data changed since the last backup of any type?",
            choices=["Incremental", "Differential", "Full", "Synthetic full"],
            answer="Incremental",
            explanation="Incremental backups reduce storage/time but can lengthen restore chains.",
        ),
        QuizQuestion(
            domain="Operations",
            question="What endpoint technology records host telemetry for detection and response?",
            choices=["EDR", "NAC", "WAF", "SIEM"],
            answer="EDR",
            explanation="EDR improves endpoint visibility and supports containment actions.",
        ),

        # Governance
        QuizQuestion(
            domain="Governance",
            question="Which risk strategy uses insurance to shift financial loss to a third party?",
            choices=["Risk transfer", "Risk acceptance", "Risk avoidance", "Risk mitigation"],
            answer="Risk transfer",
            explanation="Cyber insurance is a common risk transfer mechanism.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which standard applies to merchants processing payment card data?",
            choices=["PCI DSS", "HIPAA", "SOX", "GDPR"],
            answer="PCI DSS",
            explanation="PCI DSS defines controls for cardholder data environments.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which regulation governs personal data protection for EU residents?",
            choices=["GDPR", "FERPA", "SOX", "GLBA"],
            answer="GDPR",
            explanation="GDPR establishes strict privacy and data subject rights.",
        ),
        QuizQuestion(
            domain="Governance",
            question="What metric defines the maximum acceptable downtime for a service?",
            choices=["RTO", "RPO", "MTBF", "SLE"],
            answer="RTO",
            explanation="Recovery Time Objective sets the service restoration deadline.",
        ),
        QuizQuestion(
            domain="Governance",
            question="What metric defines the maximum acceptable data loss in time?",
            choices=["RPO", "RTO", "ARO", "SLA"],
            answer="RPO",
            explanation="Recovery Point Objective sets how old recovered data may be.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which policy defines allowed and prohibited use of company IT resources?",
            choices=["Acceptable Use Policy", "NDA", "SLA", "MOU"],
            answer="Acceptable Use Policy",
            explanation="An AUP sets behavioral expectations for system and network usage.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which analysis identifies critical business functions and downtime impact?",
            choices=["Business Impact Analysis", "Threat hunting", "Pen test", "Code review"],
            answer="Business Impact Analysis",
            explanation="A BIA helps prioritize recovery and continuity planning.",
        ),
        QuizQuestion(
            domain="Governance",
            question="What agreement defines availability and performance commitments from a provider?",
            choices=["SLA", "AUP", "NDA", "KPI"],
            answer="SLA",
            explanation="Service level agreements define expected service metrics and remedies.",
        ),

        # Cryptography
        QuizQuestion(
            domain="Cryptography",
            question="Which encryption type uses one shared key for encryption and decryption?",
            choices=["Symmetric", "Asymmetric", "Hashing", "Tokenization"],
            answer="Symmetric",
            explanation="Symmetric encryption is fast but requires secure key distribution.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which algorithm is the modern standard for symmetric encryption?",
            choices=["AES", "DES", "RC4", "MD5"],
            answer="AES",
            explanation="AES is the widely accepted modern symmetric cipher standard.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which asymmetric algorithm is based on integer factorization difficulty?",
            choices=["RSA", "AES", "ChaCha20", "SHA-256"],
            answer="RSA",
            explanation="RSA uses public and private keys and is common in PKI.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which algorithm offers strong security with relatively small key sizes?",
            choices=["ECC", "RSA-512", "DES", "3DES"],
            answer="ECC",
            explanation="Elliptic curve cryptography is efficient for mobile and constrained devices.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which property ensures data has not been altered in transit?",
            choices=["Integrity", "Confidentiality", "Availability", "Non-repudiation"],
            answer="Integrity",
            explanation="Integrity is validated with hashes, HMACs, or signatures.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="What mechanism combines a secret key with a hash to prove integrity and authenticity?",
            choices=["HMAC", "CRC", "MD5", "Base64"],
            answer="HMAC",
            explanation="HMAC protects message integrity and origin authenticity when shared keys are trusted.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which protocol checks real-time certificate revocation status?",
            choices=["OCSP", "CRL", "DNSSEC", "NTP"],
            answer="OCSP",
            explanation="OCSP provides certificate status without downloading full CRLs.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which cryptographic goal prevents a sender from denying they sent a message?",
            choices=["Non-repudiation", "Confidentiality", "Integrity", "Availability"],
            answer="Non-repudiation",
            explanation="Digital signatures are used to support non-repudiation.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which attack uses deceptive text messages to trick users into revealing sensitive data?",
            choices=["Smishing", "Vishing", "Pretexting", "Watering hole"],
            answer="Smishing",
            explanation="Smishing is phishing delivered through SMS or messaging platforms.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which attack redirects users from legitimate websites to malicious ones by corrupting DNS responses?",
            choices=["Pharming", "Spoofing", "Typosquatting", "Replay"],
            answer="Pharming",
            explanation="Pharming manipulates DNS resolution to send victims to attacker-controlled sites.",
        ),
        QuizQuestion(
            domain="Threats",
            question="What term describes unauthorized software designed to steal user activity and credentials silently?",
            choices=["Spyware", "Adware", "Rootkit", "Worm"],
            answer="Spyware",
            explanation="Spyware covertly collects information such as browsing data and credentials.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which software supply chain attack technique injects malicious code into trusted updates?",
            choices=["Compromised update", "Session hijacking", "ARP poisoning", "Smurf"],
            answer="Compromised update",
            explanation="Attackers can tamper with trusted update channels to distribute malware broadly.",
        ),
        QuizQuestion(
            domain="Threats",
            question="Which attack intentionally overwhelms CPU and memory by opening many half-open TCP connections?",
            choices=["SYN flood", "Ping flood", "Smurf", "DNS tunneling"],
            answer="SYN flood",
            explanation="SYN flood consumes server resources by abusing TCP handshake behavior.",
        ),
        QuizQuestion(
            domain="Threats",
            question="What threat occurs when malicious code activates only when a specific condition is met?",
            choices=["Logic bomb", "Rootkit", "Adware", "Spyware"],
            answer="Logic bomb",
            explanation="Logic bombs trigger on specific events such as dates or user actions.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which architecture principle requires explicit verification for each access request?",
            choices=["Never trust, always verify", "Single sign-on", "Implicit trust", "Default allow"],
            answer="Never trust, always verify",
            explanation="This is a core tenet of Zero Trust architecture.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which control type limits network communication between workloads in the same environment?",
            choices=["Microsegmentation", "Port mirroring", "Link aggregation", "NAT"],
            answer="Microsegmentation",
            explanation="Microsegmentation reduces lateral movement by enforcing granular policy boundaries.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which resiliency design uses redundant systems across different locations?",
            choices=["Geographic redundancy", "Single region", "Hot desking", "Thin provisioning"],
            answer="Geographic redundancy",
            explanation="Distributing systems across sites improves resilience against regional outages.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="What architecture pattern places security controls between user and private app without exposing the app publicly?",
            choices=["Reverse proxy", "Open relay", "Port forwarding", "Hub-and-spoke routing"],
            answer="Reverse proxy",
            explanation="Reverse proxies mediate access and hide backend service details.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which physical security model requires two independent authentication forms to access a secure room?",
            choices=["Mantrap", "Tailgating", "Hot aisle", "Biometric-only"],
            answer="Mantrap",
            explanation="Mantraps enforce controlled access and reduce piggybacking risk.",
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which trust model uses dedicated hardware roots to validate platform integrity at boot?",
            choices=["Measured boot", "Warm restart", "Failover boot", "Snapshot restore"],
            answer="Measured boot",
            explanation="Measured boot records component integrity measurements during startup.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which protocol secures directory queries and authentication over TLS?",
            choices=["LDAPS", "LDAP", "Kerberos", "RADIUS"],
            answer="LDAPS",
            explanation="LDAPS encrypts directory traffic that would otherwise be in clear text.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which mechanism verifies endpoint health before granting network access?",
            choices=["NAC", "SIEM", "PKI", "SOAR"],
            answer="NAC",
            explanation="Network Access Control checks compliance posture before admitting devices.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which process validates software integrity and publisher identity before installation?",
            choices=["Code signing verification", "Network segmentation", "Log rotation", "Rate limiting"],
            answer="Code signing verification",
            explanation="Signature verification helps prevent tampered or untrusted software execution.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which security control enforces browser policy to restrict script sources and reduce XSS impact?",
            choices=["Content Security Policy", "HSTS", "CORS wildcard", "X-Forwarded-For"],
            answer="Content Security Policy",
            explanation="CSP limits where active content can load from, reducing script injection abuse.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which method stores user passwords safely by combining salt and a slow hash function?",
            choices=["Salted adaptive hashing", "Base64 encoding", "Symmetric encryption", "Plain SHA-1"],
            answer="Salted adaptive hashing",
            explanation="Adaptive hashing with salt resists brute force and rainbow table attacks.",
        ),
        QuizQuestion(
            domain="Implementation",
            question="Which certificate field must match the hostname clients connect to for TLS validation?",
            choices=["Subject Alternative Name", "Issuer DN", "Serial number", "Key usage"],
            answer="Subject Alternative Name",
            explanation="Modern TLS clients validate hostnames against SAN entries.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which SOC process proactively searches for hidden adversary activity not yet detected by alerts?",
            choices=["Threat hunting", "Patch management", "Business continuity", "Configuration audit"],
            answer="Threat hunting",
            explanation="Threat hunting uses hypotheses and telemetry to find stealthy threats.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which incident response action isolates affected systems to stop spread while preserving evidence?",
            choices=["Containment", "Eradication", "Recovery", "Postmortem"],
            answer="Containment",
            explanation="Containment limits blast radius and prevents additional compromise.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which operation removes attacker artifacts and closes exploited vulnerabilities after containment?",
            choices=["Eradication", "Identification", "Preparation", "Tabletop"],
            answer="Eradication",
            explanation="Eradication removes root causes before restoring normal operations.",
        ),
        QuizQuestion(
            domain="Operations",
            question="Which process restores systems to production and monitors for recurrence after eradication?",
            choices=["Recovery", "Containment", "Triage", "Attribution"],
            answer="Recovery",
            explanation="Recovery focuses on safe return to normal services.",
        ),
        QuizQuestion(
            domain="Operations",
            question="What exercise walks stakeholders through a hypothetical incident to test plans and roles?",
            choices=["Tabletop exercise", "Chaos engineering", "Load test", "Data retention"],
            answer="Tabletop exercise",
            explanation="Tabletop exercises validate response readiness and communication flows.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which risk treatment strategy stops an activity entirely to eliminate associated risk?",
            choices=["Risk avoidance", "Risk transfer", "Risk acceptance", "Risk sharing"],
            answer="Risk avoidance",
            explanation="Risk avoidance removes exposure by ceasing the risky activity.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which risk treatment strategy acknowledges risk and takes no additional action?",
            choices=["Risk acceptance", "Risk mitigation", "Risk transfer", "Risk avoidance"],
            answer="Risk acceptance",
            explanation="Risk acceptance is chosen when risk is within tolerance or mitigation cost is too high.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which document describes organizational expectations for incident handling roles and escalation paths?",
            choices=["Incident response policy", "Runbook template", "Patch report", "Pen test scope"],
            answer="Incident response policy",
            explanation="Policy defines authority, responsibilities, and high-level process requirements.",
        ),
        QuizQuestion(
            domain="Governance",
            question="What metric estimates expected annual loss from a specific risk scenario?",
            choices=["ALE", "RTO", "RPO", "MTTR"],
            answer="ALE",
            explanation="Annualized Loss Expectancy estimates yearly financial risk impact.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which privacy principle limits collection to only data necessary for a defined purpose?",
            choices=["Data minimization", "Data replication", "Data warehousing", "Data escrow"],
            answer="Data minimization",
            explanation="Data minimization reduces privacy and breach impact by collecting less sensitive data.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which PKI trust anchor is kept highly protected and signs intermediate CA certificates?",
            choices=["Root CA", "Intermediate CA", "OCSP responder", "RA"],
            answer="Root CA",
            explanation="The root CA anchors trust for the certificate hierarchy.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which certificate status method distributes a signed list of revoked certificates periodically?",
            choices=["CRL", "OCSP", "CSR", "CMP"],
            answer="CRL",
            explanation="Certificate Revocation Lists are published snapshots of revoked cert serials.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which technique derives encryption keys from user passwords using configurable work factors?",
            choices=["PBKDF2", "Base64", "XOR", "CRC32"],
            answer="PBKDF2",
            explanation="PBKDF2 slows brute force through iteration count and salt.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="What property in TLS protects past sessions even if a server private key is later compromised?",
            choices=["Forward secrecy", "Non-repudiation", "Integrity", "Availability"],
            answer="Forward secrecy",
            explanation="Ephemeral key exchange prevents decryption of prior captured traffic.",
        ),
        QuizQuestion(
            domain="Cryptography",
            question="Which operation transforms plaintext into unreadable ciphertext using a key?",
            choices=["Encryption", "Hashing", "Tokenization", "Normalization"],
            answer="Encryption",
            explanation="Encryption protects confidentiality by requiring a key to reverse the process.",
        ),
        QuizQuestion(
            domain="Governance",
            question="Which formal process identifies and prioritizes risks by likelihood and business impact?",
            choices=["Risk assessment", "Patch management", "Threat hunting", "Code signing"],
            answer="Risk assessment",
            explanation="Risk assessments support treatment decisions like mitigation, transfer, or acceptance."
        )
    ]

    db.session.add_all(questions)
    db.session.commit()

    domain_count = len({q.domain for q in questions})
    print(f"Seeded {len(questions)} quiz questions across {domain_count} domains.")
