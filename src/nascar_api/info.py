import nascar_api.data as data
import nascar_api.object as object
import datetime

def sort_schedule(races):
	## sort races by race start time
	sorted_races = sorted(races, key = lambda item: item["starttime"])
	
	return sorted_races

def dictSortSchedule(races,series):
	## sort races by race start time
	sorted_races = sorted(races.items(), key = lambda item: item[series]["starttime"])
	
	return sorted_races

def getSeries(series):
	switcher = {
		1: "CUP",
		2: "NXS",
		3: "CTS"
	}
	return switcher.get(series, "N/A")

def getSeriesKey(series):
	switcher = {
		"series_1": 1,
		"series_2": 2,
		"series_3": 3
	}
	return switcher.get(series, "N/A")

def dictSchedule_info(year):
	# Returns a year's schedule as a dictionary

	## Get data through local NASCAR_api
	json_data = data.get_race_schedule(year)
	parsed = json_data.json()

	# Start for trimming of JSON data
	schedule = {}
	keys = parsed.keys()

	for key in keys:
		# Get key from series string
		series_id = getSeriesKey(key)

		# print key for testing purposes
		print(key)

		# Declare nested dict and counter variable
		schedule[series_id] = {}
		i = 0

		# add races to series in py dict
		for race in parsed[key]:

			#print(race)

			#print(str(series_id) + " - " + str(race['series_id']) + " - " + race['race_name'])

			schedule[series_id][i] = {}
			schedule[series_id][i] = {
				"series_id": series_id,
				"race_id": race['race_id'],
				"starttime": datetime.datetime.strptime(race['race_date'],"%Y-%m-%dT%H:%M:%S"),
				"name": race['race_name'],
				"total_laps": race['scheduled_laps'],
				"track": race['track_name'],
				"TV": race['television_broadcaster'],
				"qual_race": race['is_qualifying_race']
			}				
			i += 1
	return schedule

def schedule_info(year):
	"""
	Returns schedules for each series as a list of individual dictionaries
	"""
	x=1
	
	## Get data through local NASCAR_api
	json_data = data.get_race_schedule(year)
	parsed = json_data.json()
	races = []
	
	## pull data from all three national series
	while (x < 4):
		series = "series_{}".format(x)
		for race in parsed[series]:
			## Save line below for future formatting of start time
			# starttime = datetime.datetime.strptime(race["race_date"],"%Y-%m-%dT%H:%M:%S").strftime("%b %d, %I:%M %p")
			
			# set dict values to be stored in races list
			output = {
				"series_id": series[-1:],
				"race_id": race["race_id"],
				"starttime": datetime.datetime.strptime(race["race_date"],"%Y-%m-%dT%H:%M:%S"),
				"name": race["race_name"],
				"total_laps": race["scheduled_laps"],
				"track": race["track_name"],
				"TV": race["television_broadcaster"],
				"qual_race": race["is_qualifying_race"]
			}
			
			races.append(output)
		
		x += 1
	
	# Call race sort function and return races list/dict
	races = sort_schedule(races)
	
	return races