# https://www.coderdojotc.org/micropython/basics/03-potentiometer/
# https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion

from machine import Pin, ADC, PWM
import time

poti = ADC(Pin(4), atten=ADC.ATTN_11DB)
pwm_led = PWM(Pin(2, Pin.OUT))

while True:
    poti_value = poti.read_u16()
    print(f'poti_value: {poti_value}')

    pwm_led.duty_u16(poti_value)

    time.sleep(0.1)
