import network
import socket
from machine import Pin, PWM
import time
import _thread
import urandom
import neopixel

# Set up the ESP32 as an Access Point
ssid = 'ESP32-AP'
password = 'ghostbox'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())

# NeoPixel setup
num_pixels = 10  # 2x5 array
pin = 22
np = neopixel.NeoPixel(Pin(pin), num_pixels)

# Buzzer setup
buzzer = PWM(Pin(21), freq=1000, duty=0)

blinking = False
crazy_mode = False
speed = 500  # Default speed in milliseconds

def random_blink_beep():
    global blinking, speed, crazy_mode
    while True:
        if blinking:
            if crazy_mode:
                # Crazy mode: rapid random colors and patterns
                for _ in range(num_pixels):
                    np[_] = (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
                np.write()
                buzzer.duty(512)  # Buzzer on
                time.sleep(urandom.uniform(0.05, 0.2))
                buzzer.duty(0)  # Buzzer off
            else:
                # Randomly light up some NeoPixels
                np.fill((0, 0, 0))  # Turn off all pixels first
                for _ in range(urandom.getrandbits(3) + 1):  # Random number of pixels to light up
                    i = urandom.getrandbits(3) % num_pixels
                    np[i] = (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
                np.write()
                buzzer.duty(512)  # Buzzer on
                time.sleep(urandom.uniform(0.1, speed / 1000.0))
                np.fill((0, 0, 0))
                np.write()
                buzzer.duty(0)  # Buzzer off
                time.sleep(urandom.uniform(0.1, speed / 1000.0))
        else:
            np.fill((0, 0, 0))
            np.write()
            buzzer.duty(0)  # Buzzer off
            time.sleep(0.1)

_thread.start_new_thread(random_blink_beep, ())

# HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Ghost Detector</title>
    <style>
        button { font-size: 20px; margin: 10px; padding: 10px; }
        input[type=range] { width: 300px; }
    </style>
</head>
<body>
    <h1>ESP32 Ghost Detector</h1>
    <button onclick="fetch('/start')">Start</button>
    <button onclick="fetch('/stop')">Stop</button>
    <button onclick="fetch('/crazy')">Crazy Mode</button>
    <p>Speed: <span id="speedValue">500</span> ms</p>
    <input type="range" min="100" max="2000" value="500" id="speedRange" oninput="updateSpeed(this.value)">
    <script>
        function updateSpeed(value) {
            document.getElementById('speedValue').innerText = value;
            fetch('/speed/' + value);
        }
    </script>
</body>
</html>
"""

# Create a socket and listen for connections
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Handle connections
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    request = cl_file.readline().decode('utf-8')
    print(request)

    if '/start' in request:
        blinking = True
        crazy_mode = False
    if '/stop' in request:
        blinking = False
        crazy_mode = False
    if '/crazy' in request:
        blinking = True
        crazy_mode = True
    if '/speed/' in request:
        speed = int(request.split('/speed/')[1].split()[0])

    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    cl.send('HTTP/1.1 200 OK\r\n')
    cl.send('Content-Type: text/html\r\n')
    cl.send('Connection: close\r\n\r\n')
    cl.sendall(html)
    cl.close()
