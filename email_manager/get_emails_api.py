from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
from .email_class import *
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

# date format: %Y/%m/%d
# ex: 2018/06/17
DATE_FORMAT = "%Y/%m/%d"

def get_emails_api(email, since_date):

    emails_list = []
    token_filename = email + "_token.json"
    credentials_filename = email + "_credentials.json"

    try:

        store = oauth_file.Storage(token_filename)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_filename, SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        since_date_query = "after:" + since_date.strftime(DATE_FORMAT)
        api_result = service.users().messages().list(userId='me', q=since_date_query).execute()
        messages = api_result['messages']

        for message_dict in messages:
            email_msg = Email(message_dict)
            emails_list.append(email_msg)

    except:
        pass

    return emails_list