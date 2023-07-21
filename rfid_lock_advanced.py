# https://electropeak.com/learn/interfacing-rdm6300-125khz-rfid-reader-module-with-arduino/
# https://docs.micropython.org/en/latest/library/framebuf.html

import functools
import random
import time
from array import array

import ssd1306
from machine import UART, Pin, SoftI2C

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

        self.card2color = {
            12906581: 'Grün',
            13012325: 'Grau',
            1338145: 'Schwarz',
            1484985: 'Gelb',
            15798243: 'Orange',
            6008435: 'Gelb',
            7888819: 'Blau',
            8202175: 'Blau',
            8644032: 'Rot',
            8736126: 'Rot',
        }

        self.card2sol_level1 = {
            #     puzzle1,  puzzle2,   # puzzle1,  puzzle2,
            'A': [13012325, 15798243], # grey,     orange
            'B': [6008435,  1338145],  # yellow,   black
            'C': [8644032,  1484985],  # red,      yellow
            'D': [8202175,  8736126],  # blue,     red
            'E': [12906581, 7888819],  # green,    blue
        }

        self.solution_level1 = [
            'E',
            'A',
            'D',
            'B',
        ]

        self.card2sol_level2 = {
            #     puzzle1,  puzzle2,   # puzzle1,  puzzle2,
            'A': [12906581, 7888819],  # green,    blue
            'B': [13012325, 15798243], # grey,     orange
            'C': [6008435,  1338145],  # yellow,   black
            'D': [8202175,  8736126],  # blue,     red
            'E': [8644032,  1484985],  # red,      yellow
        }

        self.riddles_level2 = [
            {
                'name': 'square',
                'display_functions': [
                    functools.partial(self.display.rect, 50, 30, 30, 30, 1, True),
                ],
                'solution': [
                    'A',
                    'D',
                    'E',
                    'C',
                ],
            },
            {
                'name': 'square-circle',
                'display_functions': [
                    functools.partial(self.display.rect, 30, 30, 30, 30, 1, True),
                    functools.partial(self.display.ellipse, 80, 45, 15, 15, 1, True),
                ],
                'solution': [
                    'D',
                    'B',
                    'C',
                    'E',
                ],
            },
            {
                'name': 'square-triangle',
                'display_functions': [
                    functools.partial(self.display.rect, 25, 30, 30, 30, 1, True),
                    functools.partial(self.display.poly, 65, 9, array('h', [0, 50, 15, 30, 30, 50]), 1, True),
                ],
                'solution': [
                    'E',
                    'A',
                    'B',
                    'C',
                ],
            },
            {
                'name': 'circle',
                'display_functions': [
                    functools.partial(self.display.ellipse, 60, 40, 15, 15, 1, True),
                ],
                'solution': [
                    'C',
                    'B',
                    'D',
                    'A',
                ],
            },
            {
                'name': 'circle-square',
                'display_functions': [
                    functools.partial(self.display.ellipse, 40, 45, 15, 15, 1, True),
                    functools.partial(self.display.rect, 60, 30, 30, 30, 1, True),
                ],
                'solution': [
                    'B',
                    'C',
                    'A',
                    'E',
                ],
            },
            {
                'name': 'circle-triangle',
                'display_functions': [
                    functools.partial(self.display.ellipse, 40, 45, 15, 15, 1, True),
                    functools.partial(self.display.poly, 65, 9, array('h', [0, 50, 15, 30, 30, 50]), 1, True),
                ],
                'solution': [
                    'A',
                    'E',
                    'C',
                    'B',
                ],
            },
            {
                'name': 'triangle',
                'display_functions': [
                    functools.partial(self.display.poly, 45, 0, array('h', [0, 50, 15, 30, 30, 50]), 1, True),
                ],
                'solution': [
                    'D',
                    'E',
                    'B',
                    'A',
                ],
            },
            {
                'name': 'triangle-square',
                'display_functions': [
                    functools.partial(self.display.poly, 25, 9, array('h', [0, 50, 15, 30, 30, 50]), 1, True),
                    functools.partial(self.display.rect, 70, 30, 30, 30, 1, True),
                ],
                'solution': [
                    'C',
                    'A',
                    'E',
                    'D',
                ],
            },
            {
                'name': 'triangle-circle',
                'display_functions': [
                    functools.partial(self.display.poly, 25, 9, array('h', [0, 50, 15, 30, 30, 50]), 1, True),
                    functools.partial(self.display.ellipse, 80, 45, 15, 15, 1, True),
                ],
                'solution': [
                    'E',
                    'C',
                    'D',
                    'B',
                ],
            },
        ]


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
            return int(card_id, 16)
        return None


    def check_solution(self, solution, given_cards, card2sol):
        print('check_solution')
        for sol, given_card in zip(solution, given_cards):
            print(f'\tsol: {sol}')
            print(f'\tcard2sol[sol]: {card2sol[sol]} ({", ".join(self.card2color[card] for card in card2sol[sol])})')
            print(f'\tgiven_card: {given_card} ({self.card2color[given_card]})')
            if given_card not in card2sol[sol]:
                print('\tsolution incorrect')
                return False
        print('\tsolution correct')
        return True


    def run(self):
        self.level1()
        self.level2()

        self.display.fill(0)
        self.display.text('Code:', 0, 0, 1)
        self.display.text('1234 oder 1234', 0, 50, 1)
        self.display.show()


    def level1(self):
        # List of card IDs for unlocking
        # repeat until solved, then exit the method
        while True:
            read_card_ids = []
            current_card_index = 0

            # wait until 4 cards are read, then break and check the card IDs
            while True:
                print(f'current_card_index: {current_card_index}')
                self.display.fill(0)
                self.display.text('Level 1', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                self.display.show()

                read_card_id = self.read_card()

                if read_card_id is not None and read_card_id not in read_card_ids:
                    # blink button LED
                    self.btn_led.on()
                    time.sleep(0.2)
                    self.btn_led.off()

                    print(f'read_card_id: {read_card_id} ({self.card2color[read_card_id]})')
                    current_card_index += 1
                    read_card_ids.append(read_card_id)

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

            if self.check_solution(self.solution_level1, read_card_ids, self.card2sol_level1):
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

                # wait until read_card returns None, else we get a wrong first read
                while (temp := self.read_card()) is not None:
                    print(f'temp: {temp}')
                    time.sleep(0.1)


    def level2(self):
        # repeat until solved, then exit the method
        while True:
            current_riddle = random.choice(self.riddles_level2)
            read_card_ids = []
            current_card_index = 0

            # wait until 4 cards are read, then break and check the card IDs
            while True:
                print(f'current_card_index: {current_card_index}')
                self.display.fill(0)
                self.display.text('Level 2', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                for display_function in current_riddle['display_functions']:
                    display_function()
                self.display.show()

                read_card_id = self.read_card()

                if read_card_id is not None and read_card_id not in read_card_ids:
                    # blink button LED
                    self.btn_led.on()
                    time.sleep(0.2)
                    self.btn_led.off()

                    print(f'read_card_id: {read_card_id} ({self.card2color[read_card_id]})')
                    current_card_index += 1
                    read_card_ids.append(read_card_id)

                    if current_card_index == 4:
                        print('got 4 cards, wait for button press now')
                        break

                time.sleep(0.2)

            self.display.fill(0)
            self.display.text('Level 2', 0, 0, 1)
            self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
            for display_function in current_riddle['display_functions']:
                display_function()
            self.display.show()

            # wait for button press
            while self.btn_input.value() == 1:
                self.btn_led.on()
                time.sleep(0.2)
                self.btn_led.off()
                time.sleep(0.2)

            if self.check_solution(current_riddle['solution'], read_card_ids, self.card2sol_level2):
                self.display.fill(0)
                self.display.text('Level 2', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                self.display.text('SOLVED!', 0, 40, 1)
                self.display.show()
                time.sleep(2) # sleep so one can read the messages on the screen
                return # exit the function

            else:
                self.display.fill(0)
                self.display.text('Level 2', 0, 0, 1)
                self.display.text(f'{"X" * current_card_index:?<4}', 0, 20, 1)
                self.display.text('WRONG!', 0, 40, 1)
                self.display.show()
                time.sleep(2) # sleep so one can read the messages on the screen
                print('wrong, therefore repeat')

                # wait until read_card returns None, else we get a wrong first read
                while (temp := self.read_card()) is not None:
                    print(f'temp: {temp}')
                    time.sleep(0.1)


    def print_solutions(self):
        for puzzle_index, puzzle_name in enumerate(['gray', 'black']):
            print(f'# Puzzle {puzzle_index + 1} ({puzzle_name})')

            print('## Level 1')
            for i, sol in enumerate(self.solution_level1):
                card = self.card2sol_level1[sol][puzzle_index]
                print(f'\t{i + 1}: {self.card2color[card]}')
            print()

            print('## Level 2')
            for riddle in self.riddles_level2:
                print(f'### Riddle {riddle["name"]}')
                for i, sol in enumerate(riddle['solution']):
                    card = self.card2sol_level2[sol][puzzle_index]
                    print(f'\t{i + 1}: {self.card2color[card]}')
                print()
            print()


if __name__ == '__main__':
    puzzle = Puzzle()
    puzzle.run()

    # puzzle.print_solutions()

    # while True:
    #     print(puzzle.read_card())
    #     time.sleep(0.2)
