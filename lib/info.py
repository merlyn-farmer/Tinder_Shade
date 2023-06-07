import time

import requests, re, string, json, gspread, natsort, os
from selenium import webdriver
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def folder_checker(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            print(f"Ошибка при создании папки: {path}")
            time.sleep(5)
            return False

    return True

def df_to_gsheets(df, spreadsheet_name, worksheet_name):
    """Sending df to google sheets"""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('res/erudite-stratum-316309-a2d8c45cadb8.json', scope)
    gc = gspread.authorize(credentials)
    # Open the Google Sheet
    spreadsheet = gc.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    # Write the DataFrame to the Google Sheet
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def parse_session(file):
    """parsing session excel"""
    df = pd.read_excel(file, dtype=str)
    row = df.iloc[0]
    session_name, name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude, longitude = row

    parsed_df = df.iloc[1:]

    parsed_df.to_excel(file, index=False)
    return session_name, name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude, longitude


def send_cmd(driver, cmd, params={}):
    """Deprecated*, used to send command to browser"""
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')

def parse_line(file):
    """Deprecated*, used to parse first line of text file"""
    with open(file, "r", encoding="UTF-8") as f:
        list = f.readlines()
        line = list[0].strip()

    with open(file, "w", encoding="UTF-8") as f:
        new_list = list[1:]
        content = "".join(new_list)
        f.write(content)

    return line

def create_driver(session, port):
    """create driver"""
    mla_url = f'http://127.0.0.1:{port}/api/v1/profile/start?automation=true&profileId=' + session
    resp = requests.get(mla_url)
    json = resp.json()
    print(json)
    driver = webdriver.Remote(command_executor=json['value'])
    return driver


def update_profile_group(profile_id, group_id, port):
    """Update profile group"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "group": group_id
    }
    r = requests.post(url, json.dumps(data), headers=header)
    print(r.status_code)

def list_profiles(port):
    """list all profiles"""
    url = f"http://localhost:{port}/api/v2/profile"
    resp = requests.get(url)
    resp_json = json.loads(resp.content)
    return resp_json

def get_profile_group(session, port):
    """get profile group"""
    data = list_profiles(port)
    df = pd.DataFrame(data)
    locked = df.loc[df['uuid'] == session]
    group_id = locked["group"]
    print(group_id)
    return group_id

def get_profile_name(session, port):
    """get profile name"""
    data = list_profiles(port)
    df = pd.DataFrame(data)
    locked = df.loc[df['uuid'] == session]
    session_name = locked["name"]
    session_name = session_name.to_list()
    session_name = session_name[0]
    pattern = r'[' + string.punctuation + ']'
    session_name = re.sub(pattern, "", session_name)
    print(session_name)
    return session_name

def delete(session):
    url = 'http://localhost.multiloginapp.com:35000/api/v2/profile/' + session
    headers = {'accept': 'application/json'}

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print('Профиль успешно удален.')
    else:
        print('Ошибка при удалении профиля. Код ошибки:', response.status_code)
