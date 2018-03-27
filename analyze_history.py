import json
import datetime
import argparse

# raw data is supplied through a json file from the command line
parser = argparse.ArgumentParser()
parser.add_argument('-f', help='file to parse')
args = parser.parse_args()

with open(args.f, 'r') as f:
    data = json.load(f)

new_file = open('parsed.json', 'w')
new_data = {}
new_data['locations'] = []

# coordinates you want to match in the data, add/subtract numbers to
# increase/decrease accuracy of wanted location
gym_lat = '-37873'
gym_lon = '144726'

# check each data point and see if it matches the necessary coordinates
# if it does, add it to a new json object, keeping only relevant information
for location in data['locations']:
    lon = str(location['longitudeE7'])[:6]
    lat = str(location['latitudeE7'])[:6]
    if lon == gym_lon and lat == gym_lat:
        new_data['locations'].append({
            'timestamp': int(location['timestampMs']),
            'longitude': location['longitudeE7'],
            'latitude' : location['latitudeE7']
            })

json.dump(new_data, new_file, indent=4)
new_file.close()
