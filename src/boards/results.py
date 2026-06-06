from PIL import Image, ImageFont, ImageDraw
from time import sleep
import debug
import nascar_api


class Results:
	"""
	Live running order board. Shows the top 10 cars with position, car number,
	and driver name, scrolling upward. The header row is color-coded by flag state.

	Data source: nascar_api.race (called fresh each render so the board always
	reflects the current lap/position, not a snapshot from startup).
	"""

	def __init__(self, data, matrix, sleepEvent):
		self.data = data
		self.matrix = matrix
		self.sleepEvent = sleepEvent
		self.sleepEvent.clear()

	def render(self):
		self.matrix.clear()

		if not self.data.race_is_live or not self.data.live_races:
			debug.info("Results board: no live race to display")
			self.sleepEvent.wait(5)
			return

		for race in self.data.live_races:
			series_id = race["series_id"]
			race_id   = race["race_id"]

			# Get header data: flag state, lap number, lap count, track name
			race_info = nascar_api.race.get_race_info(series_id, race_id)
			if not race_info:
				debug.error("Results: could not get race info for series {} race {}".format(series_id, race_id))
				continue

			# Get live running order: {position: {fName, lName, carNo, ...}}
			drivers = self.data.refresh_running_order(series_id, race_id)
			if not drivers:
				debug.error("Results: could not get running order for series {} race {}".format(series_id, race_id))
				continue

			row_pixels = 7
			im_height  = 10 * row_pixels  # room for top 10 cars
			i = row_pixels                 # start drawing below the header row

			# Draw the static header
			img_header = draw_header(self.data, race_info, row_pixels, self.matrix.width)
			self.matrix.draw_image((0, 0), img_header)

			# Draw the full running order image and show the first screenful
			image = draw_standing(self.data, drivers, im_height, self.matrix.width)
			self.matrix.draw_image((0, i), image)
			self.matrix.render()
			self.sleepEvent.wait(5)

			# Scroll the running order upward one pixel at a time
			while i > -(im_height - self.matrix.height) and not self.sleepEvent.is_set():
				i -= 1
				image = image.crop((0, 1, self.matrix.width, im_height))
				self.matrix.draw_image((0, row_pixels), image)
				self.matrix.render()
				self.sleepEvent.wait(0.2)

			self.sleepEvent.wait(5)


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_header(data, race_info, img_height, width):
	"""
	Draw the header bar showing flag color and lap info.

	race_info keys: flag_state, lap_number, laps_in_race, track_name, run_name
	"""
	layout     = data.config.layout
	flag_state = race_info.get("flag_state", 0)

	# Background and text color per flag state
	flag_colors = {
		1: ((0,   255, 0),   (0,   0,   0)),   # Green  — black text
		2: ((255, 255, 0),   (0,   0,   0)),   # Yellow — black text
		3: ((255, 0,   0),   (0,   0,   0)),   # Red    — black text
		4: ((0,   0,   0),   (255, 255, 255)), # Checkered — white text
		5: ((255, 255, 255), (0,   0,   0)),   # White  — black text
	}
	bg, fg = flag_colors.get(flag_state, ((0, 0, 255), (255, 255, 255)))  # default: blue

	image = Image.new('RGB', (width, img_height))
	draw  = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width - 1, img_height - 1), fill=bg)

	if flag_state in (0, 8, 9):
		# Pre-race: show track name instead of lap count
		text = race_info.get("track_name", "Pre-Race")
	else:
		text = "Lap {} of {}".format(
			race_info.get("lap_number", "?"),
			race_info.get("laps_in_race", "?")
		)

	draw.text((1, 0), text, fill=fg, font=layout.font)
	return image


def draw_standing(data, drivers, img_height, width):
	"""
	Draw the top-10 running order from the live_ticker drivers dict.

	drivers: {running_position (int): {fName, lName, carNo, status, ...}}
	Alternates row background color for readability.
	"""
	layout = data.config.layout
	image  = Image.new('RGB', (width, img_height))
	draw   = ImageDraw.Draw(image)

	row_height = 7
	row_pos    = 0

	for pos in sorted(drivers.keys()):
		if pos > 10:
			break

		driver = drivers[pos]
		car    = str(driver.get("carNo", ""))
		fname  = driver.get("fName", "")[:1]   # first initial only
		lname  = driver.get("lName", "")

		# Alternate odd/even row backgrounds
		bg_row = (0, 0, 0) if pos % 2 == 1 else (30, 30, 30)
		draw.rectangle([0, row_pos, width - 1, row_pos + row_height - 1], fill=bg_row)

		# Position number, car number, driver name
		draw.text((1,  row_pos), str(pos), fill=(255, 255, 255), font=layout.font)
		draw.text((9,  row_pos), car,      fill=(255, 255, 255), font=layout.font)
		draw.text((18, row_pos), fname,    fill=(255, 255, 255), font=layout.font)
		draw.text((23, row_pos), lname,    fill=(255, 255, 255), font=layout.font)

		row_pos += row_height

	return image
