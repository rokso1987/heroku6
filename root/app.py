import flask
import pickle
import os.path
from googleapiclient.discovery import build
# import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = flask.Flask(__name__)
@app.route('/')
def index():
    return('It works')
@app.route("/read_and_broadcast", methods=['POST', "GET"])
def read_and_broadcast():
    if flask.request.method == 'GET':
        val_array = read_array("1RPn2loVmuXCAtr161HjdX3ZfRTIHzMuTK-SXqXD0UxE", "List1!d:d")
        return val_array


def read_array(spreadsheet_id, range_):
    # CLIENT_CONFIG = {"web":{
    #     "client_id":"358132512710-4lppp3cntiudt7e9u80hmvi0urs6unvb.apps.googleusercontent.com",
    #     "project_id":"quickstart-1584982273217",
    #     "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    #     "token_uri":"https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    #     "client_secret":"Jd5wZyebWL-E6BBfr43Glskk"}}
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # The file 4.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../4.pickle'):
        with open('../4.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # flow = google_auth_oauthlib.flow.Flow.from_client_config(
            #     client_config=CLIENT_CONFIG,
            #     scopes=SCOPES)
            # # flow = InstalledAppFlow.from_client_secrets_file(
            # #     'credentials.json', SCOPES)
            # # Indicate where the API server will redirect the user after the user completes
            # # the authorization flow. The redirect URI is required.
            # flow.redirect_uri = 'http://localhost:8000'
            #
            # # Generate URL for request to Google's OAuth 2.0 server.
            # # Use kwargs to set optional request parameters.
            # authorization_url, state = flow.authorization_url(
            #     # Enable offline access so that you can refresh an access token without
            #     # re-prompting the user for permission. Recommended for web server apps.
            #     access_type='offline',
            #     # Enable incremental authorization. Recommended as a best practice.
            #     include_granted_scopes='true')

        # Save the credentials for the next run
        with open('../4.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    values = response.get('values')

    if not values:
        return 'No data found.'
    else:
        otvet3 = {"content": values}
        return otvet3