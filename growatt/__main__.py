import sys
import datetime
from . import hash_password, GrowattApi, Timespan

username = sys.argv[1]
password = sys.argv[2]

assert hash_password("banaan") == "31d674be46e1ba6b54388a671cc9accb"

api = GrowattApi()
login_res = api.login(username, password)
user_id = login_res["userId"]
plant_info = api.plant_list(user_id)
print(plant_info)

plant_id = plant_info["data"][0]["plantId"]
plant_detail = api.plant_detail(plant_id, Timespan.day, datetime.date.today())
print(plant_detail)
