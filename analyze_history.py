# First task: Calculate avg duration for each weekday

import json
import math
import argparse
import datetime

def get_weekday(date):
    y,m,d = (int(x) for x in date.split('-'))
    return datetime.date(y,m,d).weekday()

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='input a file to analyze')
args = parser.parse_args()

duration_per_day = [[0, 0], [0, 0], [0, 0], [0, 0],
                    [0, 0], [0, 0], [0, 0]]
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
max_duration = [0, 0]

with open(args.f, 'r') as f:
    data = json.load(f)

# Count which day of week and sum up the duration into a list of lists
#       [[no. times gone, sum of duration],..]
# Also keep track of session with maximum duration
for sesh in data['locations']:
    weekday = get_weekday(sesh['start_date'][:10])
    duration = sesh['end_time'] - sesh['start_time']

    duration_per_day[weekday][0] += 1
    duration_per_day[weekday][1] += duration

    if duration > max_duration[0]:
        max_duration[0] = duration
        max_duration[1] = sesh

i = 0
for day in duration_per_day:
    try:
        print('{}: {} times, {} mins on average'.format(days[i], day[0],
                math.floor((day[1] / day[0]) / 60000)))
    except ZeroDivisionError:
        print('{}: 0 times, 0 mins on average'.format(days[i]))
    i += 1

print("\nlongest sesh: {} mins".format(math.floor(max_duration[0] / 60000)))

