from state_machine import Device
from state import State
from spot_states import *
from ui import *
import asyncio
import time

def __init__(self)
    self.iop = pynq.lib.PynqMicroblaze(mb_info, IOP_EXECUTABLE)
    
class SPOT(object):
    """
    Object declaration for SPOT device.
    """

    def __init__(self, user):
        """
        Initialize all components for SPOT device.
        """
        self.state = MainState()
        self.user = user
    
    def on_event(self, event):
        """
        This is the main chunk of the state machine. Incoming events are delegated to 
        the given states which then handle the event. The result is then assigned as
        the new state.
        """

        # Next state will be the result of of the on_event function.
        self.state = self.state.on_event(event)

async def button_to_led(number):
    button = base.buttons[number]
    led = base.leds[number]
    while True:
        await button.wait_for_level_async(1)
        led.on()
        await button.wait_for_level_async(0)
        led.off()


async def wake_up(delay):
    '''A coroutine that will yield to asyncio.sleep() for a few seconds
       and then resume, having preserved its state while suspended
    '''

    start_time = time.time()
    print(f'The time is: {time.strftime("%I:%M:%S")}')
    print(f"Suspending coroutine 'wake_up' at 'await` statement\n")
    await asyncio.sleep(delay)
    print(f"Resuming coroutine 'wake_up' from 'await` statement")
    end_time = time.time()
    sleep_time = end_time - start_time
    print(f"'wake-up' was suspended for precisely: {sleep_time} seconds")

# This is the MAIN (grand/event) LOOP.
def main():
    # Instantiate SPOT device. Initial state is "Main".
    # This object is the PHYSICAL (as in, peripherals) device.
    # NOT THE USER INTERFACE!
    device = SPOT("TEST_USER")

    # Create UI object.
    interface = UI()

    # Create both buttons.
    button_pair = ButtonPair()
    button_pair.configuration_1()

    """
    1) Either need to link button pair to SPOT device, OR
    2) Make button object part of SPOT physical device (above).

    The issue here is that the buttons are the "glue" between the 
    interface and the physical device. Probably better to keep it 
    a separate object and link them manually.
    """

    radar = Radar()


"""
NEED A WAY TO TRIGGER A KERNEL RESTART 
Just the reset button on the PYNQ? Or power cycle?
"""
if __name__ == '__main__':
    eventLoop = asyncio.get_event_loop()
    try:
        print("Creating task for coroutine 'main'\n")
        wakeUpTask = eventLoop.create_task()
    except RuntimeError as error:
        print(f'{error}' + ' - restart kernel to re-run the event loop')
    finally:
        eventLoop.close()
