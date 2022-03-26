from enum import IntEnum
import hashlib
import requests


def hash_password(password):
    """
    Normal MD5, except add c if a byte of the digest is less than 10.
    """
    password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()
    for i in range(0, len(password_md5), 2):
        if password_md5[i] == "0":
            password_md5 = password_md5[0:i] + "c" + password_md5[i + 1 :]
    return password_md5


def _back_success_response(response):
    """
    Check and return the response, where we expect a "back" key with a
    "success" item.
    """
    if response.status_code != 200:
        raise GrowattApiError("Request failed: %s" % response)
    data = response.json()
    result = data["back"]
    if not "success" in result or not result["success"]:
        raise GrowattApiError(result)
    return result

def _obj_success_response(response):
    if response.status_code != 200:
        raise GrowattApiError("Request failed: %s" % response)
    data = response.json()
    if data["result"] != 1 or "obj" not in data:
        raise GrowattApiError(data)
    return data["obj"]


class Timespan(IntEnum):
    day = 1
    month = 2
    year = 3
    total = 4

    def format_date(self, date):
        if self == Timespan.day:
            return date.strftime("%Y-%m-%d")
        elif self == Timespan.month:
            return date.strftime("%Y-%m")
        elif self == Timespan.year:
            return date.strftime("%Y")
        elif self == Timespan.total:
            return ""
        else:
            raise ValueError(self)


class GrowattApiError(RuntimeError):
    pass


class LoginError(GrowattApiError):
    pass


class GrowattApi:
    server_url = "https://server-api.growatt.com/" #"https://server.growatt.com/"
    print(server_url)
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.logged_in:
            self.logout()

    def get_url(self, page):
        return self.server_url + page

    def login(self, username, password):
        """
        Log in to the Growatt server, or raise an exception if this fails.
        """
        password_md5 = hash_password(password)
        response = self.session.post(
            self.get_url("newLoginAPI.do"),
            data={"userName": username, "password": password_md5},
        )
        try:
            result = _back_success_response(response)
            self.logged_in = True
            result["userId"] = result["user"]["id"]
            return result
        except GrowattApiError:
            raise LoginError

    def plant_list(self):
        """
        Retrieve all plants beloning to the current user.
        """
        response = self.session.get(
            self.get_url("PlantListAPI.do"), allow_redirects=False
        )
        return _back_success_response(response)

    def plant_detail(self, plant_id, timespan, date):
        """
        Return amount of power generated for the given timespan.
        * Timespan.day : power on each half hour of the day.
        * Timespan.month : power on each day of the month.
        * Timespan.year: power on each month of the year.
        * Timespan.total: power on each year. `date` parameter is ignored.
        """
        assert timespan in Timespan
        date_str = timespan.format_date(date)

        response = self.session.get(
            self.get_url("PlantDetailAPI.do"),
            params={"plantId": plant_id, "type": timespan.value, "date": date_str},
        )
        return _back_success_response(response)

    def new_plant_detail(self, plant_id, timespan, date):
        """
        Return amount of power generated for the given timespan.
        * Timespan.day : power on each five minutes of the day.
        * Timespan.month : power on each day of the month.
        * Timespan.year: power on each month of the year.
        * Timespan.total: power on each year. `date` parameter is ignored.
        """
        assert timespan in Timespan
        date_str = timespan.format_date(date)

        response = self.session.get(
            self.get_url("newPlantDetailAPI.do"),
            params={"plantId": plant_id, "type": timespan.value, "date": date_str},
        )
        return _back_success_response(response)

    def get_user_center_energy_data(self):
        """
        Get overall data including:
        * powerValue - current power in Watt
        * todayValue - power generated today
        """
        response = self.session.post(
            self.get_url("newPlantAPI.do"),
            params={"action": "getUserCenterEnertyData"},  # sic
            data={"language": 1},
        )
        return response.json()

    def get_all_device_list(self, plant_id):
        """
        Get information on each device/inverter.
        """
        response = self.session.post(
            self.get_url("newTwoPlantAPI.do"),
            params={
                "op": "getAllDeviceList",
                "plantId": plant_id
            }
        )
        return response.json()

    def logout(self):
        self.session.get(self.get_url("logout.do"))
        self.logged_in = False

    def storage(self, plant_id, device_sn):
        return Storage(self, plant_id, device_sn)

    def spa(self, plant_id, device_sn):
        return Spa(self, plant_id, device_sn)

    def mix(self, plant_id, device_sn):
        return Mix(self, plant_id, device_sn)


