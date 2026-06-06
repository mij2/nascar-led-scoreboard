import json
import requests
#import debug

"""
Current known NASCAR API URLs:

  Live / race day:
    https://cf.nascar.com/cacher/live/current-results.json
    https://cf.nascar.com/cacher/live/live-feed.json
    https://cf.nascar.com/live/feeds/series_1/{race_id}/live_feed.json   ← primary live feed
    https://cf.nascar.com/live/feeds/series_1/{race_id}/live_points.json
    https://cf.nascar.com/live-ops/live-ops.json                         ← unknown purpose

  Schedule:
    https://cf.nascar.com/cacher/{year}/race_list_basic.json
    https://www.nascar.com/json/schedule/?season={year}

  Points / standings:
    https://cf.nascar.com/cacher/{year}/{series}/points-feed.json
    https://cf.nascar.com/cacher/{year}/1/final/1-owners-points.json     ← Cup owners points
    https://cf.nascar.com/cacher/{year}/2/final/2-owners-points.json     ← Xfinity owners points
    https://cf.nascar.com/cacher/{year}/3/final/3-owners-points.json     ← Truck owners points

  Drivers:
    https://cf.nascar.com/cacher/drivers.json                            ← Badge_Image = car number image

  Scanner audio (future use?):
    https://cf.nascar.com/config/audio/audio_mapping_1_3.json
    https://cf.nascar.com/config/audio/audio_mapping_2_3.json
    https://cf.nascar.com/config/audio/audio_mapping_3_3.json
"""

CAR_BASE_URL = "https://cf.nascar.com/"
CAR_LIVE_URL = CAR_BASE_URL + "live/feeds/series_{series}/{race}/live_feed.json"
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