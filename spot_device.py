# from state_machine import Device
from pynq.lib.arduino.state import State
# from pynq.lib.arduino.spot_states import *
# from ui import *
import asyncio
import time

# def __init__(self)
#     self.iop = pynq.lib.PynqMicroblaze(mb_info, IOP_EXECUTABLE)

class SPOT(State):
	"""
	Object declaration for SPOT device.
	"""

	state = None
	# user = None
	device = None

	def __init__(self, device):
		"""
		Initialize all components for SPOT device.
		"""
		self.device = device
		# self.user = user

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

	def loop(self, ):
		'''
		Based on state, will call state's loop function in event loop
		'''
		self.state.loop()

# async def button_to_led(number):
#     button = base.buttons[number]
#     led = base.leds[number]
#     while True:
#         await button.wait_for_level_async(1)
#         led.on()
#         await button.wait_for_level_async(0)
#         led.off()
#
#
# async def wake_up(delay):
#     '''A coroutine that will yield to asyncio.sleep() for a few seconds
#        and then resume, having preserved its state while suspended
#     '''
#
#     start_time = time.time()
#     print(f'The time is: {time.strftime("%I:%M:%S")}')
#     print(f"Suspending coroutine 'wake_up' at 'await` statement\n")
#     await asyncio.sleep(delay)
#     print(f"Resuming coroutine 'wake_up' from 'await` statement")
#     end_time = time.time()
#     sleep_time = end_time - start_time
#     print(f"'wake-up' was suspended for precisely: {sleep_time} seconds")
#
# # This is the MAIN (grand/event) LOOP.
# def main():
#     # Instantiate SPOT device. Initial state is "Main".
#     # This object is the PHYSICAL (as in, peripherals) device.
#     # NOT THE USER INTERFACE!
#     device = SPOT("TEST_USER")
#
#     # Create UI object.
#     interface = UI()
#
#     # Create both buttons.
#     button_pair = ButtonPair()
#     button_pair.configuration_1()
#
#     """
#     1) Either need to link button pair to SPOT device, OR
#     2) Make button object part of SPOT physical device (above).
#
#     The issue here is that the buttons are the "glue" between the
#     interface and the physical device. Probably better to keep it
#     a separate object and link them manually.
#     """
#
#     radar = Radar()
#
#
# """
# NEED A WAY TO TRIGGER A KERNEL RESTART
# Just the reset button on the PYNQ? Or power cycle?
# """
# if __name__ == '__main__':
#     eventLoop = asyncio.get_event_loop()
#     try:
#         print("Creating task for coroutine 'main'\n")
#         wakeUpTask = eventLoop.create_task()
#     except RuntimeError as error:
#         print(f'{error}' + ' - restart kernel to re-run the event loop')
#     finally:
#         eventLoop.close()

# from pynq.lib.arduino.state import State
# from pynq.lib.arduino.spot_device import SPOT
# from ui import UI

##############################################################################################

# relevant events for now: TOP and BOTTOM
# error event is ERROR

# NOTE: not possible to declare devices individually. Specific helper function for devices need to be called from arduino_spot.py (the main python functions file)
# haptic = Haptic() # Declare haptic motor here?
# rangefinder = Rangefinder() # Declare rangefinder here?
# camera = Camera() # Declare camera here?

# Might need to create different temp objects for each peripheral. Easier to store data that way.
# Could maybe get away with using the asyncio calls only, but could be issues w/ timing.

counter = 1

def createTimestamp():
	timestamp = time.time()
	timestamp_string_converted = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M')
	return timestamp_string_converted

class MainState(SPOT):
	"""
	State that shows MAIN screen.
	"""

	state = 'MAIN'
	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent):
		self.parent = parent
		parent.device.drawMainScreen() # Main
		# button_pair.configuration_1()

	# def assignButton(self):
	# 	# check what button is pressed, and assign respective string
	# 	if self.TOP_BUTTON:

	def on_event(self, event):
		if event == 'TOP':
			return ViewState(self.parent)
		elif event == 'BOTTOM':
			return MarkState(self.parent)
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class ViewState(SPOT):
	"""
	State that shows VIEW screen.
	"""
	state = 'MAIN'
	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent):
		self.parent = parent
		parent.device.drawViewScreen() # Main
		# button_pair.configuration_2()

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return ConfirmState(self.parent)
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class InfoState(SPOT):
	"""
	State that shows INFO screen.
	"""

	state = 'MAIN'
	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent):
		self.parent = parent
		parent.device.drawSelectView()
		# button_pair.configuration_3()

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return ViewState(self.parent)
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class MarkState(SPOT):
	"""
	State that shows MARK screen.

	THIS IS THE ONLY FUNCTION WHERE WE NEED:
	1) RANGEFINDER
	2) CAMERA
	"""

	state = 'MAIN'
	button_pressed = False
	button = ''
	parent = None


	def __init__(self, parent):
		self.parent = parent
		parent.device.drawMarkScreen()
		# button_pair.configuration_4()

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return ConfirmState(self.parent)
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class ConfirmState(SPOT):
	"""
	State that shows CONFIRM MARK screen.
	"""

	state = 'MAIN'
	button_pressed = False
	button = ''
	parent = None

	global counter

	# self.point = Point()

	def __init__(self, parent):
		self.parent = parent
		# self.point.distance = rangefinder.poll() # <--------- Placeholder
		# self.point.picture = camera.snapshot() # <-------- Placeholder, I forgot the exact command despite having done it a million times...
		parent.device.drawAfterMark()
		# button_pair.configuration_5()

	def on_event(self, event):
		if event == 'TOP':
			return MarkState(self.parent)
		elif event == 'BOTTOM':
			# stamp = createTimestamp()
			# self.point.name = 'point_{}'.format(stamp)
			# self.point.name = 'point_{}'.format(counter)
			counter = counter + 1
			return MainState(self.parent)
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")

class AlertState(SPOT):
	"""
	State that shows ALERT screen.

	----> NEED HAPTIC IN THIS STATE <----
	"""

	state = 'MAIN'
	button_pressed = False
	button = ''
	parent = None

	def __init__(self, parent):
		# haptic.buzz()
		self.parent = parent
		parent.device.drawAlertInterest() # Main
		# button_pair.configuration_6()

	def on_event(self, event):
		if event == 'TOP':
			return MainState(self.parent)
		elif event == 'BOTTOM':
			return InfoState(self.parent)
		return self

	def loop(self):
		while True:
			try:
				print("Currently in <MAIN> state")
				# code for new state change
			except ValueError:
				print("ERROR: Cannot access from current state")
