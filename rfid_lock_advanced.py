# https://electropeak.com/learn/interfacing-rdm6300-125khz-rfid-reader-module-with-arduino/

import time

import machine
from machine import Pin, SoftI2C
import ssd1306


def read_card(uart):
    header = 0x02
    stop_byte = 0x03
    if uart.any():
        data = uart.read()
        # print(f'data: {hex(data)}')
        # print(f'length: {len(data)}')
        # print(f'header: {hex(data[0])}')
        # print(f'stop: {hex(data[13])}')
        # print(f'decoded: {data[1:11][2:].decode("ascii")}')

        # for i, char in enumerate(data):
        #     print(f'\t{i}: {hex(char)}')

        packet = data[:14]

        # check for the packet header
        if packet[0] != header:
            print("WARNING: RFID packet header is invalid.")
            return False

        # check for the packet stop byte
        if packet[-1] != stop_byte:
            print("WARNING: RFID packet stop byte is invalid.")
            return False

        card_data = packet[1:11]  # raw bytes of the card data
        card_id = card_data[2:].decode('ascii')

        # convert hex to decimal
        return(int(card_id, 16))


i2c = SoftI2C(sda=Pin(25), scl=Pin(33))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

uart = machine.UART(1, baudrate=9600, timeout=2, timeout_char=10, tx=19, rx=27)
uart.init(9600)

btn_input = Pin(26, Pin.IN, Pin.PULL_UP)
btn_led = Pin(32, Pin.OUT)

# List of card IDs for unlocking
card_ids = [
    8202175, # 0: blue
    12906581, # 1: green
    13012325, # 2: grey
    6008435, # 3: yellow
]

seen_card_ids = []
current_card_index = 0


# Level 1
while True:
    print(f'current_card_index: {current_card_index}')
    display.fill(0)
    display.text('Level 1', 0, 0, 1)
    display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
    display.show()

    read_card_id = read_card(uart)
    correct_card_id = card_ids[current_card_index]

    # print(f'read_card_id: {read_card_id}')

    if read_card_id is not None:
        # blink button LED
        btn_led.on()
        time.sleep(0.2)
        btn_led.off()

        if read_card_id == correct_card_id:
            print('correct')

            current_card_index += 1
            seen_card_ids.append(read_card_id)

            if current_card_index == 4:
                print('OPEN')
                break

        elif read_card_id and read_card_id not in seen_card_ids:
            print('wrong')
            print(f'\tread_card_id: {read_card_id}')
            print(f'\tcorrect_card_id: {correct_card_id}')

            display.fill(0)
            display.text('Level 1', 0, 0, 1)
            display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
            display.text('WRONG!', 0, 40, 1)
            display.show()
            time.sleep(0.5)

            # reset
            current_card_index = 0
            seen_card_ids = []

    time.sleep(0.2)

display.fill(0)
display.text('Level 1', 0, 0, 1)
display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
display.show()

for _ in range(10):
    btn_led.on()
    time.sleep(0.2)
    btn_led.off()
    time.sleep(0.2)

display.fill(0)
display.text('Level 1', 0, 0, 1)
display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
display.text('SOLVED!', 0, 40, 1)
display.show()

time.sleep(2)


# Level 2
display.fill(0)
display.text('Level 2', 0, 0, 1)
display.text('???', 0, 20, 1)
display.show()
while True:
    pass

# new pinout
# 25 display sda
# 26 btn input
# 27 rfid
# 32 btn led
# 33 display scl
