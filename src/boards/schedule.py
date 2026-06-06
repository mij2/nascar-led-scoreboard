from PIL import Image, ImageFont,ImageDraw, ImageSequence
from rgbmatrix import graphics
from time import sleep

class Schedule:
	"""
	Display upcoming races with details
	"""
	
	def __init__(self,data,matrix,sleepEvent):
		self.series = ["NASCAR Cup Series","NASCAR Xfinity Series","NASCAR Truck Series"]
		self.data = data
		self.matrix = matrix
		self.sleepEvent = sleepEvent
		self.sleepEvent.clear()
	
	def render(self):
		self.matrix.clear()
		
		im_height = 4 * 7 # doing static math for initial version
		
		races = self.data.races_upcoming
		
		for race in races:
			image = draw_race_schedule(self.data, race, im_height, self.matrix.width)
			self.matrix.draw_image((0,0), image)
			self.matrix.render()
			self.sleepEvent.wait(5)

def draw_race_schedule(data, race, img_height, width):

	layout = data.config.layout
	bgClr = data.config.series_colors.color("{}.bg".format(race["series_id"]))
	txtClr = data.config.series_colors.color("{}.text".format(race["series_id"]))
		
	image = Image.new('RGB', (width,img_height))
	draw = ImageDraw.Draw(image)
	
	#simple draw schedule details
	row_pos = 0
	row_height = 7
	top = row_height - 1
	
	draw.rectangle((0,0,63,6), fill=(bgClr["r"],bgClr["g"],bgClr["b"]))
	draw.text((1,0), race["name"], font=layout.font, fill=(txtClr["r"],txtClr["g"],txtClr["b"]))
	draw.text((1,7), race["track"], font=layout.font, fill=(255,255,255))
	draw.text((1,14), race["starttime"].strftime("%b %d, %I:%M %p"), font=layout.font, fill=(255,255,255))
	draw.text((1,21), race["TV"], font=layout.font, fill=(255,255,255))
	
	return image