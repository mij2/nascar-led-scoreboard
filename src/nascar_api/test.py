import info

# schedule = info.schedule_info(2023)

schedule = info.dictSchedule_info(2023)

###

# Test code to filter on Cup races only
"""
cup = []
for race in schedule:
    if race['series_id'] == 1:
        cup.append(race)

print(cup)
"""

###

# Test to print race id and race name for series 3
""" series3 = schedule['series_3']

for race in series3:
    print(str(race['race_id']) + " " + race['race_name']) """

## Print schedule for series_3 (trucks)
# print(schedule["series_3"])

###

for series in schedule:
    print(series)
    for key, val in schedule[series].items():
        #print(key," - ",val)
        print(key, " - ", val["race_id"], " - ", val["series_id"])

for series in schedule:
    print(series)
    for key, val in schedule[series].items():
        #print(key," - ",val)
        print(key, " - ", val["race_id"], " - ", val["series_id"])


#print(schedule)