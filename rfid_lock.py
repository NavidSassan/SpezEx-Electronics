import time

import machine
from machine import Pin


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


uart = machine.UART(1, baudrate=9600, timeout=2, timeout_char=10, tx=19, rx=18)
uart.init(9600)


leds = [
    Pin(27, Pin.OUT, value=0), # 0
    Pin(14, Pin.OUT, value=0), # 1
    Pin(12, Pin.OUT, value=0), # 2
    Pin(13, Pin.OUT, value=0), # 3
]

# List of card IDs for unlocking
card_ids = [
    8202175, # 0: blue
    12906581, # 1: green
    13012325, # 2: grey
    6008435, # 3: yellow
]

seen_card_ids = []
current_card_index = 0

while True:
    print(f'current_card_index: {current_card_index}')
    # turn on the current LED
    for led in leds:
        led.off()
    leds[current_card_index].on()

    read_card_id = read_card(uart)
    correct_card_id = card_ids[current_card_index]

    if read_card_id == correct_card_id:
        print('correct')

        if current_card_index == 3:
            print('OPEN')

            while True:
                for led in leds:
                    led.on()
                time.sleep(0.2)
                for led in leds:
                    led.off()
                time.sleep(0.2)

        current_card_index += 1
        seen_card_ids.append(read_card_id)


    elif read_card_id and read_card_id not in seen_card_ids:
        print('wrong')
        print(f'\tread_card_id: {read_card_id}')
        print(f'\tcorrect_card_id: {correct_card_id}')

        # reset
        current_card_index = 0
        seen_card_ids = []



    time.sleep(0.2)
