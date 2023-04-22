# Import necessary modules
from email.message import EmailMessage  # for creating email messages
from my_passwords import password  # to import email password
import ssl  # for creating secure socket layer connections
import smtplib  # for sending emails through SMTP
import datetime  # for working with dates
import sqlite3  # for working with SQLite databases


# Define a function to send emails
def send_email(sender, recipient, subject, message_body):
    """Sends an email message.

  Args:
    sender: The sender's email address.
    recipient: The recipient's email address.
    subject: The email subject.
    message_body: The email message body.

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


# Main program starts here
if __name__ == '__main__':
    # Email configuration
    email_sender = 'Admin@giftPal.com'  # Set the administrator's email as sender
    email_password = password  # Use the imported email password

    # Connect to the SQLite database
    conn = sqlite3.connect('giftpal.db')
    c = conn.cursor()

    # Set the current date
    today = datetime.date.today()

    # Query the database for birthdays
    c.execute("SELECT name, email, birthdate FROM birthdays")
    for row in c.fetchall():
        name, email, birth_date_str = row

        # Convert the birth date string to a date object
        birth_date = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        # If the birth date is today, send an email reminder
        if birth_date.month == today.month and birth_date.day == today.day:
            subject = f"Happy birthday, {name}!"  # Set the email subject
            body = f"Dear {name},\n\nHappy birthday!\n\nBest regards,\nWith Love from giftPal"  # Set the email body

            # Send the email and print a message indicating success or failure
            if send_email(email_sender, email, subject, body):
                print(f"Email sent successfully to {name} at {email}")
            else:
                print(f"Error sending email to {name} at {email}")

    # Close the database connection
    conn.close()
