# https://www.coderdojotc.org/micropython/basics/03-blink/

from machine import Pin
import time


btn = Pin(26, Pin.IN)
led = Pin(2, Pin.OUT)

counter = 0

while True:

    print(f'counter: {counter}')

    if btn.value() == 1:
        counter += 1

    if counter % 2 == 0:
        led.off()
    else:
        led.on()

    time.sleep(0.2)
