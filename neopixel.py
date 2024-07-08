from machine import Pin
import neopixel

led_length = 10

pin = Pin(22, Pin.OUT)
np = neopixel.NeoPixel(pin, led_length)

# Draw a red gradient.
for i in range(led_length):
    np[i] = ((i + 1) * 8, 0, 0)
    # np[i] = (100, 100, 100)

print(np)

# Update the strip.
np.write()
