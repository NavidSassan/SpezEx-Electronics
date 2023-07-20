# https://www.coderdojotc.org/micropython/sound/03-play-three-tones/

import time
from machine import Pin, PWM


# lower right corner with USB connector on top
SPEAKER_PIN = 32

# create a Pulse Width Modulation Object on this pin
speaker = PWM(Pin(SPEAKER_PIN))

speaker.duty_u16(1000)
speaker.freq(300) # 1 Kilohertz
time.sleep(.5) # wait a 1/4 second
speaker.duty_u16(0)
time.sleep(.25)

speaker.duty_u16(1000)
speaker.freq(800)
time.sleep(.5)
speaker.duty_u16(0)
time.sleep(.25)

speaker.duty_u16(1000)
speaker.freq(400)
time.sleep(.5)

# turn off the PWM 
speaker.duty_u16(0)
