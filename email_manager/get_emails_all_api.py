import google.oauth2.credentials
import googleapiclient.discovery
from .email_class import *
from application_manager.models import *


API_SERVICE_NAME = "gmail"
API_VERSION = "v1"

# date format: %Y/%m/%d
# ex: 2018/06/17
DATE_FORMAT = "%Y/%m/%d"


def get_emails_api(current_user, since_date):

    emails_list = []

    try:
        credentials_dict = get_credentials_dict_from_db(current_user)
        credentials = google.oauth2.credentials.Credentials(**credentials_dict)
        service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

        since_date_query = "after:" + since_date.strftime(DATE_FORMAT)
        api_result = service.users().messages().list(userId='me', q=since_date_query).execute()
        messages = api_result['messages']

        for message_dict in messages:
            message_id = message_dict['id']
            full_message_dict = service.users().messages().get(userId='me', id=message_id, format='full').execute()
            email_msg = Email(full_message_dict)
            emails_list.append(email_msg)

    except Exception as e:
        # print("Some error getting from API: ", e)
        pass

    return emails_list


def get_credentials_dict_from_db(current_user):
    credentials = CustomCredentialsModel.objects.filter(user=request.user)
    credentials_dict = {'token': credentials.token,
                        'refresh_token': credentials.refresh_token,
                        'token_uri': credentials.token_uri,
                        'client_id': credentials.client_id,
                        'client_secret': credentials.client_secret,
                        'scopes': credentials.scopes}
    return credentials_dict


def save_credentials_to_db(current_user, credentials):
    user_credentials = CustomCredentialsModel.objects.filter(user=current_user)
    if not user_credentials.exists():
        user_credentials = CustomCredentialsModel(user=current_user)
    user_credentials.token = credentials.token
    user_credentials.refresh_token = credentials.refresh_token
    user_credentials.token_uri = credentials.token_uri
    user_credentials.client_id = credentials.client_id
    user_credentials.client_secret = credentials.client_secret
    user_credentials.scopes = credentials.scopes

    user_credentials.save()




