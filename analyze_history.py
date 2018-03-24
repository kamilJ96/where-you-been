import json
import datetime

with open('raw.json', 'r') as f:
    data = json.load(f)

new_file = open('parsed.json', 'w')
new_data = {}
new_data['locations'] = []

gym_lat = '-37873'
gym_lon = '144726'

for location in data['locations']:
    lon = str(location['longitudeE7'])[:6]
    lat = str(location['latitudeE7'])[:6]
    if lon == gym_lon and lat == gym_lat:
        time = datetime.datetime.fromtimestamp(int(location['timestampMs'])/1000.0)
        new_data['locations'].append({
            'timestamp': time.strftime("%Y-%m-%d %H:%M"),
            'longitude': location['longitudeE7'],
            'latitude' : location['latitudeE7']
            })

json.dump(new_data, new_file, indent=4)


