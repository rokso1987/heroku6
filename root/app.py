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
def check_promocode():
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
                    promolist = read_array(spreadsheet_id, range_)
                    check = check_promocode(spreadsheet_id, promolist, promo, range_, user)
                    otvet = json.dumps({"otvet": check})
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

@app.route("/write_array", methods=['POST', "GET"])
def write_array():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            if 'data_array' in data:
                data_array = data.get('data_array')
                write_array_func(range_, spreadsheet_id, data_array)
                otvet = json.dumps({"status": "OK"})
                return otvet
            else:
                otvet = json.dumps({"status": "0", "response": "data_array was not transacted!"})
                return otvet

        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet

    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet

@app.route("/buttons_category_array", methods=['POST', "GET"])
def buttons_category_array():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            button_massiv = get_button_category_massiv(range_, spreadsheet_id)
            otvet = json.dumps({"massiv": button_massiv})
            return otvet
        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet

    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet
#     otvet = json.dumps({"massiv":[
#     "Железногорск (Курская область)",
#     "Железногорск (Красноярский край)",
#     "Железногорск-Илимский"
# ]})
#     return otvet

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
def read_array(spreadsheet_id, range_):
    service = google_registry()
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    return response

def check_promocode(spreadsheet_id, promolist, promo, range_, user):
    values = promolist.get('values')
    status = ''
    row = 1
    row_list = {}
    for code in values:

        if code[0] == promo:
            if len(code) >= 2:
                if code[1] == "":
                    write_used(spreadsheet_id, row, range_, user)
                    for i in range(2, len(code)):
                        row_list[i+1] = code[i]
                    status = 'True'

                else:
                    status = 'Код использован!'
            else:
                status = 'True'
                write_used(spreadsheet_id, row, range_, user)
            break
        else:
            row += 1
            status = 'Код не найден!'
    otvet = {"status": status, "row_list": row_list, "row": str(row)}
    return otvet

def write_used(spreadsheet_id, row, range_, user):
    service = google_registry()
    split_range = range_.split('!')
    list = split_range[0]
    range = f'{list}!b{row}'
    value_range_body = {
        "values": [[user]]
    }
    value_Input_Option = "USER_ENTERED"

    request = service.spreadsheets().values().append(body=value_range_body, spreadsheetId=spreadsheet_id, range=range,
                                                     valueInputOption=value_Input_Option).execute()

def write_array_func(range_, spreadsheet_id, data_array):
    service = google_registry()
    value_range_body = {
        "values": [data_array]
    }
    value_Input_Option = "USER_ENTERED"
    request = service.spreadsheets().values().append(body=value_range_body, spreadsheetId=spreadsheet_id, range=range_,
                                                     valueInputOption=value_Input_Option).execute()

def get_button_category_massiv(range_, spreadsheet_id):
    response = read_array(spreadsheet_id, range_)
    list_button_array = response.get('values')
    button_massiv = []
    for buttons in list_button_array:
        button_massiv.append(buttons[0])
    return button_massiv