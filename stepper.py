# https://blog.kutej.net/2017/07/sbt0811_28byj48
# https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/

from machine import Pin
import time

pins = [13, 12, 14, 27]

step_positions = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

def get_step_pos():
    while True:
        for step_pos in step_positions:
            yield step_pos

for pin in pins:
    Pin(pin, Pin.OUT)

stepper = get_step_pos()

while True:
    for pin, value in zip(pins, next(stepper)):
        # print(f'setting {pin} to {value}')
        Pin(pin, Pin.OUT, value=value)

    time.sleep(0.001)
