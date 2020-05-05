import flask
import pickle
import os.path
from googleapiclient.discovery import build
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = flask.Flask(__name__)
@app.route('/')
def index():
    return('It works')
@app.route("/read_and_broadcast", methods=['POST', "GET"])
def read_and_broadcast():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            klients = read_array(spreadsheet_id, range_)
            otvet = json.dumps({"status": "1", "response": klients})
            return otvet

        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet

    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet


def read_array(spreadsheet_id, range_):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # The file 4.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('4.pickle'):
        with open('4.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('4.pickle', 'wb') as token:
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