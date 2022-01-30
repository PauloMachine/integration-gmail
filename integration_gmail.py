import imaplib
import email
import time

from robot.api.deco import keyword

HOST = "imap.gmail.com"
USERNAME = "email"
PASSWORD = "senha"

@keyword(name="Checking Email Sending")
def checking_email_sending():
  return get_last_email()

def get_last_email():
  mail = imaplib.IMAP4_SSL(HOST)
  mail.login(USERNAME, PASSWORD)

  _, num_messages = mail.select("inbox")
  _, last_message = mail.fetch(num_messages[0], '(RFC822)')
  _, bytes_message = last_message[0]

  message = {}

  email_message = email.message_from_bytes(bytes_message)
  message['subject'] = email_message['subject']

  for part in email_message.walk():
    if part.get_content_type() == "text/plain":
      body = part.get_payload(decode=True)
      message['body'] = body.decode().replace("\r\n", "")

  return message
