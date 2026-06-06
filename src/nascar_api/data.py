import json
import requests
#import debug

"""
Current known NASCAR API URLs:

  Live configuration (NASCAR.com backend — always accessible):
    https://cf.nascar.com/live-ops/live-ops.json
      ← live_current_series{1|2|3}_race  = current race ID per series
      ← live_feed_url_series{1|2|3}      = live feed URL (populated during race week)
      ← red_flag_status_series{1|2|3}    = red flag state (populated during race)
      ← live_graphical_indicators_stage{1|2|3}indicatorColor = hex color per stage
           Stage 1: #4f821e (green), Stage 2: #1e73be (blue), Stage 3: #e20087 (magenta)
      ← live_graphical_indicators_rookieIndicatorColor = #cc4900 (orange)
      ← live_graphical_indicators_playoffsIndicatorColor = #000000 (black)
      ← live_points_feed_url_series{1|2|3} = live points feed URL

  Live / race day:
    https://cf.nascar.com/cacher/live/current-results.json
    https://cf.nascar.com/cacher/live/live-feed.json
    https://cf.nascar.com/live/feeds/series_{series}/{race_id}/live_feed.json   ← primary live feed
    https://cf.nascar.com/live/feeds/series_{series}/{race_id}/live_points.json
      ← array of driver standings: car_number, first_name, last_name, points,
        points_position, delta_leader, wins, top_5, top_10, is_in_chase,
        is_rookie, stage_1_points .. stage_3_points, stage_1_winner .. stage_3_winner

  Schedule:
    https://cf.nascar.com/cacher/{year}/race_list_basic.json
    https://www.nascar.com/json/schedule/?season={year}

  Race weekend (post-race / historical):
    https://cf.nascar.com/cacher/{year}/{series}/{race_id}/weekend-feed.json
      ← weekend_race[]: race results, finishing order, stage results, cautions,
                         lead changes, practice/qualifying schedule
      ← weekend_runs[]: practice + qualifying session lap times and rankings
    https://cf.nascar.com/cacher/{year}/{series}/{race_id}/lap-times.json
      ← laps[]: per-driver lap-by-lap LapTime (seconds), LapSpeed (mph), RunningPos

  Points / standings:
    https://cf.nascar.com/cacher/{year}/{series}/points-feed.json
    https://cf.nascar.com/cacher/{year}/1/final/1-owners-points.json     ← Cup owners points
    https://cf.nascar.com/cacher/{year}/2/final/2-owners-points.json     ← Xfinity owners points
    https://cf.nascar.com/cacher/{year}/3/final/3-owners-points.json     ← Truck owners points

  Drivers:
    https://cf.nascar.com/cacher/drivers.json
      ← Badge_Image = car number image URL (no color data in any driver endpoint)

  Scanner audio (future use?):
    https://cf.nascar.com/config/audio/audio_mapping_1_3.json
    https://cf.nascar.com/config/audio/audio_mapping_2_3.json
    https://cf.nascar.com/config/audio/audio_mapping_3_3.json

  403 / gated (require auth or only available during live race):
    /cacher/{year}/{series}/{race_id}/pit-stop-data.json
    /cacher/{year}/{series}/{race_id}/live-flag-data.json
    /cacher/{year}/{series}/{race_id}/stage-points.json
    /cacher/teams.json, /cacher/cars.json, /cacher/manufacturers.json
    /cacher/{year}/{series}/entry-list.json

  Color note:
    No NASCAR API endpoint provides driver/car/team RGB or hex colors.
    Stage indicator colors are available in live-ops.json (see above).
    Series colors must be maintained manually in config/colors/series.json.
"""

CAR_BASE_URL = "https://cf.nascar.com/"
CAR_LIVE_URL = CAR_BASE_URL + "live/feeds/series_{series}/{race}/live_feed.json"
CAR_LIVE_POINTS_URL = CAR_BASE_URL + "live/feeds/series_{series}/{race}/live_points.json"
CAR_LIVE_OPS_URL = CAR_BASE_URL + "live-ops/live-ops.json"
CAR_SCHEDULE_URL = CAR_BASE_URL + "cacher/{year}/race_list_basic.json"
CAR_WEEKEND_FEED_URL = CAR_BASE_URL + "cacher/{year}/{series}/{race}/weekend-feed.json"
CAR_LAP_TIMES_URL = CAR_BASE_URL + "cacher/{year}/{series}/{race}/lap-times.json"
CAR_POINTS_URL = CAR_BASE_URL + "cacher/{year}/{series}/points-feed.json"
CAR_OWNERS_POINTS_URL = CAR_BASE_URL + "cacher/{year}/{series}/final/{series}-owners-points.json"
REQUEST_TIMEOUT = 5

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