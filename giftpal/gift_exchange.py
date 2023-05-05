import random
from giftpal.models import db, User, Pair, Group
from email.message import EmailMessage
import ssl
import smtplib


# Define a function to send emails
def send_email(sender, recipient, subject, message_body, email_password):
    """Sends an email message.

  Args:
    sender: The sender's email address.
    recipient: The recipient's email address.
    subject: The email subject.
    message_body: The email message body.
    email_password: The email password.

  Returns:
    True if the email was sent successfully, False otherwise.
  """
    # Create a new EmailMessage object
    email_message = EmailMessage()
    # Set the email headers
    email_message['From'] = sender
    email_message['To'] = recipient
    email_message['Subject'] = subject
    # Set the email body
    email_message.set_content(message_body)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Use SMTP_SSL to send the email securely
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        try:
            # Login to the email account using the email password
            smtp.login(sender, email_password)
            # Send the email
            smtp.send_message(email_message)
            # Return True if the email was sent successfully
            return True
        except Exception as e:
            # Print the error message and return False if the email could not be sent
            print(e)
            return False


def match_gift_pairs(group_id):
    # Get Group
    group = Group.query.get(group_id)
    # Get all users in the group
    users = [ug.user for ug in group.users]

    # Skip groups with less than 2 users
    if len(users) < 2:
        return

    # Shuffle the users within the group to randomize the gift exchange order
    random.shuffle(users)

    # Pair up users within the group
    for i, giver in enumerate(users):
        receiver = users[(i + 1) % len(users)]
        pair = Pair(giver=giver, receiver=receiver, group=group)
        db.session.add(pair)
        # Send an email containing the giver and receiver information
        message_body = f"You have been paired with {receiver.name}."
        subject = "Secret Santa Gift Exchange"
        sender_email = "umgcgiftpal@gmail.com"
        email_password = "<OUR PASSWORD>"
        send_email(sender_email, giver.email, subject,
                  message_body, email_password)


    # Commit the changes to the database
    db.session.commit()
