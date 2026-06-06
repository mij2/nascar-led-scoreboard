import debug

class Status:
	"""
	NASCAR race status based on flag state codes returned by the live feed API.

	Flag state codes:
		0  = Not yet started / pre-race
		1  = Green flag  (race running)
		2  = Yellow flag (caution)
		3  = Red flag
		4  = Checkered flag (leader has finished)
		5  = White flag (final lap)
		6  = Checkered + Yellow (finish under caution)
		8  = Warm-up / pace laps
		9  = Not live (pre-event, no active session)
	"""

	def __init__(self):
		pass

	def is_scheduled(self, flag_state):
		"""Race is on today's schedule but has not started (pre-race/warm-up)."""
		return flag_state == 0 or flag_state == 8 or flag_state == 9

	def is_live(self, flag_state):
		"""Race is actively running under any flag (green, yellow, red, white)."""
		return 1 <= flag_state <= 5

	def is_game_over(self, flag_state):
		"""Leader has taken the checkered flag but race may still be finishing."""
		return flag_state == 4

	def is_final(self, flag_state):
		"""Race is fully complete (checkered or checkered-yellow)."""
		return flag_state == 4 or flag_state == 6

	def is_irregular(self, flag_state):
		"""Red flag or other unusual stoppage."""
		return flag_state == 3
