import smtplib
from .models import Setup

def send_email(reciever, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    sender = Setup.query.filter_by(id=1).first().email_addr
    app_password = Setup.query.filter_by(id=1).first().email_key

    s.login(sender, app_password)

    # sending the mail
    s.sendmail(sender, reciever, message)

    s.quit()

def exchange_notification(pairs):
    for pair in pairs:
        subject = "Giftpal - New Pair"
        body = """

        You have been paired with """ + pair.receiver.first_name + " " + pair.receiver.last_name + """ for """ + pair.group.group_name + """!
        
        """
        message = f"Subject: {subject}\n{body}"
        send_email(pair.giver.email, message)

def reminder_notification():
    test = 'test'
