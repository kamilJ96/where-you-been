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
end_time = 0
max_elapsed_time = 14400000

def conv_timestamp(time):
    new_time = datetime.datetime.fromtimestamp(time/1000.0)
    new_time = new_time.strftime('%Y-%m-%d %H:%M')
    return(new_time)

# check each data point and see if it matches the necessary coordinates
# if it does, consider that the end time
for location in data['locations']:
    lon = str(location['longitudeE7'])[:6]
    lat = str(location['latitudeE7'])[:6]
    if lon == gym_lon and lat == gym_lat:
        if not end_time:
            end_time = int(location['timestampMs'])
    elif end_time:
        start_time = int(prev_location['timestampMs'])
        if end_time - start_time > 0:
            new_data['locations'].append({
                'start_time': start_time,
                'end_time': end_time,
                'longitude': prev_location['longitudeE7'],
                'latitude' : prev_location['latitudeE7'],
                'start_date': conv_timestamp(start_time),
                'end_date': conv_timestamp(end_time)
                })
        end_time = 0

    prev_location = location

json.dump(new_data, new_file, indent=4)
new_file.close()
