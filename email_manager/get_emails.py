import smtplib
import imaplib
import datetime
import time
import email

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


class Email:
    def __init__(self, id, from_email, date, subject):
        self.id = id
        self.from_email = from_email
        self.date = date
        self.subject = subject

# %d-%b-%Y
# date format: 17-Jun-2018
def get_emails(gmail_email, pswd, since_date):

    emails_list = []
    DATE_FORMAT = "%d-%b-%Y"


    # 'mail' is the server
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)

    # login using email & pswd
    mail.login(gmail_email, pswd)

    # select only messages with 'inbox' tag
    mail.select('inbox')

    # 1st mandatory param is charset (None in this case), 2nd is search criteria
    # atype is a str with some 'status', in this case its value is "OK"
    # data is a list with only one element, a series of bytes
    # atype, data = mail.search(None, 'ALL')
    since_date = since_date.strftime(DATE_FORMAT)
    atype, data = mail.search(None, 'SINCE "{}"'.format(since_date))


    # mail_ids is a series of bytes
    mail_ids = data[0]

    # splits into ***strings*** using sep=(ASCII whitespace)
    id_list = mail_ids.split()

    earlier_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    # for the id of emazils received since the specified date
    for i in range(latest_email_id, earlier_email_id, -1):

        # typ is some status code, like above. "OK" in this case.
        # data is a list of two objects:
        # 1. A tuple with bytes of the relevant data we want
        # 2. some irrelevant byte object
        typ, data = mail.fetch(str(i), '(RFC822)')

        # We only care about the data's tuple in the below loop
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                email_id = i
                email_subject = msg['subject']
                email_from = msg['from']
                email_date = msg['date']
                an_email = Email(email_id, email_from, email_date, email_subject)
                emails_list.append(an_email)

    return emails_list
