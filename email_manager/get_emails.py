import imaplib
import datetime
import email
import json
import mailparser

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


class Email:
    def __init__(self, email_msg=None, id=""):
        self.email = email_msg
        self.id = id
        self.from_email = ""
        self.date = ""
        self.subject = ""
        self.content = ""

        # used for raw instance of EmailMessage
        # if isinstance(self.email, email.message.EmailMessage):
        #     self.from_email = email_msg['from']
        #     self.date = email_msg['date']
        #     self.subject = email_msg['subject']
        #     self.retrieve_body(self.email)

        if self.email is not None:
            self.from_email = ", ".join(self.email.from_[0])
            self.date = str(self.email.date)
            self.subject = self.email.subject
            self.content = self.email.body


    # used for raw instance of EmailMessage
    # def retrieve_body(self, payload):
    #     if payload.is_multipart():
    #         for part in payload.get_payload():
    #             self.retrieve_body(part)
    #     else:
    #         self.content += payload.get_payload() + "\n"
    #
    # def retrieve_plaintext(self):
    #     if self.email.is_multipart():
    #         for part in self.email.walk():
    #             ctype = part.get_content_type()
    #             cdispo = str(part.get('Content-Disposition'))
    #
    #             # skip any text/plain (txt) attachments
    #             if ctype == 'text/plain' and 'attachment' not in cdispo:
    #                 self.content = part.get_payload(decode=True)  # decode
    #                 break
    #     # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    #     else:
    #         self.content = self.email.get_payload(decode=True)


class EmailEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Email):
            return {
                "__Email__": True,
                "id": o.id,
                "from_email": o.from_email,
                "date": o.date,
                "subject": o.subject,
                "content": o.content
            }

        else:
            return super().default(o)


def email_decoder(dct):
    if "__Email__" in dct:
        msg = Email()
        msg.id = dct["id"]
        msg.from_email = dct["from_email"]
        msg.date = dct["date"]
        msg.subject = dct["subject"]
        msg.content = dct["content"]
        return msg
    return dct


# date format: %d-%b-%Y
# ex: 17-Jun-2018
def get_emails(gmail_email, pswd, since_date):
    
    emails_list = []

    try:
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

        # for the id of emails received since the specified date
        for i in range(latest_email_id, earlier_email_id, -1):

            # typ is some status code, like above. "OK" in this case.
            # data is a list of two objects:
            # 1. A tuple with bytes of the relevant data we want
            # 2. some irrelevant byte object
            typ, data = mail.fetch(str(i), '(RFC822)')

            # We only care about the data's tuple in the below loop
            for response_part in data:
                if isinstance(response_part, tuple):

                    # used for raw instance of EmailMessage
                    #msg = email.message_from_bytes(response_part[1])

                    # convenient wrapper for EmailMessage,
                    # which extracts body and all email parts properly
                    msg = mailparser.parse_from_bytes(response_part[1])

                    email_id = i

                    an_email = Email(msg, email_id)
                    emails_list.append(an_email)

    # If there are no emails (quick fix - to do proper fix later)
    except IndexError as e:
        pass

    return emails_list
