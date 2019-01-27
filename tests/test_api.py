import json

import requests_mock

from growatt_api import growatt_api as victim


def test_hash():
    assert victim.hash_password("banaan") == "31d674be46e1ba6b54388a671cc9accb"


def test_extract_single_energy():
    plant_info_data = [
        {'plantMoneyText': '137.9 ',
         'plantName': 'my plant',
         'plantId': '107658',
         'isHaveStorage': 'false',
         'todayEnergy': '0.6 kWh',
         'totalEnergy': '114.9 kWh',
         'currentPower': '142 W'}
    ]

    assert victim.GrowattApi()._extract_energy(plant_info_data, 'todayEnergy') == 0.6


def test_extract_multiple_energy():
    plant_info_data = [
        {'plantMoneyText': '137.9 ',
         'plantName': 'my plant',
         'plantId': '107658',
         'isHaveStorage': 'false',
         'todayEnergy': '0.6 kWh',
         'totalEnergy': '114.9 kWh',
         'currentPower': '142 W'},
        {'plantMoneyText': '137.9 ',
         'plantName': 'my plant',
         'plantId': '107658',
         'isHaveStorage': 'false',
         'todayEnergy': '0.6 kWh',
         'totalEnergy': '114.9 kWh',
         'currentPower': '142 W'}
    ]

    assert victim.GrowattApi()._extract_energy(plant_info_data, 'todayEnergy') == 1.2


def test_login():
    api = victim.GrowattApi()
    with requests_mock.mock() as m:
        m.post('https://server.growatt.com/LoginAPI.do',
               text=json.dumps({'back': {'userId': '1'}}))

        login_res = api.login('foo', 'bar')
        assert login_res == {'userId': '1'}


def test_plant_list():
    api = victim.GrowattApi()
    with requests_mock.mock() as m:
        m.get('https://server.growatt.com/PlantDetailAPI.do',
              text=json.dumps({'back': {'data': 'some-data'}}))

        login_res = api.plant_detail('1')
        assert login_res == {'data': 'some-data'}


def test_today_energy_total():
    with requests_mock.mock() as m:
        m.post('https://server.growatt.com/LoginAPI.do',
               text=json.dumps({'back': {'userId': '1'}}))

        dummy_plant_info = {'data': [{'plantMoneyText': '137.9 ',
                                      'plantName': 'my plant',
                                      'plantId': '107658',
                                      'isHaveStorage': 'false',
                                      'todayEnergy': '0.6 kWh',
                                      'totalEnergy': '114.9 kWh',
                                      'currentPower': '142 W'}],
                            'totalData': {'currentPowerSum': '142 W',
                                          'CO2Sum': '114.9 T',
                                          'isHaveStorage': 'false',
                                          'eTotalMoneyText': '137.9 ',
                                          'todayEnergySum': '0.6 kWh',
                                          'totalEnergySum': '114.9 kWh'},
                            'success': True}

        m.get('https://server.growatt.com/PlantListAPI.do?userId=1',
              text=json.dumps({'back': dummy_plant_info}))

        assert victim.GrowattApi().todays_energy_total('foo', 'bar') == 0.6
