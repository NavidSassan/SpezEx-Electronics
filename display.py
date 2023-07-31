# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
# https://docs.micropython.org/en/latest/library/framebuf.html

from machine import Pin, SoftI2C
import ssd1306

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
print(i2c.scan())

display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Now you can use the display object to control the display
display.fill(0) # Clear the display
display.text('Hello, World!', 0, 0, 1) # Write text at coordinates (0, 0)
display.text('Pfadi St. Ulrich', 0, 20, 1) # Write text at coordinates (0, 0)
display.text('is the best', 0, 40, 1) # Write text at coordinates (0, 0)
display.show() # Update the display
print('end')
