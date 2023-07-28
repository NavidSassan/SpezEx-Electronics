# https://www.coderdojotc.org/micropython/sound/03-play-three-tones/

import time
from machine import Pin, PWM

speaker = PWM(Pin(32))

speaker.duty_u16(60000)


while True:
    speaker.freq(100)
    time.sleep(1)

    speaker.freq(300)
    time.sleep(1)
