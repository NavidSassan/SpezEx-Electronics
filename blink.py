# https://www.coderdojotc.org/micropython/basics/03-blink/

from machine import Pin
import time

input_pin = Pin(26, Pin.IN)

digital_input = Pin(26, Pin.IN)
led = Pin(2, Pin.OUT)

while True:
    led.on()
    time.sleep(0.2)
    led.off()
    time.sleep(0.2)

# 1:1
# while True:
#     btn = digital_input.value()
#     print(f'btn: {btn}')
#     if btn == 1:
#         led.on()
#     else:
#         led.off()
#
#     time.sleep(0.1)


# toggle
# state = False
#
# while True:
#     btn = digital_input.value()
#     print(f'btn: {btn}')
#
#     if btn == 1:
#         state = not state
#         print(f'state: {state}')
#         led.value(state)
#         time.sleep(0.3)
#
#     time.sleep(0.1)
#

# toggle (shorter)
# while True:
#     if btn.value():
#         led.toggle()
#     time.sleep(0.1)
