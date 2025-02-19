import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from db_connection import get_users_with_expiry, update_email_sent_status

# Send email
def send_email(full_name, email, expiry_date):
    sender_email = "dbmojt@gmail.com"
    sender_password = "yjzv pzne mggq hkfr"
    subject = "Expiry Notification"
    body = f"Dear {full_name},\n\nYour Contract will expire on {expiry_date}.\n\nBest regards,\nYour Company"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        print(f"Email sent to {email}")
        update_email_sent_status(email)  
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

# Main function
def main():
    users = get_users_with_expiry()
    if users is None:
        print("Failed to connect to the database.")
        return

    if not users:
        print("There are no upcoming account expiries.")
        return

    today = datetime.today().date()
    for user in users:
        expiry_date = user['ExpiryDate']
        if expiry_date - today <= timedelta(days=5):
            send_email(user['FullName'], user['Email'], expiry_date)

if __name__ == "__main__":
    main()