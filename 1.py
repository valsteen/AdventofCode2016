import re

class Advent1(object):
    DIRECTIONS = "NESW"
    x = 0
    y = 0
    direction = "N"

    def turn(self, s):
        current = self.DIRECTIONS.index(self.direction)
        if s == "L":
            current -= 1
            if current < 0:
                current += len(self.DIRECTIONS)
            self.direction = self.DIRECTIONS[current]
        elif s == "R":
            current = (current + 1) % len(self.DIRECTIONS)
            self.direction = self.DIRECTIONS[current]
        else:
            raise Exception("EPIC FAIL")

    def forward(self, l):
        if self.direction == "N":
            self.y -= l
        elif self.direction == "E":
            self.x += l
        elif self.direction == "S":
            self.y += l
        elif self.direction == "W":
            self.x -= l
        else:
            raise Exception("EPIC FAIL")

    def __init__(self, i):
        parts = re.split(r"[, ]+", i)
        for part in parts:
            d = part[0]
            l = int(part[1:])

            self.turn(d)
            self.forward(l)

        print abs(self.x) + abs(self.y)


Advent1("R2, L3")
Advent1("R2, R2, R2")
Advent1("R5, L5, R5, R3")
Advent1("L5, R1, L5, L1, R5, R1, R1, L4, L1, L3, R2, R4, L4, L1, L1, R2, R4, R3, L1, R4, L4, L5, L4, R4, L5, R1, R5, L2, R1, R3, L2, L4, L4, R1, L192, R5, R1, R4, L5, L4, R5, L1, L1, R48, R5, R5, L2, R4, R4, R1, R3, L1, L4, L5, R1, L4, L2, L5, R5, L2, R74, R4, L1, R188, R5, L4, L2, R5, R2, L4, R4, R3, R3, R2, R1, L3, L2, L5, L5, L2, L1, R1, R5, R4, L3, R5, L1, L3, R4, L1, L3, L2, R1, R3, R2, R5, L3, L1, L1, R5, L4, L5, R5, R2, L5, R2, L1, L5, L3, L5, L5, L1, R1, L4, L3, L1, R2, R5, L1, L3, R4, R5, L4, L1, R5, L1, R5, R5, R5, R2, R1, R2, L5, L5, L5, R4, L5, L4, L4, R5, L2, R1, R5, L1, L5, R4, L3, R4, L2, R3, R3, R3, L2, L2, L2, L1, L4, R3, L4, L2, R2, R5, L1, R2")