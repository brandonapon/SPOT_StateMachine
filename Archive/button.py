class Button(object):
    def __init__(self):
        self.options = {1:'View', 2:'Mark', 3:'Cancel', 4:'Select', 5:'Home', 6:'Go Back', 7:'Confirm', 8:'Dismiss'}
        self.type = ''
        # May not need PRESSED flag. Check event loop documentation.
        self.pressed = False

class ButtonPair(object):
	def __init__(self):
		self.button_1 = Button()
		self.button_2 = Button()

	def configuration_1(self):
		# VIEW and MARK
		self.button_1.type = self.button_1.options[1]
		self.button_1.pressed = False
		self.button_2.type = self.button_2.options[2]
		self.button_2.pressed = False

	def configuration_2(self):
		# CANCEL and SELECT
		self.button_1.type = self.button_1.options[3]
		self.button_1.pressed = False
		self.button_2.type = self.button_2.options[4]
		self.button_2.pressed = False

	def configuration_3(self):
		# HOME and GO BACK
		self.button_1.type = self.button_1.options[5]
		self.button_1.pressed = False
		self.button_2.type = self.button_2.options[6]
		self.button_2.pressed = False

	def configuration_4(self):
		# CANCEL and MARK
		self.button_1.type = self.button_1.options[3]
		self.button_1.pressed = False
		self.button_2.type = self.button_2.options[2]
		self.button_2.pressed = False

	def configuration_5(self):
		# CANCEL and CONFIRM
		self.button_1.type = self.button_1.options[3]
		self.button_1.pressed = False
		self.button_2.type = self.button_2.options[7]
		self.button_2.pressed = False

	def configuration_6(self):
		# DISMISS and VIEW
		self.button_1.type = self.button_1.options[8]
		self.button_1.pressed = False
		self.button_2.type = self.button_2.options[1]
		self.button_2.pressed = False	