class Storage:
    def __init__(self, api, plant_id, device_sn):
        self.plant_id = plant_id
        self.device_sn = device_sn
        self.api = api
        self.session = api.session

    def get_url(self, page):
        return self.api.get_url(page)

    def get_energy_prod_and_cons_data(self, date, type=0):
        response = self.session.post(
            self.get_url("newStorageAPI.do"),
            params={"op": "getEnergyProdAndConsData"},
            data={
                "plantId": self.plant_id,
                "storageSn": self.device_sn,
                "date": date,
                "type": type,
            }
        )
        return _obj_success_response(response)

    def get_storage_energy_data(self, date):
        response = self.session.post(
            self.get_url("newStorageAPI.do"),
            params={"op": "getStorageEnergyData"},
            data={
                "plantId": self.plant_id,
                "storageSn": self.device_sn,
                "date": date,
            }
        )
        return _obj_success_response(response)

    def get_system_status_data(self):
        response = self.session.post(
            self.get_url("newStorageAPI.do"),
            params={"op": "getSystemStatusData"},
            data={
                "plantId": self.plant_id,
                "storageSn": self.device_sn,
            }
        )
        return _obj_success_response(response)

    def get_energy_overview_data(self):
        response = self.session.post(
            self.get_url("newStorageAPI.do"),
            params={"op": "getEnergyOverviewData"},
            data={
                "plantId": self.plant_id,
                "storageSn": self.device_sn,
            }
        )
        return _obj_success_response(response)

    def get_storage_params(self):
        response = self.session.get(
            self.get_url("newStorageAPI.do"),
            params={
                "op": "getStorageParams",
                "storageId": self.device_sn,
            }
        )
        return response.json()["storageDetailBean"]


class Spa:
    def __init__(self, api, plant_id, device_sn):
        self.plant_id = plant_id
        self.device_sn = device_sn
        self.api = api
        self.session = api.session

    def get_url(self, page):
        return self.api.get_url(page)

    def get_system_status(self):
        response = self.session.post(
            self.get_url("newSpaApi.do"),
            params={
                "op": "getSystemStatus",
            },
            data={
                "plantId": self.plant_id,
                "spaId": self.device_sn,
            }
        )
        return _obj_success_response(response)

    def get_spa_energy(self, date):
        response = self.session.post(
            self.get_url("newSpaApi.do"),
            params={
                "op": "getSpaEnergy",
            },
            data={
                "plantId": self.plant_id,
                "spaId": self.device_sn,
                "date": date,
            }
        )
        return _obj_success_response(response)

    def get_energy_overview(self):
        response = self.session.post(
            self.get_url("newSpaApi.do"),
            params={
                "op": "getEnergyOverview",
            },
            data={
                "plantId": self.plant_id,
                "spaId": self.device_sn,
            }
        )
        return _obj_success_response(response)

    def get_energy_prod_and_cons_data(self, date, timespan):
        assert timespan in Timespan
        date_str = timespan.format_date(date)

        response = self.session.post(
            self.get_url("newSpaApi.do"),
            params={
                "op": "getEnergyProdAndConsData",
            },
            data={
                "plantId": self.plant_id,
                "spaId": self.device_sn,
                "date": date_str,
                "type": timespan.value - 1
            }
        )
        return _obj_success_response(response)


class Mix:
    def __init__(self, api, plant_id, device_sn):
        self.plant_id = plant_id
        self.device_sn = device_sn
        self.api = api
        self.session = api.session

    def get_url(self, page):
        return self.api.get_url(page)

    def get_system_status(self):
        response = self.session.post(
            self.get_url("newMixApi.do"),
            params={
                "op": "getSystemStatus",
            },
            data={
                "plantId": self.plant_id,
                "mixId": self.device_sn,
            },
        )
        return _obj_success_response(response)

    def get_mix_energy(self, date):
        response = self.session.post(
            self.get_url("newMixApi.do"),
            params={
                "op": "getMixEnergy",
            },
            data={
                "plantId": self.plant_id,
                "mixId": self.device_sn,
                "date": date,
            },
        )
        return _obj_success_response(response)

    def get_energy_overview(self):
        response = self.session.post(
            self.get_url("newMixApi.do"),
            params={
                "op": "getEnergyOverview",
            },
            data={
                "plantId": self.plant_id,
                "mixId": self.device_sn,
            },
        )
        return _obj_success_response(response)

    def get_energy_prod_and_cons(self, date, timespan):
        assert timespan in Timespan
        date_str = timespan.format_date(date)

        response = self.session.post(
            self.get_url("newMixApi.do"),
            params={
                "op": "getEnergyProdAndCons",
            },
            data={
                "plantId": self.plant_id,
                "mixId": self.device_sn,
                "date": date_str,
                "type": timespan.value - 1,
            },
        )
        return _obj_success_response(response)
