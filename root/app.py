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
@app.route("/check_promocode", methods=['POST', "GET"])
def read_and_broadcast():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            if 'promo' in data:
                promo = data.get('promo')
                if 'user' in data:
                    user = data.get('user')
                    service = google_registry()
                    promolist = read_array(service, spreadsheet_id, range_)
                    check, Row_list = check_promocode(service, spreadsheet_id, promolist, promo, range_, user)
                    otvet = json.dumps({"status": check, "Row_list": Row_list})
                    return otvet
                else:
                    otvet = json.dumps({"status": "0", "response": "user was not transacted!"})
                    return otvet
            else:
                otvet = json.dumps({"status": "0", "response": "promocode was not transacted!"})
                return otvet

        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet

    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet

def google_registry():
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
    return service
def read_array(service, spreadsheet_id, range_):
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    return response

def check_promocode(service, spreadsheet_id, promolist, promo, range_, user):
    values = promolist.get('values')
    otvet = ''
    row = 1
    Row_list = {}
    for code in values:

        if code[0] == promo:
            if len(code) >= 2:
                if code[1] == "":
                    otvet = 'True'
                    write_used(service, spreadsheet_id, row, range_, user)
                    for i in range(2, len(code)):
                        Row_list[i+1] = code[i]

                else:
                    otvet = 'Код использован!'
            else:
                otvet = 'True'
                write_used(service, spreadsheet_id, row, range_, user)
            break
        else:
            row += 1
            otvet = 'Код не найден!'
    return otvet, Row_list

def write_used(service, spreadsheet_id, row, range_, user):
    split_range = range_.split('!')
    list = split_range[0]
    range = f'{list}!b{row}:b{row}'
    value_range_body = {
        "values": [[user]]
    }
    value_Input_Option = "USER_ENTERED"

    request = service.spreadsheets().values().append(body=value_range_body, spreadsheetId=spreadsheet_id, range=range,
                                                     valueInputOption=value_Input_Option).execute()

