# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
# https://docs.micropython.org/en/latest/library/framebuf.html

from machine import Pin, SoftI2C
import _thread
import ssd1306
import time

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

led = Pin(2, Pin.OUT)


def display_skull():
    print('starting display_skull')
    counter = 0
    while True:

        counter += 1
        display.fill(0) # Clear the display

        display.text(f'Warning! {counter}', 10, 30, 1)

        display.show() # Update the display

        time.sleep(2)


def blink():
    print('starting blink')
    while True:
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)


print('start')

_thread.start_new_thread(display_skull, ())
_thread.start_new_thread(blink, ())
