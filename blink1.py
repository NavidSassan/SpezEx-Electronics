# https://www.coderdojotc.org/micropython/basics/03-blink/

from machine import Pin
import time


btn = Pin(26, Pin.IN)
led = Pin(2, Pin.OUT)

state = False

while True:

    print(f'state: {state}')

    if btn.value() == 1:

        state = not state
        led.value(state)

        while btn.value() == 1:
            time.sleep(0.1)

    led.value(state)

    time.sleep(0.1)
