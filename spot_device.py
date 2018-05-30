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

	def __init__(self, device):
		"""
		Initialize all components for SPOT device.
		"""
		self.device = device
		self.radar = Radar(device)
		device.setImageAddress()
		device.beginTX(1)
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
		parent.device.drawMainScreen() # Main
		for val in parent.radar.visible:
			parent.radar.redraw.append(val)
		parent.radar.refresh()

		#REDRAW ALL VISIBLE

	def on_event(self, event):
		if event == 'TOP':
			return ViewState(self.parent)
		elif event == 'BOTTOM':
			return MarkState(self.parent)
		return self

	def loop(self):
		'''
		Functionality:
		- refresh display function(updates points)
		'''
		self.parent.radar.updateRadar()
		self.parent.radar.updateRedraw()
		self.parent.radar.refresh()

class ViewState(SPOT):
	"""
	State that shows VIEW screen.
	"""

	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent):
		self.parent = parent
		parent.device.clearAll()
		parent.device.drawViewScreen() # View
		""" ADDED """
		# parent.device.layer(1)
		# points = parent.device.radar.points
		""" >> DRAW POINTS HERE << """

	def on_event(self, event):
		'''
		Add draw box around point function on CW or CCW event
		'''
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return InfoState(self.parent, )
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
		parent.device.drawSelectView()
		parent.device.displayTag(parent.device.radar.points[key].tag)
		parent.device.displayDistance(parent.device.radar.points[key].distance)
		parent.device.displayCreatedBy(parent.device.radar.points[key].createdBy)

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

	global counter

	# self.point = Point()

	def __init__(self, parent):
		self.parent = parent
		""" ADDED """
		# distance = parent.device.range_poll()
		# gps = parent.device.readFromGPS()
		# pic = parent.device.snapPic(0,0)

		parent.device.clearAll()
		parent.device.drawAfterMark()
		parent.device.prepareToSend()
		# parent.device.draw2X(100,15,15, 0xf800)
		parent.device.snapPic(0,0)
		# parent.device.draw2X(150,15,15, 0xf800)
		parent.device.conversion()
		parent.device.beginCameraTransfer(4)
		parent.device.writeToTX(4, 'd')


	def on_event(self, event):
		if event == 'TOP':
			return MarkState(self.parent)
		elif event == 'BOTTOM':
			""" ADDED """
			# parent.device.beginCameraTransfer(""" >> NEED ADDRESS << """)
			# stamp = createTimestamp()
			# self.point.name = 'point_{}'.format(stamp)
			# self.point.name = 'point_{}'.format(counter)
			# counter = counter + 1
			return MainState(self.parent)
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

	def __init__(self, parent):
		self.parent = parent
		""" ADDED """
		# parent.device.play_sequence([16, -100, 16, -100, 16, -50, 16])
		parent.device.clearAll()
		parent.device.drawAlertInterest() # Main

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return InfoState(self.parent, key)
		return self

	def loop(self):
		'''
		do nothing
		'''
		pass
