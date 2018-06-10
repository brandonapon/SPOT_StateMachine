from pynq.lib.arduino.state import State
from pynq.lib.arduino.data import *
import asyncio
import time

class SPOT(State):
	"""
	Object declaration for SPOT device.
	"""

	state = None
	device = None
	radar = None
	createdBy = 'SPOT'

	def __init__(self, device):
		"""
		Initialize all components for SPOT device.
		"""
		self.device = device
		self.radar = Radar(device)
		device.setImageAddress()
		device.beginTX(1)
		device.layerMode(1)
		device.layerEffect(2)
		device.layer(1)
		# self.radar.points = dict([(i, Point('point_{}'.format(i))) for i in range(0, 10)])
		# self.radar.getDisplayCoordinates(thing1, thing2)

	def start(self):
		self.state = MainState(self)

	def on_event(self, event):
		"""
		This is the main chunk of the state machine. Incoming events are delegated to
		the given states which then handle the event. The result is then assigned as
		the new state.
		"""
		# Next state will be the result of of the on_event function.
		self.state = self.state.on_event(event)

	def loop(self):
		'''
		Based on state, will call state's loop function in event loop
		'''
		self.state.loop()
		# receive testing
		# if self.device.hasMessages():
		# 	print(self.device.readFromTX())

# def createTimestamp(): #unnecesary?
# 	timestamp = time.time()
# 	timestamp_string_converted = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M')
# 	return timestamp_string_converted

"""
# NOTE: For reference only.

states = ['Main', 'View', 'Info', 'Mark', 'Confirm', 'Alert']
transitions = [
{ 'trigger': 'Main->View',                  'source': 'Main',       'dest': 'View' },
{ 'trigger': 'Main->Mark',                  'source': 'Main',       'dest': 'Mark' },
{ 'trigger': 'Main->View->Cancel',          'source': 'View',       'dest': 'Main' },
{ 'trigger': 'Main->View->Select',          'source': 'View',       'dest': 'Info' },
{ 'trigger': 'Main->View->Select->Home',    'source': 'Info',       'dest': 'Main' },
{ 'trigger': 'Main->View->Select->Go Back', 'source': 'Info',       'dest': 'View' },
{ 'trigger': 'Main->Mark->Cancel',          'source': 'Mark',       'dest': 'Main' },
{ 'trigger': 'Main->Mark->Mark',            'source': 'Mark',       'dest': 'Confirm'},
{ 'trigger': 'Main->Mark->Mark->Cancel',    'source': 'Confirm',    'dest': 'Mark' },
{ 'trigger': 'Main->Mark->Mark->Confirm',   'source': 'Confirm',    'dest': 'Main' },
{ 'trigger': 'AlertInt->Dismiss',           'source': 'Alert',      'dest': 'Main' },
{ 'trigger': 'AlertInt->View',              'source': 'Alert',      'dest': 'Info' },
{ 'trigger': 'AlertDan->Dismiss',           'source': 'Alert',      'dest': 'Main' },
{ 'trigger': 'AlertDan->View',				'source': 'Alert',		'dest': 'Info'}
]
"""

class MainState(SPOT):
	"""
	State that shows MAIN screen.
	"""

	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent):
		'''
		clears screen
		Draws main screen
		'''
		self.parent = parent
		parent.device.clearAll()
		time.sleep(0.05)
		parent.device.drawMainScreen() # Main
		parent.device.layer(1)
		for val in parent.radar.visible:
			parent.radar.redraw.append(val)
		while len(parent.radar.redraw) != 0:
			parent.radar.refresh()
		# print (parent.radar.redraw)


		#REDRAW ALL VISIBLE

	def on_event(self, event):
		if event == 'TOP':
			return ViewState(self.parent)
		elif event == 'BOTTOM':
			return MarkState(self.parent)
		# elif event == "CCW":
		# 	print('CCW')
		# elif event == "CW":
		# 	print('CW')
		return self

	def loop(self):
		'''
		Functionality:
		- refresh display function(updates points)
		'''
		# print('in loop')
		self.parent.radar.updateRadar()
		self.parent.radar.updateRedraw()
		self.parent.radar.refresh()

		# currPoint = self.parent.radar.points[1]
		# if(currPoint.currentLocation[0] > -10):
		# 	newTuple = (currPoint.currentLocation[0] - 0.25, currPoint.currentLocation[1])
		# 	currPoint.currentLocation = newTuple
		# print ('point1 = ', currPoint.currentLocation)
		#
		# currPoint = self.parent.radar.points[2]
		# if(currPoint.currentLocation[1] > -10):
		# 	newTuple = (currPoint.currentLocation[0], currPoint.currentLocation[1] - 0.25)
		# 	currPoint.currentLocation = newTuple
		# print ('point2 = ', currPoint.currentLocation)

