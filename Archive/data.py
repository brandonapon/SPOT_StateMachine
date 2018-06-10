import math
import pickle
import time

class Point:
	'''
	TAG: only one tag
	LOCATION: tuple GPS location
	CREATED_BY: who created it
	TYPE: interest vs. danger
	PICTURE: needs to be saved in byte chunks. .txt file string
	'''
	def __init__(self, name):
		self.name = name
		self.key = ''
		self.tag = ''
		self.createdBy = ''
		self.type = ''
		self.picture = ''
		self.isVisible = False
		self.ack = False
		self.distance = ''
		self.gpsLocation = (0,0) # gps location (from actual GPS, static)
		self.currentLocation = (0,0) # current location of the point relative to user
		self.markedLocation = (0,0) # visible marked location

	# '''
	# Saves picture from DDR (be it from Transceiver or Camera)
	# CPICKLE
	# '''
	# def savePicture(self, array):
	#     fileObject = open("picture_{}.txt".format(self.name), "w")
	#     fileObject.write(array)
	#     fileObject.close()
	#     # INCOMPLETE

	# '''
	# Calculates distance based on USER location and the POI
	# param user_loc: GPS coordinates of the astronaut's location
	# '''
	# def calculateDistance(self, user_loc):

	def updateMarkedLoc(self):
		self.markedLocation = self.currentLocation

