import re


class Advent8(object):
    def __init__(self, width=50, height=6):
        self.width = width
        self.height = height
        self.matrix = [[False for _ in xrange(width)] for _ in range(height)]

    def dispatch(self, line):
        rect_match = re.match(r"rect (?P<width>[0-9]+)x(?P<height>[0-9]+)$", line)
        if rect_match:
            self.rect(int(rect_match.group("width")), int(rect_match.group("height")))
            return

        rotate_match = re.match(r"rotate (?P<what>row|column) .=(?P<y>[0-9]+) by (?P<by>[0-9]+)$", line)
        if rotate_match:
            if rotate_match.group("what") == "row":
                self.shift_row(int(rotate_match.group("y")), int(rotate_match.group("by")))
                return
            elif rotate_match.group("what") == "column":
                self.shift_column(int(rotate_match.group("y")), int(rotate_match.group("by")))
                return
        raise Exception("Unknown instruction %s" % line)

    def rect(self, width, height):
        for x in xrange(width):
            for y in xrange(height):
                self.matrix[y][x] = True

    def shift_row(self, y, by):
        self.matrix[y] = self.matrix[y][-by:] + self.matrix[y][:-by]

    def shift_column(self, x, by):
        self.matrix = [list(_) for _ in zip(*self.matrix)]
        self.shift_row(x, by)
        self.matrix = [list(_) for _ in zip(*self.matrix)]

    def count(self):
        return sum(1 if c else 0 for line in self.matrix for c in line)

    def __str__(self):
        return "-" * self.width + "\n" + "\n".join(
            "".join("#" if cell else "." for cell in line) for line in self.matrix) + "\n" + "-" * self.width


a = Advent8(7, 3)
seq = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

for line in seq.split("\n"):
    a.dispatch(line)
    print a

print a.count()

a = Advent8()
seq = """rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 6
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 5
rect 2x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 4
rect 1x1
rotate row y=0 by 3
rect 2x1
rotate row y=0 by 7
rect 3x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 3
rect 1x2
rotate row y=1 by 13
rotate column x=0 by 1
rect 2x1
rotate row y=0 by 5
rotate column x=0 by 1
rect 3x1
rotate row y=0 by 18
rotate column x=13 by 1
rotate column x=7 by 2
rotate column x=2 by 3
rotate column x=0 by 1
rect 17x1
rotate row y=3 by 13
rotate row y=1 by 37
rotate row y=0 by 11
rotate column x=7 by 1
rotate column x=6 by 1
rotate column x=4 by 1
rotate column x=0 by 1
rect 10x1
rotate row y=2 by 37
rotate column x=19 by 2
rotate column x=9 by 2
rotate row y=3 by 5
rotate row y=2 by 1
rotate row y=1 by 4
rotate row y=0 by 4
rect 1x4
rotate column x=25 by 3
rotate row y=3 by 5
rotate row y=2 by 2
rotate row y=1 by 1
rotate row y=0 by 1
rect 1x5
rotate row y=2 by 10
rotate column x=39 by 1
rotate column x=35 by 1
rotate column x=29 by 1
rotate column x=19 by 1
rotate column x=7 by 2
rotate row y=4 by 22
rotate row y=3 by 5
rotate row y=1 by 21
rotate row y=0 by 10
rotate column x=2 by 2
rotate column x=0 by 2
rect 4x2
rotate column x=46 by 2
rotate column x=44 by 2
rotate column x=42 by 1
rotate column x=41 by 1
rotate column x=40 by 2
rotate column x=38 by 2
rotate column x=37 by 3
rotate column x=35 by 1
rotate column x=33 by 2
rotate column x=32 by 1
rotate column x=31 by 2
rotate column x=30 by 1
rotate column x=28 by 1
rotate column x=27 by 3
rotate column x=26 by 1
rotate column x=23 by 2
rotate column x=22 by 1
rotate column x=21 by 1
rotate column x=20 by 1
rotate column x=19 by 1
rotate column x=18 by 2
rotate column x=16 by 2
rotate column x=15 by 1
rotate column x=13 by 1
rotate column x=12 by 1
rotate column x=11 by 1
rotate column x=10 by 1
rotate column x=7 by 1
rotate column x=6 by 1
rotate column x=5 by 1
rotate column x=3 by 2
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 49x1
rotate row y=2 by 34
rotate column x=44 by 1
rotate column x=40 by 2
rotate column x=39 by 1
rotate column x=35 by 4
rotate column x=34 by 1
rotate column x=30 by 4
rotate column x=29 by 1
rotate column x=24 by 1
rotate column x=15 by 4
rotate column x=14 by 1
rotate column x=13 by 3
rotate column x=10 by 4
rotate column x=9 by 1
rotate column x=5 by 4
rotate column x=4 by 3
rotate row y=5 by 20
rotate row y=4 by 20
rotate row y=3 by 48
rotate row y=2 by 20
rotate row y=1 by 41
rotate column x=47 by 5
rotate column x=46 by 5
rotate column x=45 by 4
rotate column x=43 by 5
rotate column x=41 by 5
rotate column x=33 by 1
rotate column x=32 by 3
rotate column x=23 by 5
rotate column x=22 by 1
rotate column x=21 by 2
rotate column x=18 by 2
rotate column x=17 by 3
rotate column x=16 by 2
rotate column x=13 by 5
rotate column x=12 by 5
rotate column x=11 by 5
rotate column x=3 by 5
rotate column x=2 by 5
rotate column x=1 by 5"""

for line in seq.split("\n"):
    a.dispatch(line)
    print a

print a.count()
