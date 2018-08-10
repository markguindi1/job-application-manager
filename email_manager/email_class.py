import json


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