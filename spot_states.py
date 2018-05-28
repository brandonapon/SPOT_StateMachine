from state import State
from ui import UI
import time
import datetime

# relevant events for now: TOP and BOTTOM
# error event is ERROR

haptic = Haptic() # Declare haptic motor here?
rangefinder = Rangefinder() # Declare rangefinder here?
camera = Camera() # Declare camera here?
# Might need to create different temp objects for each peripheral. Easier to store data that way.
# Could maybe get away with using the asyncio calls only, but could be issues w/ timing.

global counter = 1

def createTimestamp():
	timestamp = time.time()
	timestamp_string_converted = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M')
	return timestamp_string_converted

class MainState(State):
	"""
	State that shows MAIN screen.
	"""
	
	self.state = 'MAIN'
	self.button_pressed = False
	self.button = ''

	def __init__(self):
		interface.drawMainScreen() # Main
    	button_pair.configuration_1()

	def assignButton(self):
		# check what button is pressed, and assign respective string
		if self.TOP_BUTTON:

	def on_event(self, event):
		if event == 'TOP':
			return ViewState()
		elif event == 'BOTTOM':
			return MarkState()
		return self
	
	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class ViewState(State):
	"""
	State that shows VIEW screen.
	"""
	def __init__(self):
		interface.drawViewScreen() # Main
    	button_pair.configuration_2()

	def on_event(self, event):
		if event == 'TOP':
			return MainState()
		elif event == 'BOTTOM':
			return ConfirmState()
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class InfoState(State):
	"""
	State that shows INFO screen.
	"""
	def __init__(self):
		interface.drawSelectView()
    	button_pair.configuration_3()

	def on_event(self, event):
		if event == 'TOP':
			return MainState()
		elif event == 'BOTTOM':
			return ViewState()
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class MarkState(State):
	"""
	State that shows MARK screen.

	THIS IS THE ONLY FUNCTION WHERE WE NEED:
	1) RANGEFINDER
	2) CAMERA
	"""
	def __init__(self):
		interface.drawMarkScreen()
    	button_pair.configuration_4()

	def on_event(self, event):
		if event == 'TOP':
			return MainState()
		elif event == 'BOTTOM':
			return ConfirmState()
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class ConfirmState(State):
	"""
	State that shows CONFIRM MARK screen.
	"""

	global counter
	self.point = Point()

	def __init__(self):
		self.point.distance = rangefinder.poll() # <--------- Placeholder
		self.point.picture = camera.snapshot() # <-------- Placeholder, I forgot the exact command despite having done it a million times...
		interface.drawAfterMark()
    	button_pair.configuration_5()

	def on_event(self, event):
		if event == 'TOP':
			return MarkState()
		elif event == 'BOTTOM':
			stamp = createTimestamp()
			self.point.name = 'point_{}'.format(stamp)
			# self.point.name = 'point_{}'.format(counter)
			global counter = counter + 1
			return MainState()
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class AlertState(State):
	"""
	State that shows ALERT screen.

	----> NEED HAPTIC IN THIS STATE <----
	"""
	def __init__(self):
		haptic.buzz()
		interface.drawAlertInterest() # Main
    	button_pair.configuration_6()

	def on_event(self, event):
		if event == 'TOP':
			return MainState()
		elif event == 'BOTTOM':
			return InfoState()
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")