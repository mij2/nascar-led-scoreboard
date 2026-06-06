from time import sleep
from datetime import datetime
import debug
from boards.boards import Boards
from boards.clock import Clock



class MainRenderer:
	def __init__(self, matrix, data, sleepEvent):
		self.matrix = matrix
		self.data = data
		self.status = self.data.status
		self.refresh_rate = self.data.config.live_game_refresh_rate
		self.boards = Boards()
		self.sleepEvent = sleepEvent
#		self.sog_display_frequency = data.config.sog_display_frequency
		self.alternate_data_counter = 1
		

	def render(self):
		# used for testing
		self.data.network_issues = False
		
		debug.info('test message 1')
		
		if self.data.config.testing_mode:
			debug.info("Rendering in Testing Mode")
			while True:
				# TODO: wire up a specific NASCAR board or renderer for testing mode
				Clock(self.data, self.matrix, self.sleepEvent)
				sleep(1)
				debug.info("Testing Mode Refresh")

		if self.data.config.test_live_race:
			debug.info("Test Live Race Mode — injecting most recent past race")
			# Find the most recently completed race from the loaded schedule
			now = datetime.now()
			past_races = [r for r in self.data.races if r["starttime"] < now]
			if past_races:
				test_race = sorted(past_races, key=lambda r: r["starttime"])[-1]
				debug.info("Using race: {} (series {}, race {})".format(
					test_race.get("name", "?"), test_race["series_id"], test_race["race_id"]))
				self.data.race_is_live = True
				self.data.live_races = [test_race]
			else:
				debug.error("No past races found in schedule — cannot inject test race")
			while True:
				self.boards.results(self.data, self.matrix, self.sleepEvent)
				debug.info("Test Live Race Refresh")

		#while self.data.network_issues:
			#Clock(self.data, self.matrix, self.sleepEvent, duration=60)
			#self.data.refresh_data()

		while True:
			debug.info('Rendering...')
			self.data.race_is_live = self.data.is_live_race()

			if self.data.race_is_live:
				debug.info("Live race detected — rendering results board")
				self.__render_live_race()
			else:
				debug.info("No live race")
				self.__render_no_race()

	def __render_no_race(self):
		i = 0
		while True:
			debug.info('PING !!! Render off day')
			
			if self.data._is_new_day():
				debug.info('This is a new day')
				return
			self.boards._no_race(self.data, self.matrix,self.sleepEvent)

			if i >= 1:
				debug.info("off day data refresh")
				#self.data.refresh_data()
				i = 0
			else:
				i += 1
	
	def __render_live_race(self):
		while self.data.race_is_live:
			self.boards.results(self.data, self.matrix, self.sleepEvent)
			if self.data._is_new_day():
				return
			self.data.race_is_live = self.data.is_live_race()
