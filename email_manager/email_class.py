import json
import mailparser
import datetime
import base64
import email


class Email:
    def __init__(self, email_msg=None, id=""):
        self.email = email_msg
        self.id = id
        self.from_email = ""
        self.date = ""
        self.subject = ""
        self.content = ""
        self.snippet = ""

        if self.email is None:
            return

        if isinstance(self.email, mailparser.mailparser.MailParser):
            self.from_email = ", ".join(self.email.from_[0])
            self.date = str(self.email.date)
            self.subject = self.email.subject
            self.content = self.email.body
            self.snippet = self.content[:50]

        # If email retrieved from Gmail API
        if isinstance(self.email, dict):
            self.id = self.get_id_api_email()
            self.from_email = self.get_from_email_api_email()
            self.date = self.get_date_api_email()
            self.subject = self.get_subject_api_email()
            self.content = self.get_content_api_email()
            self.snippet = self.get_snippet_api_email()

        self.content = self.content.replace("\\n", "").replace("\\r", "")

    def get_from_email_api_email(self):
        return self.get_attribute_from_headers("From")

    def get_id_api_email(self):
        #print(self.email['id'])
        return self.email['id']

    def get_date_api_email(self):
        epoch_timestamp = int(self.email['internalDate']) // 1000
        return datetime.datetime.fromtimestamp(epoch_timestamp).strftime("%a, %b %w, %Y, %I:%M:%S %p")

    def get_subject_api_email(self):
        return self.get_attribute_from_headers("Subject")

    def get_content_api_email(self):
        # Possible guide for decoding emails:
        # https://github.com/abhishekchhibber/Gmail-Api-through-Python/blob/master/gmail_read.py

        body = ""
        if 'data' in self.email['payload']['body']:
            body_data = self.email['payload']['body']['data']
            mssg_body = str(base64.urlsafe_b64decode(body_data.encode("ASCII")))
            body += mssg_body

        # "Parts" is a list of dictionary, each dictionary being another message part
        if 'parts' in self.email['payload']:
            payload_parts = self.email['payload']['parts']
            for part in payload_parts:
                if 'data' in part['body']:
                    part_body_data = part['body']['data']
                    mssg_body = str(base64.urlsafe_b64decode(part_body_data.encode("ASCII")))
                    body += mssg_body

        return body

    def get_snippet_api_email(self):
        return self.email['snippet']

    def get_attribute_from_headers(self, attribute):
        headers = self.email['payload']['headers']
        value = ""
        for header_dict in headers:
            if header_dict['name'].lower() == attribute.lower():
                value = header_dict['value']
                break
        return value
    

class EmailEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Email):
            return {
                "__Email__": True,
                "id": o.id,
                "from_email": o.from_email,
                "date": o.date,
                "subject": o.subject,
                "content": o.content,
                "snippet": o.snippet,
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
        msg.snippet = dct["snippet"]
        return msg
    return dct