import json
import requests
#import debug

"""
    TODO:
        Add functions to call single series overview (all the games of a single series) using the NHL record API. 
        https://records.nhl.com/site/api/playoff-series?cayenneExp=playoffSeriesLetter="A" and seasonId=20182019
"""
#NASCAR URLS

CAR_BASE_URL = "https://cf.nascar.com/"
CAR_LIVE_URL = CAR_BASE_URL + "live/feeds/{series}/{race}/live_feed.json"
CAR_SCHEDULE_URL = CAR_BASE_URL + "cacher/{year}/race_list_basic.json"
REQUEST_TIMEOUT = 5

#Add standings and other URLs later

TIMEOUT_TESTING = 0.001  # TO DELETE

#Get race schedules
def get_race_schedule(year):
	try:
		data = requests.get(CAR_SCHEDULE_URL.format(year=year), timeout=REQUEST_TIMEOUT)
		return data
	except requests.exceptions.RequestException as e:
		raise ValueError(e)

#NASCAR call data
#
#Get live race data
def get_liveRace(seriesID, raceID):
	try:
		data = requests.get(CAR_LIVE_URL.format(series = seriesID, race=raceID), timeout=REQUEST_TIMEOUT)
		return data
	except requests.exceptions.RequestException as e:
		raise ValueError(e)