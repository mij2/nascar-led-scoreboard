"""
	TODO: Recode this by sorting into separate classes instead of having everything in a
		single one.
"""

from datetime import datetime, timedelta, date
from time import sleep
import debug
from data.status import Status
from utils import get_lat_lng

import nascar_api

NETWORK_RETRY_SLEEP_TIME = 0.5


def get_upcoming_races(races, startDate, numDays):
	"""
	Standalone helper that filters a list of race dicts to only those
	falling within [startDate, startDate + numDays). Used to populate the
	upcoming races display board.

	Each race dict is expected to have a "starttime" key of type datetime.
	"""
	upcomingRaces = []
	for race in races:
		if (race["starttime"] > startDate and race["starttime"] < (startDate + timedelta(days=numDays))):
			upcomingRaces.append(race)
	return upcomingRaces


class Data:
	def __init__(self, config):
		"""
		Central data store for the scoreboard display system. Holds all state the
		renderer boards need: current date, NASCAR schedule, live race status,
		weather, and hardware flags (push-button, screensaver, network health).
		"""

		# lat/lng for weather and dimmer features — falls back to None if location is unset
		try:
			self.latlng, self.latlng_msg = get_lat_lng(config.location)
		except Exception:
			self.latlng = None
			self.latlng_msg = "Location unavailable"

		# Flag for if pushbutton has triggered (physical button on the Pi hardware)
		self.pb_trigger = False

		# "reboot" or "poweroff" — set when a pushbutton press should trigger a system action
		self.pb_state = None

		# Track which board is actively rendering and which was shown before it
		self.curr_board = None
		self.prev_board = None

		# NASCAR race state
		# race_is_live: True while a flagged (green/yellow/etc.) race is running
		# today_races:  list of race dicts scheduled for today
		# live_races:   list of race dicts currently under a live flag
		self.race_is_live = False
		self.today_races = []
		self.live_races = []

		# Date components — rebuilt into a date object via self.date()
		self.day = ""
		self.month = ""
		self.year = ""

		# Weather board state
		self.wx_updated = False
		self.wx_units = []
		self.wx_current = []
		self.wx_curr_wind = []
		self.wx_curr_precip = []

		# wx_alert_interrupt: when True the renderer cuts to the alert board immediately
		self.wx_alerts = []
		self.wx_alert_interrupt = False

		# Weather forecast state
		self.forecast_updated = False
		self.wx_forecast = []

		# Update checker
		self.newUpdate = False
		self.UpdateRepo = "mij2/nascar-led-scoreboard"

		# Screensaver state
		# screensaver_livegame: True if screensaver was interrupted by a live race starting
		self.screensaver = False
		self.screensaver_displayed = False
		self.screensaver_livegame = False

		# When True the main loop should call refresh_data() on its next tick
		self.needs_refresh = True

		# Set True on repeated API failures; boards can check this to show a "no signal" state
		self.network_issues = False

		# EC weather data handler (shared between weather, alerts, and forecast)
		self.ecData = None

		# Save the parsed config
		self.config = config

		# Live feed timestamp — format "YYYYMMDD_HHMMSS" (UTC). Used to detect new API data.
		self.time_stamp = "00000000_000000"

		# True when the live feed timestamp has changed since the last poll cycle
		self.new_data = True

		# Initialize the Status object (NASCAR flag-state helpers)
		self.get_status()

		# Parse today's date
		self.refresh_current_date()

		# Today's date as a date object
		self.today = self.date()

		# Fetch the full NASCAR schedule for the current year
		self.races = self.refresh_NASCAR_schedule()

		# Build upcoming races window (next 14 days) for the schedule board
		self.races_upcoming = get_upcoming_races(self.races, datetime.now(), 14)

		# Get today's races
		self.today_races = self.get_race_today(self.year, self.month, self.day)

		# Check if any of today's races are currently live
		self.race_is_live = self.is_live_race()

	# ---------------------------------------------------------------------------
	# Status
	# ---------------------------------------------------------------------------

	def get_status(self):
		"""Instantiate the NASCAR Status helper used throughout the renderer."""
		self.status = Status()

	# ---------------------------------------------------------------------------
	# Date helpers
	# ---------------------------------------------------------------------------

	def __parse_today(self):
		"""
		Returns (year, month, day) accounting for a configurable end-of-day boundary.
		Allows the scoreboard to keep showing the previous day's results past midnight
		until config.end_of_day has passed.
		"""
		today = datetime.today()
		noon = datetime.strptime("12:00", "%H:%M").replace(year=today.year, month=today.month, day=today.day)
		end_of_day = datetime.strptime(self.config.end_of_day, "%H:%M").replace(year=today.year, month=today.month, day=today.day)
		if noon < end_of_day < datetime.now() and datetime.now() > noon:
			today += timedelta(days=1)
		elif end_of_day > datetime.now():
			today -= timedelta(days=1)
		return today.year, today.month, today.day

	def date(self):
		"""Rebuild a date object from the stored year/month/day ints."""
		return datetime(self.year, self.month, self.day).date()

	def refresh_current_date(self):
		self.year, self.month, self.day = self.__parse_today()

	def _is_new_day(self):
		"""
		Called on each main loop tick to detect a date rollover.
		Triggers refresh_daily() and returns True when the date has changed.
		"""
		debug.info('Checking for new day')
		self.refresh_current_date()
		if self.today != self.date():
			debug.info('It is a new day, refreshing data')
			self.today = self.date()
			self.refresh_daily()
			return True
		debug.info('Not a new day')
		return False

	# ---------------------------------------------------------------------------
	# NASCAR data refresh helpers
	# ---------------------------------------------------------------------------

	def refresh_running_order(self, series, race):
		"""
		Fetches the live running order (car positions, laps, etc.) for a race
		currently under way. Retries up to 5 times on failure.

		series: series ID (1=Cup, 2=Xfinity, 3=Truck)
		race:   race ID for the live event
		"""
		attempts_remaining = 5
		while attempts_remaining > 0:
			try:
				live_results = nascar_api.race.live_ticker(series, race)
				self.network_issues = False
				return live_results
			except ValueError as error_message:
				self.network_issues = True
				debug.error("Failed to refresh running order. {} attempts remaining.".format(attempts_remaining))
				debug.error(error_message)
				attempts_remaining -= 1
				sleep(NETWORK_RETRY_SLEEP_TIME)

	def refresh_NASCAR_schedule(self):
		"""
		Fetches the full race schedule for self.year from the NASCAR API.
		Returns a dict keyed by series ID. Retries up to 5 times on failure.
		"""
		attempts_remaining = 5
		while attempts_remaining > 0:
			try:
				races = nascar_api.info.dictSchedule_info(self.year)
				self.network_issues = False
				return races
			except ValueError as error_message:
				self.network_issues = True
				debug.error("Failed to refresh NASCAR schedule. {} attempts remaining.".format(attempts_remaining))
				debug.error(error_message)
				attempts_remaining -= 1
				sleep(NETWORK_RETRY_SLEEP_TIME)
		return {}

	def get_race_today(self, year, month, day):
		"""
		Returns a list of races from self.races_upcoming whose starttime falls
		on the given calendar date.
		"""
		races = []
		for race in self.races_upcoming:
			if date(year, month, day) == race["starttime"].date():
				races.append(race)
		return races

	def is_live_race(self):
		"""
		Checks whether any of today's races are currently running under an active flag.
		Flag codes 1-5 = race is live. Updates self.live_races and triggers a
		running-order refresh for each active race.
		"""
		is_live = False
		self.live_races = []
		for race in self.today_races:
			race_info = nascar_api.race.get_race_info(race["series_id"], race["race_id"])
			if race_info and 0 < race_info.get("flag_state", 0) < 6:
				is_live = True
				self.live_races.append(race)
				self.refresh_running_order(race["series_id"], race["race_id"])
		return is_live

	def refresh_data(self):
		"""Sets needs_refresh = True so the next main loop tick will re-poll the API."""
		debug.info("Refreshing data")
		self.needs_refresh = True
		self.network_issues = False

	def refresh_daily(self):
		"""
		Called by _is_new_day() at each date rollover. Re-fetches the season schedule,
		rebuilds the upcoming window, and refreshes today's race list.
		"""
		debug.info('Refreshing daily data')
		self.races = self.refresh_NASCAR_schedule()
		self.races_upcoming = get_upcoming_races(self.races, datetime.now(), 14)
		self.today_races = self.get_race_today(self.year, self.month, self.day)
