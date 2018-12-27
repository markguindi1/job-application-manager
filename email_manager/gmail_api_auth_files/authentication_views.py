from django.urls import reverse
from django.shortcuts import redirect
from application_manager.models import *
from email_manager.get_emails_api import *

import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


# The name of the directory containing the clients secret file
CLIENT_SECRETS_DIR_NAME = "gmail_api_auth_files"
# The name of a file that contains the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE_NAME = "client_secret.json"

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, os.pardir)
client_secrets_dir = os.path.join(parent_dir, CLIENT_SECRETS_DIR_NAME)
client_secrets_file = os.path.join(current_dir, CLIENT_SECRETS_FILE_NAME)


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


# View that checks if Google authorization required


# View that redirects (or returns a redirect) to Google's authorization page
def authorize(request):

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes=SCOPES)

    flow.redirect_uri = 'http://localhost:8000/email/oauth2callback/'

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    user_state = CustomStateModel(user=request.user, state=state)
    user_state.save()

    # Store the state so the callback can verify the auth server response.
    print("New state should be:"+state)
    request.session['state'] = state
    print("Session state after set is:"+request.session['state'])
    request.session['next'] = request.get_full_path()
    print("Next:", request.session['next'])

    return redirect(authorization_url)


# View that handles return from Google authorization page, and redirects to correct page
# (saved in session)
# email/oauth2callback
def oauth2callback(request):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.

    # state = request.session['state']
    state = CustomStateModel.objects.get(user=request.user).state
    print("Session state after callback is:"+state)

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

    # Don't know why this is here. I think the guys at Google just copy-pasted from above.
    flow.redirect_uri = 'http://localhost:8000/oauth2callback/'

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.build_absolute_uri()
    print("Auth response:"+authorization_response)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    print("These are the credentials:\n", request.session['credentials'])

    print("Redirecting to after auth: ", request.session['next'])
    return redirect(reverse("email_manager:email_list"))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


# Func that gets credentials

# Func





