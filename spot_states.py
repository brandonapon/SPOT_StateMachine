from state import State

class MainState(State):
	"""
	State that shows MAIN screen.
	"""
	def on_event(self, event):
		if event == 'MAIN':
			return 


class InfoState(State):
	pass


class ViewState(State):
	pass


class MarkState(State):
	pass


class ConfirmState(State):
	pass


class AlertState(State):
	pass

