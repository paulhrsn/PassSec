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
        QuizQuestion(
            domain="Attacks",
            question="What type of attack involves sending fraudulent emails that resemble reputable sources?",
            choices=["Phishing", "DDoS", "Brute Force", "Man-in-the-middle"],
            answer="Phishing",
            explanation="Phishing uses deceptive emails to trick users into revealing credentials or clicking malicious links."
        ),
        QuizQuestion(
            domain="Attacks",
            question="Which attack floods a target with traffic to exhaust bandwidth or resources?",
            choices=["SQL Injection", "DDoS", "Password Spraying", "ARP Spoofing"],
            answer="DDoS",
            explanation="A Distributed Denial of Service (DDoS) attack overwhelms a service with traffic, causing outages."
        ),
        QuizQuestion(
            domain="Attacks",
            question="Which technique attempts many password guesses against a single account?",
            choices=["Brute Force", "Phishing", "Social Engineering", "MITM"],
            answer="Brute Force",
            explanation="A brute-force attack systematically tries all possible passwords until one works."
        ),
        QuizQuestion(
            domain="Attacks",
            question="What threat intercepts and possibly alters communications between two parties?",
            choices=["Ransomware", "Man-in-the-middle", "Tailgating", "Keylogger"],
            answer="Man-in-the-middle",
            explanation="A MITM attack sits between two endpoints, capturing or modifying transmitted data."
        ),
        QuizQuestion(
            domain="Attacks",
            question="Which injection allows attackers to manipulate SQL queries?",
            choices=["XSS", "LDAP Injection", "SQL Injection", "Command Injection"],
            answer="SQL Injection",
            explanation="SQL Injection exploits unsanitized inputs to execute arbitrary database queries."
        ),
        QuizQuestion(
            domain="Attacks",
            question="What is the best mitigation against Cross-Site Scripting (XSS)?",
            choices=["Content-Security-Policy header", "Disable cookies", "Use MD5 hashing", "Port scanning"],
            answer="Content-Security-Policy header",
            explanation="CSP restricts the sources from which scripts can be loaded, blocking injected JavaScript."
        ),
        QuizQuestion(
            domain="Attacks",
            question="Which control prevents ARP spoofing on a switched network?",
            choices=["Dynamic ARP Inspection", "MAC Filtering", "Port Mirroring", "ACLs"],
            answer="Dynamic ARP Inspection",
            explanation="DAI validates ARP packets against a trusted database to prevent spoofed ARP responses."
        ),
        QuizQuestion(
            domain="Attacks",
            question="What technique attempts a small number of common passwords across many accounts?",
            choices=["Credential Stuffing", "Password Spraying", "Brute Force", "Rainbow Table"],
            answer="Password Spraying",
            explanation="Password spraying uses one (or few) passwords against many accounts to avoid lockouts."
        ),
        QuizQuestion(
            domain="Attacks",
            question="Which log entry indicates a Slowloris DoS attack?",
            choices=["High UDP flood", "Partial HTTP requests held open", "Mass SYN resets", "Ping flood"],
            answer="Partial HTTP requests held open",
            explanation="Slowloris holds many HTTP connections open by sending headers slowly to exhaust server threads."
        ),
        QuizQuestion(
            domain="Attacks",
            question="Which DNS control helps prevent cache poisoning?",
            choices=["DNSSEC", "HTTPS", "SSH", "SNMPv3"],
            answer="DNSSEC",
            explanation="DNSSEC digitally signs DNS records so resolvers can verify their authenticity."
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which principle ensures users only get the permissions needed to do their job?",
            choices=["Separation of Duties", "Least Privilege", "Fail-Open", "High Availability"],
            answer="Least Privilege",
            explanation="Least Privilege restricts user/system rights to the minimum necessary."
        ),
        QuizQuestion(
            domain="Architecture",
            question="What concept uses multiple layers of defense to protect assets?",
            choices=["Defense in Depth", "Penalty Box", "Air Gap", "Honeynet"],
            answer="Defense in Depth",
            explanation="Defense in Depth implements overlapping controls so one failure doesn’t expose the system."
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which segmentation technique isolates different trust zones at Layer 2?",
            choices=["VLANs", "Subnets", "VPN", "DMZ"],
            answer="VLANs",
            explanation="VLANs partition a switch into logical LANs, limiting broadcast domains and isolating traffic."
        ),
        QuizQuestion(
            domain="Architecture",
            question="What design model assumes no implicit trust of any user or device?",
            choices=["Zero Trust", "IPA Model", "Bell-LaPadula", "Clark-Wilson"],
            answer="Zero Trust",
            explanation="Zero Trust never trusts automatically; every access request is continually validated."
        ),
        QuizQuestion(
            domain="Architecture",
            question="Which physical control ensures critical servers have no direct Internet connection?",
            choices=["Air Gap", "Port Security", "NAC", "IDS"],
            answer="Air Gap",
            explanation="An air-gapped system is physically isolated from all other networks, including the Internet."
        )
    ]

    db.session.add_all(questions)
    db.session.commit()
    print("\u2705 Quiz questions seeded.")
