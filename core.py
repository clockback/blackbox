#! /usr/bin/python3.4

"""
Core functionality. Separated from usage by web, cli etc interfaces.
"""

from collections import namedtuple
import json
from random import choice, randint

debug = False

Coord = namedtuple('Coord', ('x', 'y'))
Vector = namedtuple('Vector', ('dx', 'dy')) # taken with origin at top left as 0,0

DNE = "Did Not Emerge"
MOVE_UP = Vector(0, -1)
MOVE_DOWN = Vector(0, 1)
MOVE_LEFT = Vector(-1, 0)
MOVE_RIGHT = Vector(1, 0)

def get_atom_coords(side_len=8):
    """
    This generates the required number of unique coordinates from square grid 
    of side_len.

    Coordinates are 1-based so the top-left corner is (1,1).
    
    Essentially working from an side_len x side_len array. As coordinates are
    selected, they are removed from array which prevents possibility of repeats.
    """
    atom_coords = []
    possible_y = {}
    i = 0
    while i < side_len:
        i += 1
        possible_y[i] = list(range(1, side_len))
    i = 0
    while i < (side_len/2):
        i += 1
        x = randint(1, side_len)
        y = choice(possible_y[x])
        possible_y[x].remove(y)
        atom_coords.append(Coord(x, y))
    return atom_coords

def coords2json(coords):
    """
    coords -- named tuples - need to convert to plain python data structure 
    and then into json string.
    """
    plain_coords = [coord2plain(coord) for coord in coords]
    return json.dumps(plain_coords)

def coord2plain(coord):
    json_coord = [coord.x, coord.y]
    return json_coord

def coords_str2coords(coords_str):
    raw_coords = json.loads(coords_str)
    coords = [Coord(raw_coord[0], raw_coord[1]) 
        for raw_coord in raw_coords]
    return coords

def coords_to_num(side_len, contact):
    """
    This converts the coordinates into the number position.
    """
    num = None
    if contact.y == side_len + 1:
        num = contact.x
    elif contact.x == side_len + 1:
        num = (2 * side_len) + 1 - contact.y
    elif contact.y == 0:
        num = (side_len * 3) + 1 - contact.x
    elif contact.x == 0:
        num = contact.y + (side_len * 3)
    if num is None:
        raise Exception("Non-edge coordinate received. "
            "Orig coord x: {}, y: {}".format(contact.x, contact.y))
    return num

def check_and_reset(side_len, atom_coords, pos, direction):
    """
    This checks to see if the ray has intercepted a point. Check each of 
    the coordinates separately.
    
    Resets position and direction as required ready for next step.
    
    Returns DNE if it does not emerge.
    """
    orig_dir = Vector(direction.dx, direction.dy)
    corner_hits = 0
    next_spot = Coord(pos.x + direction.dx, pos.y + direction.dy)
    for atom_coord in atom_coords:
        if atom_coord == next_spot:
            contact = DNE
            return contact, pos, direction # Did not emerge
        elif orig_dir.dx: # If it moves in the x direction.
            if atom_coord == Coord(next_spot.x, next_spot.y - 1): # If above
                direction = MOVE_DOWN
                corner_hits += 1
                if (pos.x in (0, side_len + 1) or pos.y
                        in (0, side_len + 1)):
                    contact = pos
                    return contact, pos, direction
            elif atom_coord == Coord(next_spot.x, next_spot.y + 1): # If below
                direction = MOVE_UP
                corner_hits += 1
                if (pos.x in (0, side_len + 1) or pos.y in
                    (0, side_len + 1)):
                    contact = pos
                    return contact, pos, direction
        elif orig_dir.dy: # If it moves in the y direction.
            if atom_coord == Coord(next_spot.x - 1, next_spot.y): # If left
                direction = MOVE_RIGHT
                corner_hits += 1
                if (pos.x in (0, side_len + 1) or pos.y in
                        (0, side_len + 1)):
                    contact = pos
                    return contact, pos, direction
            elif atom_coord == Coord(next_spot.x + 1, next_spot.y): # If right
                direction = MOVE_LEFT
                corner_hits += 1
                if (pos.x in (0, side_len + 1) or pos.y in
                        (0, side_len + 1)):
                    contact = pos
                    return contact, pos, direction
    if corner_hits > 1:
        direction = Vector(orig_dir.dx * -1, orig_dir.dy * -1)
    next_spot = Coord(pos.x + direction.dx, pos.y + direction.dy)
    pos = next_spot
    if (pos.x in (0, side_len + 1) 
            or pos.y in (0, side_len + 1)):
        contact = pos
        return contact, pos, direction
    contact = None
    return contact, pos, direction

def exit_ray(side_len, atom_coords, entry):
    """
    Receives incoming ray number, sets initial direction and position, and 
    returns outgoing ray number if possible. Output must be json string.
    
    Processed in one-move steps in which position and direction may be 
    reset. Thus the loop. E.g. we might get None back several times before 
    we hit something or exit.
    """
    if debug:
        print("side_len: {}".format(side_len))
        print("atom_coords: {}".format(atom_coords))
        print("entry: {}".format(entry))
    # Set initial direction and position. Always a square.
    if 1 <= entry <= side_len:
        direction = MOVE_UP
        pos = Coord(entry, side_len + 1)
    elif side_len + 1 <= entry <= side_len * 2:
        direction = MOVE_LEFT
        pos = Coord(side_len + 1, side_len * 2 + 1 - entry)
    elif side_len * 2 + 1 <= entry <= side_len * 3:
        direction = MOVE_DOWN
        pos = Coord(side_len * 3 + 1 - entry, 0)
    elif side_len * 3 + 1 <= entry <= side_len * 4:
        direction = MOVE_RIGHT
        pos = Coord(0, entry - side_len * 3)
    else:
        raise Exception("Unexpected entry value: {}".format(entry))
    outgoing = None
    while True:
        contacted, pos, direction = check_and_reset(side_len, atom_coords, pos,
            direction) # resetting means the result of the check will change each loop
        if contacted == DNE:
            outgoing = contacted
            break
        elif isinstance(contacted, Coord):
            outgoing = abs(coords_to_num(side_len, contacted))
            break
        elif contacted is None:
            continue
        else:
            raise TypeError("Unexpected value of contacted "
                "received: {}".format(contacted))
    return outgoing

if __name__ == "__main__":
    side_len = 8
    atom_coords = [Coord(x=1, y=1), Coord(x=1, y=7), Coord(x=8, y=6), Coord(x=7, y=1)]
    entry = 4
    outgoing = exit_ray(side_len, atom_coords, entry)
    if debug: print("outgoing: {}".format(outgoing))

