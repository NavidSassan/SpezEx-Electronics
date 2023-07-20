# https://electropeak.com/learn/interfacing-rdm6300-125khz-rfid-reader-module-with-arduino/

import ssd1306
import time
from machine import Pin, SoftI2C, UART


# pinout:
# 25 display sda
# 26 btn input
# 27 rfid
# 32 btn led
# 33 display scl


class Puzzle():

    def __init__(self):
        i2c = SoftI2C(sda=Pin(25), scl=Pin(33))
        self.display = ssd1306.SSD1306_I2C(128, 64, i2c)

        self.uart = UART(1, baudrate=9600, timeout=2, timeout_char=10, tx=19, rx=27)
        self.uart.init(9600)

        self.btn_input = Pin(26, Pin.IN, Pin.PULL_UP)
        self.btn_led = Pin(32, Pin.OUT)


    def read_card(self):
        header = 0x02
        stop_byte = 0x03
        if self.uart.any():
            data = self.uart.read()
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


    def run(self):
        self.level1()
        self.level2()


    def level1(self):
        # List of card IDs for unlocking
        correct_card_ids = [
            8202175, # 0: blue
            12906581, # 1: green
            13012325, # 2: grey
            6008435, # 3: yellow
        ]

        # repeat until solved, then exit the method
        while True:
            seen_card_ids = []
            current_card_index = 0

            # wait until 4 cards are read, then break and check the card IDs
            while True:
                print(f'current_card_index: {current_card_index}')
                self.display.fill(0)
                self.display.text('Level 1', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                self.display.show()

                read_card_id = self.read_card()

                if read_card_id is not None and read_card_id not in seen_card_ids:
                    # blink button LED
                    self.btn_led.on()
                    time.sleep(0.2)
                    self.btn_led.off()

                    current_card_index += 1
                    seen_card_ids.append(read_card_id)

                    if current_card_index == 4:
                        print('got 4 cards, wait for button press now')
                        break

                time.sleep(0.2)

            self.display.fill(0)
            self.display.text('Level 1', 0, 0, 1)
            self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
            self.display.show()

            # wait for button press
            while self.btn_input.value() == 1:
                self.btn_led.on()
                time.sleep(0.2)
                self.btn_led.off()
                time.sleep(0.2)

            if seen_card_ids == correct_card_ids:
                self.display.fill(0)
                self.display.text('Level 1', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                self.display.text('SOLVED!', 0, 40, 1)
                self.display.show()
                time.sleep(2) # sleep so one can read the messages on the screen
                return # exit the function

            else:
                self.display.fill(0)
                self.display.text('Level 1', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                self.display.text('WRONG!', 0, 40, 1)
                self.display.show()
                time.sleep(2) # sleep so one can read the messages on the screen
                print('wrong, therefore repeat')


    def level2(self):
        self.display.fill(0)
        self.display.text('Level 2', 0, 0, 1)
        self.display.text('????', 0, 20, 1)
        self.display.show()

        # while True:
        #     pass

if __name__ == '__main__':
    puzzle = Puzzle()
    puzzle.run()
