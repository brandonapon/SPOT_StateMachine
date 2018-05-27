from transitions import Machine

class Device(object):
    states = ['Main', 'View', 'Info', 'Mark', 'Confirm', 'Alert']
    transitions = [
    { 'trigger': 'Main->View',                  'source': 'Main',       'dest': 'View' },
    { 'trigger': 'Main->Mark',                  'source': 'Main',       'dest': 'Mark' },
    { 'trigger': 'Main->View->Cancel',          'source': 'View',       'dest': 'Main' },
    { 'trigger': 'Main->View->Select',          'source': 'View',       'dest': 'Info' },
    { 'trigger': 'Main->View->Select->Home',    'source': 'Info',       'dest': 'Main' },
    { 'trigger': 'Main->View->Select->Go Back', 'source': 'Info',       'dest': 'View' },
    { 'trigger': 'Main->Mark->Cancel',          'source': 'Mark',       'dest': 'Main' },
    { 'trigger': 'Main->Mark->Mark',            'source': 'Mark',       'dest': 'Confirm' },
    { 'trigger': 'Main->Mark->Mark->Cancel',    'source': 'Confirm',    'dest': 'Mark' },
    { 'trigger': 'Main->Mark->Mark->Confirm',   'source': 'Confirm',    'dest': 'Main' },
    { 'trigger': 'AlertInt->Dismiss',           'source': 'Alert',      'dest': 'Main' },
    { 'trigger': 'AlertInt->View',              'source': 'Alert',      'dest': 'Info' },
    { 'trigger': 'AlertDan->Dismiss',           'source': 'Alert',      'dest': 'Main' },
    { 'trigger': 'AlertInt->View',              'source': 'Alert',      'dest': 'Info' }
    ] 

    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=Device.states, transitions=Device.transitions, initial='Main')

# spot = Device("SPOT")
# print(spot.state)
# spot.trigger('Main->View')
# print(spot.state)