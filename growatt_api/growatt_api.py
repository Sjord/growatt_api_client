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

    def _extract_energy(self, plant_info_data: List[Dict[str, str]], key: str) -> float:
        kwhs = [_[key] for _ in plant_info_data]
        energies = [float(_.split(' ')[0]) for _ in kwhs]
        return sum(energies)

    def _plant_info(self, username: str, password: str):
        login_res = self.login(username, password)
        user_id = login_res['userId']
        return self.plant_list(user_id)

    def todays_energy_total(self, username: str, password: str):
        plant_info = self._plant_info(username, password)
        return self._extract_energy(plant_info['data'], 'todayEnergy')

    def global_energy_total(self, username: str, password: str):
        plant_info = self._plant_info(username, password)
        return self._extract_energy(plant_info['data'], 'totalEnergy')
