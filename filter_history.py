""" TO-DO:
            Work on consolidating multiple sessions on the same day into
            one, as slight variances in coordinates make it seem like I've
            left the gym even though I haven't yet.
"""
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
gym_lat = -37873
gym_lon = 144726
end_time = 0
max_elapsed_time = 10800000

def conv_timestamp(time):
    new_time = datetime.datetime.fromtimestamp(time/1000.0)
    new_time = new_time.strftime('%Y-%m-%d %H:%M')
    return(new_time)

def constr_long(lon):
    rounded_lon = float(lon[:3]) + round(float(lon[3:7])/10000, 3)
    new_lon = str(rounded_lon)[:3] + str(rounded_lon)[4:7]
    return(new_lon)

# check each data point and see if it matches the necessary coordinates
# if it does, consider that the end time
for location in data['locations']:
    if not end_time:
        timestamps = []

    lon = int(str(location['longitudeE7'])[:6])
    lat = int(str(location['latitudeE7'])[:6])

    if (gym_lat-1 <= lat <= gym_lat+1) and (gym_lon-1 <= lon <= gym_lon+1):
        if not end_time:
            end_time = int(location['timestampMs'])
        else:
            prev_location = location

    elif end_time:
        if end_time - int(location['timestampMs']) > max_elapsed_time:
            '''
            try:
                prev_location = timestamps[-1]
            except IndexError:
                continue
                '''
            start_time = int(prev_location['timestampMs'])
            
            new_data['locations'].append({
                'start_time': start_time,
                'start_date': conv_timestamp(start_time),
                'end_time': end_time,
                'end_date': conv_timestamp(end_time)
                })
            end_time = 0

json.dump(new_data, new_file, indent=4)
new_file.close()
