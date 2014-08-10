#! /usr/bin/python3.4

"""
Core functionality. Separated from usage by web, cli etc interfaces.
"""

from collections import namedtuple
from random import choice, randint
from time import sleep

Coord = namedtuple('Coord', ('x', 'y'))
Vector = namedtuple('Vector', ('dx', 'dy')) # taken with origin at top left as 0,0

sizexy = 8
coordsnumb = sizexy / 2

DNE = "Did Not Emerge"
MOVE_UP = Vector(0, -1)
MOVE_DOWN = Vector(0, 1)
MOVE_LEFT = Vector(-1, 0)
MOVE_RIGHT = Vector(1, 0)

def get_coordinates():
    """
    This generates 4 unique coordinates from square grid of sizexy.
    
    Essentially working from an 8x8 array. As coordinates are selected, they 
    are removed from array which prevents possibility of repeats.
    """
    coordinates = []
    possible_y = {}
    i = 0
    while i < sizexy:
        i += 1
        possible_y[i] = list(range(1, sizexy))
    i = 0
    while i < coordsnumb:
        i += 1
        x = randint(1, sizexy)
        y = choice(possible_y[x])
        possible_y[x].remove(y)
        coordinates.append(Coord(x, y))
    return coordinates


class BlackBox(object):
    """
    This is the Black Box game.
    """
    def __init__(self, coordinates):
        """
        This contains all the components of the black box.
        """
        self.coordinates = coordinates
    
    def new_ray(self, entry):
        """
        Receives incoming ray number, sets initial direction and position, and 
        returns outgoing ray number.
        
        Processed in one-move steps in which position and direction may be 
        reset. Thus the loop. E.g. we might get None back several times before 
        we hit something or exit.
        """
        # Set initial direction and position. Always a square.
        if 1 <= entry <= sizexy:
            self.direction = MOVE_UP
            self.pos = Coord(entry, sizexy + 1)
        elif sizexy + 1 <= entry <= sizexy * 2:
            self.direction = MOVE_LEFT
            self.pos = Coord(sizexy + 1, sizexy * 2 + 1 - entry)
        elif sizexy * 2 + 1 <= entry <= sizexy * 3:
            self.direction = MOVE_DOWN
            self.pos = Coord(sizexy * 3 + 1 - entry, 0)
        elif sizexy * 3 + 1 <= entry <= sizexy * 4:
            self.direction = MOVE_RIGHT
            self.pos = Coord(0, entry - sizexy * 3)
        else:
            raise Exception("Unexpected entry value: {}".format(entry))
        outgoing = None
        while True:
            contacted = self.check_and_reset() # resetting means the result of the check will change each loop
            if contacted == DNE:
                outgoing = contacted
                break
            elif isinstance(contacted, Coord):
                outgoing = abs(self.coords_to_numb(contacted))
                break
            elif contacted is None:
                continue
            else:
                raise TypeError("Unexpected value of contacted "
                    "received: {}".format(contacted))
        return outgoing
    
    def check_and_reset(self):
        """
        This checks to see if the ray has intercepted a point. Check each of 
        the 4 coordinates separately.
        
        Resets position and direction as required ready for next step.
        
        Returns DNE if it does not emerge.
        """
        orig_dir = Vector(self.direction.dx, self.direction.dy)
        corner_hits = 0
        next_spot = Coord(self.pos.x + self.direction.dx, 
            self.pos.y + self.direction.dy)
        for coordinate in self.coordinates:
            if coordinate == next_spot:
                return DNE # Did not emerge
            elif orig_dir.dx: # If it moves in the x direction.
                if coordinate == Coord(next_spot.x, next_spot.y - 1): # If above
                    self.direction = MOVE_DOWN
                    corner_hits += 1
                    if (self.pos.x in (0, sizexy + 1) or self.pos.y in
                        (0, sizexy + 1)):
                        return self.pos
                elif coordinate == Coord(next_spot.x, next_spot.y + 1): # If below
                    self.direction = MOVE_UP
                    corner_hits += 1
                    if (self.pos.x in (0, sizexy + 1) or self.pos.y in
                        (0, sizexy + 1)):
                        return self.pos
            elif orig_dir.dy: # If it moves in the y direction.
                if coordinate == Coord(next_spot.x - 1, next_spot.y): # If left
                    self.direction = MOVE_RIGHT
                    corner_hits += 1
                    if (self.pos.x in (0, sizexy + 1) or self.pos.y in
                        (0, sizexy + 1)):
                        return self.pos
                elif coordinate == Coord(next_spot.x + 1, next_spot.y): # If right
                    self.direction = MOVE_LEFT
                    corner_hits += 1
                    if (self.pos.x in (0, sizexy + 1) or self.pos.y in
                        (0, sizexy + 1)):
                        return self.pos
        if corner_hits > 1:
            self.direction = Vector(orig_dir.dx * -1, orig_dir.dy * -1)
        next_spot = Coord(self.pos.x + self.direction.dx, 
            self.pos.y + self.direction.dy)
        self.pos = next_spot
        if self.pos.x in (0, sizexy + 1) or self.pos.y in (0, sizexy + 1):
            return self.pos
    
    def coords_to_numb(self, contact):
        """
        This converts the coordinates into the number position.
        """
        numb = None
        if contact.y == sizexy + 1:
            numb = contact.x
        elif contact.x == sizexy + 1:
            numb = 2 * sizexy + 1 - contact.y
        elif contact.y == 0:
            numb = sizexy * 3 + 1 - contact.x
        elif contact.x == 0:
            numb = contact.y + sizexy * 3
        if numb is None:
            raise Exception("Non-edge coordinate received. "
                "Orig coord x: {}, y: {}".format(contact.x, contact.y))
        return numb

if __name__ == '__main__':
    g = get_coordinates()
    bb = BlackBox(g)
    while True:
        number = input("Enter your number: ")
        if not number:
            break
        try:
            number = int(number)
        except ValueError:
            print("Pick a number between 1 and %d." % sizexy * 4)
            continue
        if number < 1 or number > sizexy * 4:
            print("Pick a number between 1 and %d." % sizexy * 4)
            continue
        print("%d goes to %s." % (number, bb.new_ray(number)))
    print("The coordinates were:")
    for coordinates in g:
        sleep(1)
        print(coordinates)
