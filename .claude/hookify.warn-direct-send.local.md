---
name: warn-direct-send
enabled: true
event: file
action: warn
conditions:
  - field: new_text
    operator: regex_match
    pattern: smtplib\.SMTP|sendmail\(|send_message\(
---

**Direct SMTP usage detected!**

All email sending MUST go through `outreach/email_sender.py` which enforces:
1. SHA-256 payload hash verification (tamper detection)
2. DNC checks at BOTH draft time AND send time
3. Atomic rate limits (BEGIN IMMEDIATE transaction)
4. CAN-SPAM compliance (physical address, unsubscribe link)
5. Sandbox mode (OUTREACH_SMTP_SANDBOX=true by default)

Never bypass the email sender — it's the single enforcement point for all outbound email.
