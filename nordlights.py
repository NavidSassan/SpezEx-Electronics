from machine import Pin, PWM
import time
import urandom
import neopixel

# NeoPixel setup
num_pixels = 10  # 2x5 array
neo_pin = 4
np = neopixel.NeoPixel(Pin(neo_pin), num_pixels)

aurora_speed = 0.8 # seconds
brightness = 0.5  # Brightness level (0.0 to 1.0)

buzzer = PWM(Pin(15), freq=1000, duty=0)
buzzer.duty(0)  # Buzzer off

# Aurora color palette: shades of green, blue, and purple
aurora_colors = [
    (0, 255, 128),  # Light Green
    (0, 128, 255),  # Light Blue
    (128, 0, 255),  # Purple
    (0, 64, 255),   # Blue
    (0, 255, 64),   # Green
    (64, 0, 255)    # Deep Purple
]

def apply_brightness(color, brightness):
    """Apply the brightness scaling to the given RGB color."""
    return tuple(int(c * brightness) for c in color)

def aurora_effect(brightness):
    """Simulate the aurora effect with the given brightness level."""
    offset = 0

    while True:
        for i in range(num_pixels):
            # Cycle through colors and create a moving wave
            color = aurora_colors[(i + offset) % len(aurora_colors)]
            np[i] = apply_brightness(color, brightness)

        np.write()

        # Move the wave forward
        offset = (offset + 1) % len(aurora_colors)

        time.sleep(aurora_speed)  # Adjust speed of the effect

# Main loop with aurora effect and brightness control
while True:
    aurora_effect(brightness)
