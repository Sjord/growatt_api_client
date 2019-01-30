[![Build Status](https://travis-ci.org/timvancann/growatt_api_client.svg?branch=master)](https://travis-ci.org/timvancann/growatt_api_client)

## Growatt API client

This Python 3 script logs in to server.growatt.com and retrieves data on solar panels.

### Example

You can get your plant info with the following snippet:

```python
import datetime
from growat_api.growatt_api import GrowattApi, Timespan

username = ...
password = ...


api = GrowattApi()
login_res = api.login(username, password)
user_id = login_res['userId']
plant_info = api.plant_list(user_id)
print(plant_info)

plant_id = plant_info['data'][0]['plantId']
plant_detail = api.plant_detail(plant_id, Timespan.day, datetime.date.today())
print(plant_detail)
```

## Todays total energy

To get todays total energy across all plants in `kWh` you can use

```python
from growat_api.growatt_api import todays_energy_total
todays_energy_total(username='...', password='...')
```
