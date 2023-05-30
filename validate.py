import csv
import re
import smtplib
import dns.resolver

def is_valid_email(email):
    # Email syntax validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Split email address into user and domain
    user, domain = email.split('@')

    try:
        # DNS lookup to validate domain
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return False

        # SMTP verification
        smtp_server = str(mx_records[0].exchange)
        with smtplib.SMTP(smtp_server) as server:
            # Send 'HELO' command
            server.helo()

            # Send 'MAIL FROM' command
            server.mail('your_email@example.com')

            # Send 'RCPT TO' command
            response = server.rcpt(email)

            # Check if email address is deliverable
            if response[0] == 250:
                return True

    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
        return False
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False

    return False

# Read email addresses from a .csv file
emails = []
with open('email_input.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        emails.extend(row)

# Validate email addresses and write to a CSV file
with open('email_list.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Email Address', 'Validity'])

    for email in emails:
        if is_valid_email(email):
            writer.writerow([email, 'Valid'])
        else:
            writer.writerow([email, 'Invalid'])

print("Email list has been saved to 'email_list.csv'")
