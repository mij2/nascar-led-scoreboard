import nascar_api.data
import nascar_api.object

"""
Return parsed data into dictionary variable for easy use with display boards
"""

def get_race_info(seriesID, raceID):
	"""
	return race flag, current lap, total laps, track name, and race name
	"""
	
	data = nascar_api.data.get_liveRace(seriesID, raceID)
	if not data:
		return data
	parsed = data.json()
	
	if parsed:
		output = {
			"race_id": parsed["race_id"],
			"flag_state": parsed["flag_state"],
			"lap_number": parsed["lap_number"],
			"laps_in_race": parsed["laps_in_race"],
			"track_name": parsed["track_name"],
			"run_name": parsed["run_name"]
		}
		return output
	else:
		return []

def live_ticker(seriesID, raceID):
	"""
	Return live running order for selected race
	"""
	
	data = nascar_api.data.get_liveRace(seriesID, raceID)
	if not data:
		return data
	parsed = data.json()
	
	if parsed["vehicles"]:
		driver_data = parsed["vehicles"]
		drivers = {}
		
		for driver in driver_data:
			running = driver["running_position"]
			fName = driver["driver"]["first_name"]
			lName = driver["driver"]["last_name"]
			lapsLed = driver["laps_led"]
			inPlayoffs = driver["driver"]["is_in_chase"]
			lapsCompleted = driver["laps_completed"]
			status = driver["status"]
			started = driver["starting_position"]
			onTrack = driver["is_on_track"]
			carNo = driver["vehicle_number"]
			
			output = {
				'fName': fName,
				'lName': lName,
				'lapsLed': lapsLed,
				'inPlayoffs': inPlayoffs,
				'lapsCompleted': lapsCompleted,
				'status': status,
				'started': started,
				'onTrack': onTrack,
				'carNo': carNo,
			}
			
			#save in dict
			drivers[running] = output
		return drivers
	else:
		return []
	
class info_Race(object):

	def __init__(self,data):
		# loop through data
		for x in data:
			try:
				setattr(self, x, int(data[x]))
			except ValueError:
				try:
					setattr(self,x, float(data[x]))
				except ValueError:
					setattr(self,x,str(data[x]))
			except TypeError:
				obj = nascar_api.object.Object(data[x])
				setattr(self,x,obj)
	
class live_Race(object):

	def __init__(self,data):
		# loop through data
		for x in data:
			try:
				setattr(self, x, int(data[x]))
			except ValueError:
				try:
					setattr(self,x, float(data[x]))
				except ValueError:
					setattr(self,x,str(data[x]))
			except TypeError:
				obj = nascar_api.object.Object(data[x])
				setattr(self,x,obj)