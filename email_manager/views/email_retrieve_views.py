from django.shortcuts import redirect
from django.views.generic import *
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *
from ..get_emails_api import *
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


# The name of the directory containing the clients secret file
CLIENT_SECRETS_DIR_NAME = "gmail_api_auth_files"
# The name of a file that contains the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE_NAME = "client_secret.json"

current_dir = os.path.dirname(os.path.abspath(__file__))
print("Current dir:", current_dir)
parent_dir = os.path.join(current_dir, os.pardir)
print("Parent dir:", parent_dir)
client_secrets_dir = os.path.join(parent_dir, CLIENT_SECRETS_DIR_NAME)
print("File dir:", client_secrets_dir)
client_secrets_file = os.path.join(client_secrets_dir, CLIENT_SECRETS_FILE_NAME)
print("File dir:", client_secrets_file)

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


# Create your views here.


class GmailAuthRedirectView(LoginRequiredMixin, RedirectView):
    # url = "/"

    def authorize(self, request):

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

        # Setting redirect url to authorization url.
        self.url = authorization_url

        # Store the state so the callback can verify the auth server response.
        user_state = CustomStateModel(user=request.user, state=state)
        user_state.save()

        print("New state should be:" + state)
        request.session['state'] = state
        print("Session state after set is:" + request.session['state'])
        request.session['next'] = request.get_full_path()
        print("Next:", request.session['next'])

    def dispatch(self, request, *args, **kwargs):
        self.authorize(request)
        self.url = self.url.replace('%', '%%')
        return super(GmailAuthRedirectView, self).dispatch(request, *args, **kwargs)


class OAuth2CallbackRedirectView(LoginRequiredMixin, RedirectView):
    url = "/"

    def dispatch(self, request, *args, **kwargs):
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.

        print(request.user.is_authenticated)
        state = CustomStateModel.objects.get(user=request.user).state
        print("Session state after callback is:" + state)

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file, scopes=SCOPES, state=state)

        # Don't know why this is here. I think the guys at Google just copy-pasted from above.
        flow.redirect_uri = 'http://localhost:8000/oauth2callback/'

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.build_absolute_uri()
        print("Auth response:" + authorization_response)
        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        self.request.session['credentials'] = credentials
        # user_credens = CustomCredentialsModel()
        print("These are the credentials:\n", request.session['credentials'])

        print("Redirecting to after auth: ", request.session['next'])
        return super(OAuth2CallbackRedirectView, self).dispatch(request, *args, **kwargs)


class EmailsListView(LoginRequiredMixin, TemplateView):
    template_name = "email_manager/emails-list.html"

    def dispatch(self, request, *args, **kwargs):
        # If not authenticated, redirect to Gmail Auth Redirect View
        if 'credentials' not in self.request.session:
            return redirect(reverse('gmail_auth'))
        return super(EmailsListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            emails_json = self.request.session['emails']

            # Un-serialize JSON email list, back to Python list for use in template context
            emails_list = json.loads(emails_json, object_hook=email_decoder)
        except:
            emails_list = []
        context['emails'] = emails_list

        return context


class EmailContentView(LoginRequiredMixin, TemplateView):
    template_name = "email_manager/email-content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails_json = self.request.session['emails']
        #del self.request.session['emails']

        # Un-serialize JSON email list, back to Python list
        emails_list = json.loads(emails_json, object_hook=email_decoder)
        email_to_display_id = self.request.GET["email-id"]
        email_to_display = None
        for email in emails_list:
            if email.id == email_to_display_id:
                email_to_display = email

        context['email'] = email_to_display

        return context


