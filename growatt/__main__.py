import sys
import datetime
from growatt import hash_password, GrowattApi, Timespan

username = sys.argv[1]
password = sys.argv[2]

with GrowattApi() as api:
    api.login(username, password)
    plant_info = api.plant_list()
    print(plant_info)

    plant_id = plant_info["data"][0]["plantId"]
    plant_detail = api.plant_detail(plant_id, Timespan.day, datetime.date.today())
    print(plant_detail)
