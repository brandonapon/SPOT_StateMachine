
# coding: utf-8

# In[1]:


from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")

import time

#init display
from pynq.lib.arduino import Arduino_Displaycam
test = Arduino_Displaycam(base.ARDUINO)
test.init()
test.gpio()
test.pwm()


# In[ ]:


from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")

from pynq.lib.arduino import Arduino_SPOT
device = Arduino_SPOT(base.ARDUINO,Arduino_SPOT)


# In[3]:


# device.drawMainScreen()
device.layerMode(1)
device.layerEffect(2)
device.layer(1) # 0 (foreground), 1 (background)
device.drawUpperButton()
device.drawRadar()


# In[4]:


device.clearWindow(1)


# In[ ]:


from pynq.lib.arduino.spot_device import *
import asyncio

spot = SPOT(device)
spot.start()

'''
Types of events:
TOP
BOT
CW
CCW
ERROR
'''

@asyncio.coroutine
def buttonPress(num):
    event = 'ERROR'
    while True:
        yield from base.buttons[num].wait_for_value_async(1)
        if(num == 0):
            event = 'TOP'
            while base.buttons[num].read():
                base.leds[num].toggle()
                yield from asyncio.sleep(0.1)
            base.leds[num].off()
        elif(num == 1):
            event = 'BOTTOM'
            while base.buttons[num].read():
                base.leds[num].toggle()
                yield from asyncio.sleep(0.1)
            base.leds[num].off()
        else:
            event = 'ERROR'
        spot.on_event(event)

tasks = [asyncio.ensure_future(buttonPress(i)) for i in range(4)]


# In[6]:


import psutil

@asyncio.coroutine
def print_cpu_usage():
    # Calculate the CPU utilisation by the amount of idle time
    # each CPU has had in three second intervals
    last_idle = [c.idle for c in psutil.cpu_times(percpu=True)]
    while True:
        yield from asyncio.sleep(3)
        next_idle = [c.idle for c in psutil.cpu_times(percpu=True)]
        usage = [(1-(c2-c1)/3) * 100 for c1,c2 in zip(last_idle, next_idle)]
        print("CPU Usage: {0:3.2f}%, {1:3.2f}%".format(*usage))
        last_idle = next_idle

tasks.append(asyncio.ensure_future(print_cpu_usage()))


# In[5]:


if base.switches[0].read():
    print("Please set switch 0 low before running")
else:
    base.switches[0].wait_for_value(1)


# In[6]:


[t.cancel() for t in tasks]
