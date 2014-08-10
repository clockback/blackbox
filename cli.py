#! /usr/bin/python3.4

"""
CLI interface to game.
"""

from time import sleep

import core

def play(side_len=8):
    coordinates = core.get_coordinates(side_len)
    bb = core.BlackBox(coordinates, side_len)
    while True:
        number = input("Enter your number: ")
        if not number:
            break
        try:
            number = int(number)
        except ValueError:
            print("Pick a number between 1 and {}.".format(side_len * 4))
            continue
        if number < 1 or number > side_len * 4:
            print("Pick a number between 1 and {}.".format(side_len * 4))
            continue
        print("{} goes to {}.".format(number, bb.exit_ray(number)))
    print("The coordinates were:")
    for coordinate in coordinates:
        sleep(1)
        print(coordinate)

if __name__ == '__main__':
    play()
