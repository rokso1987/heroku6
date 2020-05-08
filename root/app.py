import flask
import pickle
import os.path
from googleapiclient.discovery import build
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime


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
                    check = check_promocode_func(spreadsheet_id, promo, range_, user)
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

# Собираем страницу категории. Массив кнопок-категорий и словарь данных профиля ТОП3 экспертов.
# url = 'https://enigmatic-gorge-60919.herokuapp.com/buttons_experts_array'
# {"spreadsheet_id": "1RPn2loVmuXCAtr161HjdX3ZfRTIHzMuTK-SXqXD0UxE", "range": "Категории!2:10", "profile_range": "Лист1!c2:r", "pressed_button": "Категория 2"}
@app.route("/buttons_experts_array", methods=['POST', "GET"])
def buttons_experts_array():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            if 'pressed_button' in data:
                pressed_button = data.get('pressed_button')
                if 'profile_range' in data:
                    profile_range = data.get('profile_range')
                    otvet = get_button_experts_massiv(range_, profile_range, spreadsheet_id, pressed_button)
                    return otvet
                else:
                    otvet = json.dumps({"status": "0", "response": "profile_range was not transacted!"})
                    return otvet
            else:
                otvet = json.dumps({"status": "0", "response": "pressed_button was not transacted!"})
                return otvet
        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet
    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet

# Собираем страницу профиля эксперта. Массив с даными профиля. Входные данные:url = 'https://enigmatic-gorge-60919.herokuapp.com/expert_profile'  {"range": "Лист1!c:n", "name": "Фет Алексей", "spreadsheet_id": "1RPn2loVmuXCAtr161HjdX3ZfRTIHzMuTK-SXqXD0UxE"}
@app.route("/expert_profile", methods=['POST', "GET"])
def expert_profile():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            if 'name' in data:
                name = data.get('name')
                otvet = get_experts_profile(range_, name, spreadsheet_id)
                return otvet
            else:
                otvet = json.dumps({"status": "0", "response": "name was not transacted!"})
                return otvet
        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet
    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet

#получаем перечень событий для страницы профиля экспертов.
#Входные данные:url = 'https://enigmatic-gorge-60919.herokuapp.com/amount_of_experts'  {"range": "Лист1!i:i", "name": "Фет Алексей", "spreadsheet_id": "1RPn2loVmuXCAtr161HjdX3ZfRTIHzMuTK-SXqXD0UxE"}
@app.route("/expert_profile_sobytia", methods=['POST', "GET"])
def expert_profile_sobytia():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            if 'name' in data:
                name = data.get('name')
                otvet = get_experts_profile_sobytia(name, range_, spreadsheet_id)
                return otvet
            else:
                otvet = json.dumps({"status": "0", "response": "name was not transacted!"})
                return otvet
        else:
            otvet = json.dumps({"status": "0", "response": "range was not transacted!"})
            return otvet
    else:
        otvet = json.dumps({"status": "0", "response": "spreadsheet_id was not transacted!"})
        return otvet

# Считаем количество экспертов всего.
# Входные данные:url = 'https://enigmatic-gorge-60919.herokuapp.com/amount_of_experts'  {"range": "Лист1!i:i", "spreadsheet_id": "1RPn2loVmuXCAtr161HjdX3ZfRTIHzMuTK-SXqXD0UxE"}
@app.route("/amount_of_experts", methods=['POST', "GET"])
def amount_of_experts():
    if flask.request.method == 'GET':
        return 'The functions works well'
    data = flask.request.get_json(force=True)
    if 'spreadsheet_id' in data:
        spreadsheet_id = data.get('spreadsheet_id')
        if 'range' in data:
            range_ = data.get('range')
            otvet = get_amount_of_experts(range_, spreadsheet_id)
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
def read_array(spreadsheet_id, range_):
    service = google_registry()
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    return response

def check_promocode_func(spreadsheet_id, promo, range_, user):
    promolist = read_array(spreadsheet_id, range_)
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

# записываем, что код использован (пишем ник пользователя)
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
# Записываем данные в нужную таблицу.
def write_array_func(range_, spreadsheet_id, data_array):
    service = google_registry()
    value_range_body = {
        "values": [data_array]
    }
    value_Input_Option = "USER_ENTERED"
    request = service.spreadsheets().values().append(body=value_range_body, spreadsheetId=spreadsheet_id, range=range_,
                                                     valueInputOption=value_Input_Option).execute()
#Находим массив кнопок-категорий
def get_button_category_massiv(range_, spreadsheet_id):
    response = read_array(spreadsheet_id, range_)
    list_button_array = response.get('values')
    button_massiv = []
    for buttons in list_button_array:
        button_massiv.append(buttons[0])
    return button_massiv

# Находим список кнопок-экспертов, словарь данных профиля ТОП3 экспертов, статус для определения, что нажата кнопка.
def get_button_experts_massiv(range_, profile_range, spreadsheet_id, pressed_button):
    response = read_array(spreadsheet_id, range_)
    list_button_array = response.get('values')
    massiv = []
    status = "0"
    amount = "0"
    range_list = []
    for list in list_button_array:
        if list[0] == pressed_button:
            status = "1"
            amount = len(list) - 1
            for i in range(1, len(list)):
                massiv.append(list[i])
            for i in range(1, 4):
                range_list.append(list[i])
            break
#Ищем ТОП3 экспертов на соответсвующих страницах таблицы. Название страницы == list[i]
    array_expert_profile = {}
    kat_count = 1
    for expert in range_list:
        response = read_array(spreadsheet_id, profile_range)
        expert_values_array = response.get('values')
        count = 1
        for i in expert_values_array:
            array_profile = i
            if len(i) > 1:
                if i[0] == expert:
                    for l in array_profile:
                        array_expert_profile[f"{kat_count}{count}"] = l
                        count += 1
        kat_count += 1
    otvet = {"status": status, "massiv": massiv, "amount": amount, "experts_info": array_expert_profile}

    return otvet

# Получаем словарь с данными профиля эксперта для вывода на странице профиля
def get_experts_profile(range_, name, spreadsheet_id):
    response = read_array(spreadsheet_id, range_)
    expert_values_array = response.get('values')
    array_expert_profile = {}
    count = 1
    status = "0"
    for i in expert_values_array:
        if len(i) > 1:
            if i[0] == name:
                status = "1"
                # нужную строку с данными пакуем в словарь:
                for l in i:
                    array_expert_profile[count] = l
                    count += 1
    otvet = {"values": array_expert_profile, "status": status}
    return otvet

# Получаем строку мероприятий для показа в профиле эксперта
def get_experts_profile_sobytia(name, range_, spreadsheet_id):
    response = read_array(spreadsheet_id, range_)
    expert_values_array = response.get('values')
    future_list = ""
    last_list = ""
    now = datetime.now()
    for i in expert_values_array:
        if i[1] == name:
            if len(i) < 4:
                i.append('')
            day_sob, month_sob, year_sob = i[2].split('.')

            if now <= datetime(int(year_sob), int(month_sob), int(day_sob)):
                future_list = f"{future_list}{i[0]} - {i[2]} {i[3]}\n"
            else:
                last_list = f"{last_list}{i[0]} - {i[2]} {i[3]}\n"


    otvet = {"future_list": future_list, "last_list": last_list}
    return otvet

# Получаем количество экспертов всего.
def get_amount_of_experts(range_, spreadsheet_id):
    response = read_array(spreadsheet_id, range_)
    experts_array = response.get('values')
    amount_of_experts = experts_array.count(['Эксперт'])

    otvet ={"values": str(amount_of_experts)}
    return otvet