'''
Maps GPS location to Radar location
Note: 7 pixels PER meter. <1 meter = non update
'''
class Radar:
	"""
	(266, 240) is center location
	"""
	device = None

	def __init__(self, device):
		self.points = {} # dictionary of ALL POINTS
		self.visible = [] # list of KEYS of points that are visible
		self.redraw = [] # list of KEYS of points to be redrawn
		self.userLocation = (0,0) # GPS location of USER
		self.userLocationCartesian = (0,0)
		self.device = device
		# tags[0:3] = danger, tags[4:7] = interest
		self.tags = ['None', 'Crater', 'Gas', 'Obstacle', 'None', 'Rock', 'Sample', 'Liquid']

	'''
	Add point to dictionary of all POINTS
	'''
	def addPoint(self, point):
		self.points[len(self.points)] = point

	'''
	id = string
	tag = string
	createdBy = string
	gpsLoc = tuple
	objectType = string
	'''
	def createPoint(self, id, tag, createdBy, gpsLoc, objectType, cameraList):
		newPoint = Point(str(id))
		newPoint.tag = tag
		newPoint.createdBy = createdBy
		newPoint.gpsLocation = gpsLoc
		newPoint.type = objectType
		newPoint.picture = str(id)
		with open('{}.pkl'.format(id), 'wb') as file:
			pickle.dump(cameraList, file)
		self.addPoint(newPoint)

	'''
	Saves picture from DDR using pickle
	saves in RGB332 format
	'''
	def savePicture(self, ddr, pictureName):
		pictureList = []
		for index in range(76800):
			pictureList.append(ddr[index])
		with open('{}.pkl'.format(pictureName), 'wb') as file:
			pickle.dump(pictureList, file)
		return pictureList

	'''
	opens saved picture
	'''
	def openPicture(self, ddr, pictureName):
		imageList = []
		with open('{}.pkl'.format(pictureName), 'rb') as file:
		 	imageList = pickle.load(file)
		for index, val in enumerate(imageList):
			# ddr[index] = bytes([val])
			ddr[index] = val
		return imageList

	'''
	Converts meters to pixels.
	'''
	def convertToPixels(self, x, y):
		return x * 7, y * 7

	'''
	Shifts from center location (266, 240).
	'''
	def getDisplayCoordinates(self, x, y):
		pixels_x, pixels_y = self.convertToPixels(x, y)
		point_x, point_y = int(266 + pixels_x), int(240 - pixels_y)
		return point_x, point_y

	'''
	Calculates x and y shift of your location in the radar
	param newUserLoc: tuple
	'''
	def calculateShift(self, newUserLoc):
		x_shift = newUserLoc[0] - self.userLocation[0]
		y_shift = newUserLoc[1] - self.userLocation[1]
		return x_shift, y_shift

	'''
	adds key to visible list & marks point as visible
	populates radar locations in the point object
	'''
	def makeVisible(self, key):
		point = self.points[key] # find point based on passed in key
		point.isVisible = True # marks point as visible
		self.visible.append(key) # adds key to visible list
		self.redraw.append(key)
		point.markedLocation = point.currentLocation

	'''
	removes from visible list
	unpopulates radar locations in the point object
	'''
	def makeHidden(self, key):
		point = self.points[key]
		if(point.isVisible == True):
			point.isVisible = False
			self.visible.remove(key)
			if point.type == 'ALERT':
				self.device.drawAlert(point.markedLocation[0], point.markedLocation[1], 0x0000)
			elif point.type == 'INTEREST':
				self.device.drawInterest(point.markedLocation[0], point.markedLocation[1], 0x0000)
			elif point.type == 'CRUMB':
				pass
			else:
				pass
		point.markedLocation = (0,0)

	'''
	Draws box around select for VIEW state
	'''
	def drawSelectBox(self, point, color):
		self.device.layer(0)
		time.sleep(0.01)
		print(point.name, point.distance, point.markedLocation)
		x_pixel, y_pixel = self.getDisplayCoordinates(point.markedLocation[0], point.markedLocation[1])
		self.device.drawRect(x_pixel - 20, y_pixel - 20, 40, 40, color, 0)

	def drawTagBox(self, color):
		self.device.layer(0)
		time.sleep(0.01)
		self.device.drawRect(180, 310, 170, 40, color, 1)

	def drawTypeBox(self, color):
		self.device.layer(0)
		time.sleep(0.01)
		self.device.drawRect(190, 260, 170, 40, color, 1)

	'''
	need a way to update currentLocation of all points
	maybe done while updating Radar?

	need to update visible list in order of nearby
	'''

	'''
	converts gps coordinates to cartesian coordinates in x and y
	'''
	def gpsToCartesian(gpsLocation):
		latitude = gpsLocation[0]
		longitude = gpsLocation[1]
		x = 111111*math.cos(math.radians(latitude))
		y = 111111*longitude
		newLocation = (x,y)
		return newLocation

	'''
	updates redraw list by comparing marked location and its current radar location
	redraw list contains all points that need to be redrawn by the display
	- points whose current location is > 1m away from it's marked location
	'''
	def updateRedraw(self):
		for key in self.visible:
			# distance = math.sqrt((self.points[key].currentLocation[0] - self.points[key].markedLocation[0])**2 + (self.points[key].currentLocation[1] - self.points[key].markedLocation[1])**2)
			distance = math.sqrt(point.currentLocation[0]**2 + point.currentLocation[1]**2)
			if distance >= 1:
				# self.points[key].updateMarkedLoc()
				if key not in self.redraw:
					self.redraw.append(key)
				# self.points[key].markedLocation = self.points[key].currentLocation
			elif distance < 1:
				pass

	'''
	Check to see if need to redraw a point
	makes Visible/hidden points (using makeVisible/makeHidden)
	adds to redraw list (using updateRedraw)
	'''
	def updateRadar(self):
		for key, point in self.points.items():
			pointLocation = self.gpsToCartesian(point.gpsLocation)
			self.userLocationCartesian = self.gpsToCartesian(self.userLocation)
			point.currentLocation = (pointLocation[0] - self.userLocationCartesian[0], pointLocation[1] - self.userLocationCartesian[1])
			# distance = math.sqrt((self.userLocation[0] - point.currentLocation[0])**2 + (self.userLocation[1] - point.currentLocation[1])**2)
			distance = math.sqrt(point.currentLocation[0]**2 + point.currentLocation[1]**2)
			point.distance = distance
			if distance > 30:
				# Check if point is in REDRAW list
				# If it is, remove it if distance greater than 30m
				if key in self.redraw:
					self.redraw.remove(key)
				self.makeHidden(key)
			elif distance <= 30 and point.isVisible == False:
				# if key not in self.redraw:
				self.makeVisible(key)
				# Add point to REDRAW list
				# self.redraw.append(point)

	'''
	Updates display from redraw list
	'''
	def refresh(self):
		# print (len(self.redraw))
		if len(self.redraw) != 0:
			key = self.redraw[0]
			# print('Key: ' + str(key))
			point = self.points[key]
			# print('TYPE: ' + point.type)
			x, y = self.getDisplayCoordinates(point.markedLocation[0], point.markedLocation[1])

			if point.type == 'DANGER':
				self.device.drawDanger(x, y, 0x0000)
				point.markedLocation = point.currentLocation
				x, y = self.getDisplayCoordinates(point.markedLocation[0], point.markedLocation[1])
				self.device.drawDanger(x, y, 0xf800)

			elif point.type == 'INTEREST':
				self.device.drawInterest(x, y, 0x0000)
				point.markedLocation = point.currentLocation
				x, y = self.getDisplayCoordinates(point.markedLocation[0], point.markedLocation[1])
				self.device.drawInterest(x, y, 0x001f)

			elif point.type == 'CRUMB':
				self.device.drawCrumb(x, y, 0x0000)
				point.markedLocation = point.currentLocation
				x, y = self.getDisplayCoordinates(point.markedLocation[0], point.markedLocation[1])
				self.device.drawCrumb(x, y, 0xf81f)

			else:
				print('ERROR!')
			self.redraw.pop(0)
		else:
			pass