class ViewState(SPOT):
	"""
	State that shows VIEW screen.
	"""

	button_pressed = False
	button = ''
	parent = None
	select = 0

	def __init__(self, parent):
		self.parent = parent
		parent.device.clearAll()
		time.sleep(0.05)
		parent.device.drawViewScreen() # View
		parent.radar.redraw = []
		for val in parent.radar.visible:
			parent.radar.redraw.append(val)
		print (parent.radar.redraw)
		while len(parent.radar.redraw) != 0:
			parent.radar.refresh()
		# print('choosing point')
		# print('select', self.select)
		# print(parent.radar.points)
		if(len(self.parent.radar.visible) != 0):
			point = parent.radar.points.get(self.parent.radar.visible[self.select])
			parent.radar.drawSelectBox(point, 0xffe0)


	def on_event(self, event):
		'''
		Add draw box around point function on CW or CCW event
		'''
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			if(len(self.parent.radar.visible) != 0):
				return InfoState(self.parent, self.parent.radar.visible[self.select])
		elif event == "LEFT":
			if(len(self.parent.radar.visible) != 0):
				point = self.parent.radar.points.get(self.parent.radar.visible[self.select])
				self.parent.radar.drawSelectBox(point, 0x0000)
				time.sleep(0.05)
				self.select -= 1
				self.select = self.select % len(self.parent.radar.visible)
				point = self.parent.radar.points.get(self.parent.radar.visible[self.select])
				self.parent.radar.drawSelectBox(point, 0xffe0)
		elif event == "RIGHT":
			if(len(self.parent.radar.visible) != 0):
				point = self.parent.radar.points.get(self.parent.radar.visible[self.select])
				self.parent.radar.drawSelectBox(point, 0x0000)
				time.sleep(0.05)
				self.select += 1
				self.select = self.select % len(self.parent.radar.visible)
				point = self.parent.radar.points.get(self.parent.radar.visible[self.select])
				self.parent.radar.drawSelectBox(point, 0xffe0)
		return self

	def loop(self):
		'''
		do nothing
		'''
		pass

class InfoState(SPOT):
	"""
	State that shows INFO screen.
	"""

	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent, key):
		self.parent = parent
		parent.device.clearAll()
		time.sleep(0.05)
		point = parent.radar.points.get(key)
		parent.device.drawInfoState()
		if point.type == 'DANGER':
			parent.device.write_CUSTOM(point.type, 200, 265, 0xf800)
		else:
			parent.device.write_CUSTOM(point.type, 200, 265, 0x07e8)
		parent.device.write_CUSTOM(point.tag, 190, 315, 0xffff) # Variable tag
		parent.device.write_CUSTOM(str(point.distance), 270, 365, 0xffff) # Variable distance
		parent.device.write_CUSTOM(point.createdBy, 300, 415, 0xffff) # Variable c/b
		val = parent.radar.openPicture(parent.device.drawAddr, point.picture)
		parent.device.drawImage(100,10)

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return ViewState(self.parent)
		return self

	def loop(self):
		'''
		do nothing
		'''
		pass

class MarkState(SPOT):
	"""
	State that shows MARK screen.
	"""

	button_pressed = False
	button = ''
	parent = None


	def __init__(self, parent):
		self.parent = parent
		parent.device.clearAll()
		time.sleep(0.05)
		parent.device.drawMarkScreen()
		# parent.device.beginTX(1)

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return ConfirmState(self.parent)
		return self

	def loop(self):
		'''
		do nothing
		maybe add real-time range finder distance
		'''
		pass

