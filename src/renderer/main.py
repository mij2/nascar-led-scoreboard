from PIL import Image
from time import sleep
from datetime import datetime
import debug
from boards.boards import Boards
from boards.clock import Clock
from renderer.scoreboard import ScoreboardRenderer
from utils import get_file
import random
import glob



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

		#while self.data.network_issues:
			#Clock(self.data, self.matrix, self.sleepEvent, duration=60)
			#self.data.refresh_data()

		while True:
			debug.info('Rendering...')

			#if self.status.is_offseason(self.data.date()):
			#if True:
				# Offseason (Show offseason related stuff)
				# debug.info("It's offseason")
				# self.__render_no_race()
				
			#Only for testing
			
			debug.info("It's offseason")
			self.__render_no_race()
				
			""" Remove comment after testing
			elif self.data.config.testScChampions:
				self.test_stanley_cup_champion(self.data.config.testScChampions)

			else:
				# Season.
				if not self.data.config.live_mode:
					debug.info("Live mode is off. Going through the boards")
					self.__render_no_race()
				elif self.data.is_pref_team_offday():
					debug.info("Your preferred series are Off today")
					self.__render_no_race()
				elif self.data.is_nhl_offday():
					debug.info("There are no NASCAR races today")
					self.__render_no_race()
				else:
					debug.info("Race Day Wooooo")
					self.__render_game_day()
					
			"""

			#self.data.refresh_data()

	# Render NASCAR Days
	def __render_raceday(self):
		debug.info("Showing Race")
		# Initialize the scoreboard. get the current status at startup
		self.data.refresh_overview()
		self.scoreboard = Scoreboard(self.data.overview, self.data)
		self.sleepEvent.clear()

		while not self.sleepEvent.is_set():

			if self.data._is_new_day():
				debug.log('This is a new day')
				return

			# Display the pushbutton board
			if self.data.pb_trigger:
				debug.info('PushButton triggered in game day loop....will display ' + self.data.config.pushbutton_state_triggered1 + ' board')
				if not self.data.screensaver:
					self.data.pb_trigger = False
				#Display the board from the config
				self.boards._pb_board(self.data, self.matrix, self.sleepEvent)

			# Display the Weather Alert board
			if self.data.wx_alert_interrupt:
				debug.info('Weather Alert triggered in game day loop....will display weather alert board')
				self.data.wx_alert_interrupt = False
				#Display the board from the config
				self.boards._wx_alert(self.data, self.matrix, self.sleepEvent)

			# Display the screensaver board
			if self.data.screensaver:
				if not self.data.pb_trigger:
					debug.info('Screensaver triggered in game day loop....')
					#self.data.wx_alert_interrupt = False
					#Display the board from the config
					self.boards._screensaver(self.data, self.matrix, self.sleepEvent)
				else:
					self.data.pb_trigger = False

			if self.status.is_live(self.data.overview.status):
				""" Live Race state """
				#blocks the screensaver from running if game is live
				self.data.screensaver_livegame = True
				debug.info("Race is Live")
				sbrenderer = ScoreboardRenderer(self.data, self.matrix, self.scoreboard)
				
				self.__render_live(sbrenderer)

				self.sleepEvent.wait(self.refresh_rate)

			elif self.status.is_final(self.data.overview.status):
				""" Post Race state """
				debug.info("Race End")
				sbrenderer = ScoreboardRenderer(self.data, self.matrix, self.scoreboard)
				self.__render_postrace(sbrenderer)

				self.sleepEvent.wait(self.refresh_rate)

			elif self.status.is_scheduled(self.data.overview.status):
				""" Pre-race state """
				debug.info("Race is Scheduled")
				sbrenderer = ScoreboardRenderer(self.data, self.matrix, self.scoreboard)
				self.__render_prerace(sbrenderer)
				#sleep(self.refresh_rate)
				self.sleepEvent.wait(self.refresh_rate)
				self.boards._scheduled(self.data, self.matrix,self.sleepEvent)

			elif self.status.is_irregular(self.data.overview.status):
				""" Irregular race state """
				debug.info("Race is irregular")
				sbrenderer = ScoreboardRenderer(self.data, self.matrix, self.scoreboard)
				self.__render_irregular(sbrenderer)
				#sleep(self.refresh_rate)
				self.sleepEvent.wait(self.refresh_rate)
				self.boards._scheduled(self.data, self.matrix,self.sleepEvent)

			self.data.refresh_data()
			self.data.refresh_overview()
			self.scoreboard = Scoreboard(self.data.overview, self.data)
			if self.data.network_issues:
				self.matrix.network_issue_indicator()

			if self.data.newUpdate and not self.data.config.clock_hide_indicators:
				self.matrix.update_indicator()		

	def __render_no_race(self):
		i = 0
		while True:
			debug.info('PING !!! Render off day')
			
			## uncomment after testing
			#if self.data._is_new_day():
			#	debug.info('This is a new day')
			#	return
			self.boards._no_race(self.data, self.matrix,self.sleepEvent)

			if i >= 1:
				debug.info("off day data refresh")
				#self.data.refresh_data()
				i = 0
			else:
				i += 1

	def __render_prerace(self, sbrenderer):
		debug.info("Showing Pre-Race")
		self.matrix.clear()
		sbrenderer.render()

	def __render_postrace(self, sbrenderer):
		debug.info("Showing Post-Race")
		self.matrix.clear()
		sbrenderer.render()

	def __render_live(self, sbrenderer):
		debug.info("Showing Main Event")
		self.matrix.clear()
		sbrenderer.render()
		self.alternate_data_counter += 1

	def __render_irregular(self, sbrenderer):
		debug.info("Showing Irregular")
		self.matrix.clear()
		sbrenderer.render()

	def _draw_event_animation(self, event, id=14, name="test"):
		preferred_team_only = self.data.config.goal_anim_pref_team_only
		# Get the list of gif's under the preferred and opposing directory
		ANIMATIONS = "assets/animations/{}".format(event)
		all_gifs = glob.glob("/general/*.gif".format(ANIMATIONS))
		preferred_gifs = glob.glob("/preferred/*.gif".format(ANIMATIONS))
		opposing_gifs = glob.glob("/opposing/*.gif".format(ANIMATIONS))

		if event == "goal":
			filename = "{}/goal_light_animation.gif".format(ANIMATIONS)
		elif event == "penalty":
			filename = "{}/penalty_animation.gif".format(ANIMATIONS)

		# Use alternate animations if there is any in the respective folder
		if all_gifs:
			# Set opposing team goal animation here
			filename = random.choice(all_gifs)
			debug.info("General animation is: " + filename)

		self.play_gif(filename)

	def play_gif(self, file):
		im = Image.open(get_file(file))

		# Set the frame index to 0
		frame_nub = 0
		# Set number of loop to 1 (if you want to play you animation more then once, change this variable)
		numloop = 1
		self.matrix.clear()

		# Go through the frames
		x = 0
		while x is not numloop:
			try:
				im.seek(frame_nub)
			except EOFError:
				x += 1
				if x == numloop:
					return
				frame_nub = 0
				im.seek(frame_nub)

			self.matrix.draw_image(("50%", 0), im, "center")
			self.matrix.render()

			frame_nub += 1
			self.sleepEvent.wait(0.1)

	## Program for End of Stage 1 & 2 display
	def draw_end_of_stage(self):
		color = self.matrix.graphics.Color(0, 255, 0)
		self.matrix.graphics.DrawLine(self.matrix.matrix, (self.matrix.width * .5) - 8, self.matrix.height - 2, (self.matrix.width * .5) + 8, self.matrix.height - 2, color)
		self.matrix.graphics.DrawLine(self.matrix.matrix, (self.matrix.width * .5) - 9, self.matrix.height - 1, (self.matrix.width * .5) + 9, self.matrix.height - 1, color)

	# NASCAR-TODO: add a test_race_mode() method here for dev testing
