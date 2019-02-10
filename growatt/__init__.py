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


class Timespan(IntEnum):
    day = 1
    month = 2


class GrowattApiError(RuntimeError):
    pass


class LoginError(GrowattApiError):
    pass


class GrowattApi:
    server_url = "https://server.growatt.com/"

    def __init__(self):
        self.session = requests.Session()

    def get_url(self, page):
        return self.server_url + page

    def login(self, username, password):
        """
        Log in to the Growatt server, or raise an exception if this fails.
        """
        password_md5 = hash_password(password)
        response = self.session.post(
            self.get_url("LoginAPI.do"),
            data={"userName": username, "password": password_md5},
        )
        try:
            return self._back_success_response(response)
        except GrowattApiError:
            raise LoginError

    def plant_list(self):
        """
        Retrieve all plants beloning to the current user.
        """
        response = self.session.get(
            self.get_url("PlantListAPI.do"),
            allow_redirects=False,
        )
        return self._back_success_response(response)

    def plant_detail(self, plant_id, timespan, date):
        assert timespan in Timespan
        if timespan == Timespan.day:
            date_str = date.strftime("%Y-%m-%d")
        elif timespan == Timespan.month:
            date_str = date.strftime("%Y-%m")

        response = self.session.get(
            self.get_url("PlantDetailAPI.do"),
            params={"plantId": plant_id, "type": timespan.value, "date": date_str},
        )
        return self._back_success_response(response)

    def _back_success_response(self, response):
        """
        Check and return the response, where we expect a "back" key with a
        "success" item.
        """
        if response.status_code != 200:
            raise GrowattApiError("Request failed: %s" % response)
        data = response.json()
        result = data["back"]
        if not "success" in result or not result["success"]:
            raise GrowattApiError()
        return result