class ConfirmState(SPOT):
	"""
	State that shows CONFIRM MARK screen.
	"""

	button_pressed = False
	button = ''
	parent = None
	counter = 0
	tag = ''
	objectType = ''
	gpsVal = ''
	imuVal = ''
	rangeVal = ''

	# self.point = Point()

	def __init__(self, parent):
		self.parent = parent
		# distance = parent.device.range_poll()
		# gps = parent.device.readFromGPS()

		parent.device.clearAll()
		parent.device.drawAfterMark()
		time.sleep(0.05)
		self.gpsVal, self.imuVal, self.rangeVal = parent.device.prepareToSend()
		parent.device.play_sequence([16])
		time.sleep(1)
		parent.device.stop()
		parent.device.snapPic(100,10)
		self.objectType = 'DANGER'
		self.tag = parent.radar.tags[0]
		self.parent.radar.drawTypeBox(0x2104)
		self.parent.radar.drawTagBox(0x2104)
		parent.device.write_CUSTOM(self.tag, 185, 315, 0xffff) # Variable tag
		parent.device.write_CUSTOM('DANGER', 200, 265, 0xf800) # Variable type

	def on_event(self, event):
		if event == 'TOP':
			return MarkState(self.parent)
		elif event == 'BOTTOM':
			# parent.device.beginCameraTransfer(""" >> NEED ADDRESS << """)
			print('making pictureList')
			pictureList = []
			print('writing image data')
			for index in range(76800):
				pictureList.append(self.parent.device.drawAddr[index])
			print('creatingpoint')
			self.parent.radar.createPoint(len(self.parent.radar.points), self.tag, self.parent.createdBy, self.parent.radar.userLocation, self.objectType, pictureList)
			print('image conversion')
			parent.device.conversion()
			print('sending gps')
			self.writeToTX(4, self.gpsVal)
			print('sending imu')
			self.writeToTX(4, self.imuVal)
			print('sending range')
			self.writeToTX(4, self.rangeVal)
			print('sending tag')
			self.writeToTX(4, "t,"+ self.tag)
			print('sending image')
			parent.device.beginCameraTransfer(4)
			parent.device.writeToTX(4, 'd')
			return MainState(self.parent)
		elif event == 'RIGHT': # Right button
			# First wipe the text area with a black box, then write the selected text
			# self.parent.device.play_sequence([16])
			self.parent.radar.drawTagBox(0x2104)
			self.counter += 1
			if (self.counter % len(self.parent.radar.tags)) < 4:
				self.parent.radar.drawTypeBox(0x2104)
				self.objectType = 'DANGER'
				self.parent.device.write_CUSTOM('DANGER', 200, 265, 0xf800) # Variable tag
			elif (self.counter % len(self.parent.radar.tags)) < 8:
				self.parent.radar.drawTypeBox(0x2104)
				self.objectType = 'INTEREST'
				self.parent.device.write_CUSTOM('INTEREST', 200, 265, 0x07e8) # Variable tag
			else:
				self.objectType = 'NONE'
			self.parent.device.write_CUSTOM(self.parent.radar.tags[self.counter % len(self.parent.radar.tags)], 190, 315, 0xffff) # Variable tag
			self.tag = self.parent.radar.tags[self.counter % len(self.parent.radar.tags)]

			# self.parent.device.stop()
		elif event == 'LEFT':
			# First wipe the text area with a black box, then write the selected text
			# self.parent.device.play_sequence([16])
			self.parent.radar.drawTagBox(0x2104)
			self.counter -= 1
			if (self.counter % len(self.parent.radar.tags)) < 4:
				self.parent.radar.drawTypeBox(0x2104)
				self.objectType = 'DANGER'
				self.parent.device.write_CUSTOM('DANGER', 200, 265, 0xf800) # Variable tag
			elif (self.counter % len(self.parent.radar.tags)) < 8:
				self.parent.radar.drawTypeBox(0x2104)
				self.objectType = 'INTEREST'
				self.parent.device.write_CUSTOM('INTEREST', 200, 265, 0x07e8) # Variable tag
			else:
				self.objectType = 'NONE'
			self.parent.device.write_CUSTOM(self.parent.radar.tags[self.counter % len(self.parent.radar.tags)], 190, 315, 0xffff) # Variable tag
			self.tag = self.parent.radar.tags[self.counter % len(self.parent.radar.tags)]
			# self.parent.device.stop()
		return self

	def loop(self):
		'''
		do nothing
		'''
		pass

class AlertState(SPOT):
	"""
	State that shows ALERT screen.
	"""

	button_pressed = False
	button = ''
	parent = None
	state = None

	def __init__(self, parent, key, lastState):
		self.state = lastState
		self.parent = parent
		parent.device.clearAll()
		parent.device.drawAlertState()
		point = parent.radar.points[key]
		point.ack = True
		if point.type == 'DANGER':
			parent.device.write_CUSTOM(point.type, 200, 265, 0xf800)
		else:
			parent.device.write_CUSTOM(point.type, 200, 265, 0x07e8)
		parent.device.write_CUSTOM(point.tag, 190, 315, 0xffff) # Variable tag
		parent.device.write_CUSTOM(str(point.distance), 270, 365, 0xffff) # Variable distance
		parent.device.write_CUSTOM(point.createdBy, 300, 415, 0xffff) # Variable c/b
		val = parent.radar.openPicture(parent.device.drawAddr, point.picture)
		parent.device.drawImage(100,10)

	def on_event(self, event):
		if event == 'BOTTOM':
			return type(self.state)(self.parent)
		return self

	def loop(self):
		'''
		do nothing
		'''
		pass
