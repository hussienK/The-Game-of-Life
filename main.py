import random
from colorama import Fore, init, Back, Style
from time import sleep
import os
init()


def clear_screen():
    # Check if the platform is Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        # For other platforms (like Unix), use the 'clear' command
        os.system('clear')

def load_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        exit()


class Board():
    width = 0
    height = 0
    board_state = None

    def __init__(self, link):
        loaded_text = load_text_from_file(link)
        self.get_dim(loaded_text)
        self.dead_state(self.width, self.height)
        self.create_intial_state(loaded_text)
        print(self.width)
        print(self.height)
        self.run_forever()

    #initialize board to zeros
    def dead_state(self, width, height):
        self.board_state = [[0 for _ in range(width)] for _ in range(height)]

    #fill randomly
    def random_state(self):
        random_n = 0
        for y in range(self.height):
            for x in range(self.width):
                random_n = random.random()
                if (random_n < 0.5):
                    self.board_state[y][x] = 1
        
    #render to screen based on color
    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if (self.board_state[y][x] == 1):
                    print(Back.BLACK + Style.BRIGHT + "  " + Style.RESET_ALL, end="")
                else:
                    print(Back.WHITE + Style.BRIGHT + "  " + Style.RESET_ALL, end="")
            print()

    def next_board_state(self):
        prev_board_state = self.board_state
        width = self.width
        height = self.height

        #does all the checking on the current board
        next_state = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                counter = 0
                if (x > 0):
                    if (prev_board_state[y][x-1] == 1):
                        counter += 1
                    if (y > 0):
                        if (prev_board_state[y-1][x-1] == 1):
                            counter += 1
                    if (y < height - 1):
                        if (prev_board_state[y+1][x-1] == 1):
                            counter += 1
                if (x < width - 1):
                    if (prev_board_state[y][x+1] == 1):
                        counter += 1
                    if (y > 0):
                        if (prev_board_state[y-1][x+1] == 1):
                            counter += 1
                    if (y < height - 1):
                        if (prev_board_state[y+1][x+1] == 1):
                            counter += 1
                if (y > 0):
                    if (prev_board_state[y-1][x] == 1):
                        counter += 1
                if (y <height - 1):
                    if (prev_board_state[y+1][x] == 1):
                        counter += 1

                #creates next state based on old state
                if (prev_board_state[y][x] == 1):
                    if counter == 0 or counter == 1:
                        next_state[y][x] = 0
                    elif counter == 2 or counter == 3:
                        next_state[y][x] = 1
                    elif counter > 3:
                        next_state[y][x] = 0
                elif (prev_board_state[y][x] == 0):
                    if counter == 3:
                        next_state[y][x] = 1
        return next_state

    def run_forever(self):
        while True:
            self.render()
            self.board_state = self.next_board_state()
            sleep(0.05)
            clear_screen()

    #handles file loading
    def get_dim(self, loaded_text):
        #get the width
        for char in loaded_text:
            if (char == '\0' or char == '\n'):
                break
            self.width = self.width + 1

        loaded_text = loaded_text.replace("\n", "")
        if (len(loaded_text) % self.width != 0):
            print("Error in format of file")
            exit()
        #get the height
        self.height = int(len(loaded_text) / self.width)

    #loads the text into a board
    def create_intial_state(self, loaded_text):
        loaded_text = loaded_text.replace("\n", "")
        i = 0
        for y in range(self.height):
            for x in range(self.width):
                self.board_state[y][x] = int(loaded_text[i])
                i += 1


i = input("Enter a link for the data: ")
board = Board(i)