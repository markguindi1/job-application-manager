import imaplib
import datetime
import email

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


class Email:
    def __init__(self, id, from_email, date, subject, content=None):
        self.id = id
        self.from_email = from_email
        self.date = date
        self.subject = subject
        self.content = content

# %d-%b-%Y
# date format: 17-Jun-2018
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
                    msg = email.message_from_bytes(response_part[1])

                    email_id = i
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_date = msg['date']
                    email_content = ""
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":  # ignore attachments/html
                            body = part.get_payload(decode=True).decode("utf-8")
                            email_content += body

                    an_email = Email(email_id, email_from, email_date, email_subject, email_content)
                    emails_list.append(an_email)

    # If there are no emails (quick fix - to do proper fix later)
    except IndexError as e:
        pass

    return emails_list



# Credit: https://gist.github.com/ktmud/cb5e3ca0222f86f5d0575caddbd25c03

# def extract_body(msg, depth=0):
#     """ Extract content body of an email messsage """
#     body = []
#     if msg.is_multipart():
#         main_content = None
#         # multi-part emails often have both
#         # a text/plain and a text/html part.
#         # Use the first `text/plain` part if there is one,
#         # otherwise take the first `text/*` part.
#         for part in msg.get_payload():
#             is_txt = part.get_content_type() == 'text/plain'
#             if not main_content or is_txt:
#                 main_content = extract_body(part)
#             if is_txt:
#                 break
#         if main_content:
#             body.extend(main_content)
#     elif msg.get_content_type().startswith("text/"):
#         # Get the messages
#         charset = msg.get_param('charset', 'utf-8').lower()
#         # update charset aliases
#         charset = email.charset.ALIASES.get(charset, charset)
#         msg.set_param('charset', charset)
#         try:
#             body.append(msg.get_content())
#         except AssertionError as e:
#             print('Parsing failed.    ')
#             print(e)
#         except LookupError:
#             # set all unknown encoding to utf-8
#             # then add a header to indicate this might be a spam
#             msg.set_param('charset', 'utf-8')
#             body.append('=== <UNKOWN ENCODING POSSIBLY SPAM> ===')
#             body.append(msg.get_content())
#     return body