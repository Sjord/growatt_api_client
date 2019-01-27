from enum import IntEnum
import datetime
import hashlib
import json
from typing import List, Dict

import requests


def hash_password(password):
    """
    Normal MD5, except add c if a byte of the digest is less than 10.
    """
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    for i in range(0, len(password_md5), 2):
        if password_md5[i] == '0':
            password_md5 = password_md5[0:i] + 'c' + password_md5[i + 1:]
    return password_md5


class Timespan(IntEnum):
    day = 1
    month = 2


class GrowattApi:
    server_url = 'https://server.growatt.com/'

    def __init__(self):
        self.session = requests.Session()

    def get_url(self, page):
        return self.server_url + page

    def login(self, username, password):
        password_md5 = hash_password(password)
        response = self.session.post(self.get_url('LoginAPI.do'), data={
            'userName': username,
            'password': password_md5
        })
        data = json.loads(response.content.decode('utf-8'))
        return data['back']

    def plant_list(self, user_id):
        response = self.session.get(self.get_url('PlantListAPI.do'),
                                    params={'userId': user_id},
                                    allow_redirects=False)
        if response.status_code != 200:
            raise RuntimeError("Request failed: %s", response)
        data = json.loads(response.content.decode('utf-8'))
        return data['back']

    def plant_detail(self, plant_id, timespan=Timespan.day, date=None):
        assert timespan in Timespan

        if not date:
            date = datetime.date.today()

        if timespan == Timespan.month:
            date_str = date.strftime('%Y-%m')
        else:
            date_str = date.strftime('%Y-%m-%d')

        response = self.session.get(self.get_url('PlantDetailAPI.do'), params={
            'plantId': plant_id,
            'type': timespan.value,
            'date': date_str
        })
        data = json.loads(response.content.decode('utf-8'))
        return data['back']


def extract_energy(plant_info_data: List[Dict[str, str]]) -> float:
    kwhs = [_['todayEnergy'] for _ in plant_info_data]
    energies = [float(_.split(' ')[0]) for _ in kwhs]
    return sum(energies)


def todays_energy_total(username: str, password: str):
    api = GrowattApi()
    login_res = api.login(username, password)
    user_id = login_res['userId']
    plant_info = api.plant_list(user_id)
    return extract_energy(plant_info['data'])
