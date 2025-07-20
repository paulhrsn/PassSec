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

    lab = LabScenario(
        title="Phishing Log Investigation",
        log_data="""
Jul 12 10:33:21 mailserver postfix/smtpd[12345]: connect from unknown[192.168.1.45]
Jul 12 10:33:22 mailserver postfix/smtpd[12345]: NOQUEUE: reject: RCPT from unknown[192.168.1.45]: 550 5.7.1 Access denied
Jul 12 10:33:23 mailserver postfix/smtpd[12345]: disconnect from unknown[192.168.1.45]
        """.strip(),
        question="What kind of attack is shown in the log?",
        choices=[
            "Credential Harvesting",
            "SQL Injection",
            "Ransomware",
            "Man-in-the-Middle"
        ],
        answer="Credential Harvesting"
    )

    db.session.add(lab)
    db.session.commit()
    print("✅ Lab scenario seeded.")
