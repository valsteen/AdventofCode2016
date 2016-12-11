import copy
import hashlib
import heapq
from itertools import chain
from itertools import combinations

import sys
from time import time


class Generator(object):
    def __init__(self, type):
        self.type = type


class Chip(object):
    def __init__(self, type):
        self.type = type


class Facility(object):
    def __init__(self, floor_count):
        self.floor_count = floor_count
        self.current_floor = 0
        self.steps = 0
        self.chips_on_floors = [set() for _ in range(floor_count)]
        self.generators_on_floors = [set() for _ in range(floor_count)]
        self.chips_on_elevator = set()
        self.generators_on_elevator = set()

    def chips_are_safe(self):
        for chips, generators in zip(self.chips_on_floors, self.generators_on_floors):
            if generators:
                for chip in chips:
                    chip_protected = any(generator == chip for generator in generators)
                    if not chip_protected and any(generator != chip for generator in generators):
                        return False

        return True

    def win(self):
        return sum(len(self.chips_on_floors[x]) for x in range(self.floor_count - 1)) + sum(
            len(self.generators_on_floors[x]) for x in range(self.floor_count - 1)) == 0

    def elevator_charge(self):
        return len(self.chips_on_elevator) + len(self.generators_on_elevator)

    def elevator_up(self):
        if self.current_floor < self.floor_count - 1 and 0 < self.elevator_charge() <= 2:
            new_factory = self.copy()
            new_factory.current_floor += 1
            for chip in new_factory.chips_on_elevator:
                new_factory.chips_on_floors[new_factory.current_floor - 1].remove(chip)
                new_factory.chips_on_floors[new_factory.current_floor].add(chip)
            for generator in new_factory.generators_on_elevator:
                new_factory.generators_on_floors[new_factory.current_floor - 1].remove(generator)
                new_factory.generators_on_floors[new_factory.current_floor].add(generator)
            new_factory.steps += 1
            if new_factory.chips_are_safe():
                return new_factory

    def elevator_down(self):
        if self.current_floor > 0 and 0 < self.elevator_charge() <= 2:
            new_factory = self.copy()
            new_factory.current_floor -= 1
            for chip in new_factory.chips_on_elevator:
                new_factory.chips_on_floors[new_factory.current_floor + 1].remove(chip)
                new_factory.chips_on_floors[new_factory.current_floor].add(chip)
            for generator in new_factory.generators_on_elevator:
                new_factory.generators_on_floors[new_factory.current_floor + 1].remove(generator)
                new_factory.generators_on_floors[new_factory.current_floor].add(generator)
            new_factory.steps += 1
            if new_factory.chips_are_safe():
                return new_factory

    def elevator_combinations(self):
        for chips_combination in chain(*(combinations(self.chips_on_floors[self.current_floor], x) for x in range(3))):
            for generator_combination in chain(
                    *(combinations(self.generators_on_floors[self.current_floor], x) for x in range(3))):
                new_factory = self.copy()
                new_factory.chips_on_elevator = chips_combination
                new_factory.generators_on_elevator = generator_combination

                up_factory = new_factory.elevator_up()
                if up_factory:
                    yield up_factory
                down_factory = new_factory.elevator_down()
                if down_factory:
                    yield down_factory

    @property
    def occupied_floors_count(self):
        return sum(1 if chips or generators else 0 for chips, generators in zip(self.chips_on_floors, self.generators_on_floors))

    def __cmp__(self, other):
        return cmp(self.steps, other.steps) or cmp(self.occupied_floors_count, other.occupied_floors_count) or cmp(hash(self), hash(other))

    def __repr__(self):
        return "{}".format(self.steps)

    def __hash__(self):
        if not hasattr(self, '_hash'):
            res = ""
            for item in (
                    'floor_count', 'current_floor', 'chips_on_floors', 'generators_on_floors'
            ):
                res += "{}={}".format(item, getattr(self, item))

            m = hashlib.md5()
            m.update(res)
            digest = m.hexdigest()
            self._hash = int(digest, 16)
        return self._hash

    def copy(self):
        new_facility = Facility(self.floor_count)
        new_facility.floor_count = self.floor_count
        new_facility.current_floor = self.current_floor
        new_facility.steps = self.steps
        new_facility.chips_on_floors = [set(_) for _ in self.chips_on_floors]
        new_facility.generators_on_floors = [set(_) for _ in self.generators_on_floors]
        new_facility.chips_on_elevator = set(self.chips_on_elevator)
        new_facility.generators_on_elevator = set(self.generators_on_elevator)

        return new_facility


def test_chips_are_safe():
    facility = Facility(4)
    assert facility.win()
    facility.chips_on_floors[1].add("L")
    assert not facility.win()
    assert facility.chips_are_safe()
    facility.generators_on_floors[1].add("L")
    assert facility.chips_are_safe()
    facility.generators_on_floors[1].add("F")
    assert facility.chips_are_safe()
    facility.generators_on_floors[1].remove("L")
    assert not facility.chips_are_safe()


test_chips_are_safe()

facility = Facility(4)
facility.chips_on_floors[0] = {'H', 'L'}
facility.generators_on_floors[1] = {'H'}
facility.generators_on_floors[2] = {'L'}

queue = [facility]

seen = set()

while True:
    facility = heapq.heappop(queue)
    if facility.win():
        print facility.steps
        break
    for new_facility in facility.elevator_combinations():
        if new_facility not in seen:
            seen.add(new_facility)
            heapq.heappush(queue, new_facility)

facility = Facility(4)
facility.generators_on_floors[0] = {'Pr'}
facility.chips_on_floors[0] = {'Pr'}

facility.generators_on_floors[1] = {'Co', 'Cu', 'Ru', 'Pl'}
facility.chips_on_floors[2] = {'Co', 'Cu', 'Ru', 'Pl'}

queue = [facility]

seen = {hash(facility)}

prev = time()

while True:
    facility = heapq.heappop(queue)

    now = time()
    if now - prev > 10:
        print "at step", facility.steps
        prev = now

    if facility.win():
        print facility.steps
        break
    for new_facility in facility.elevator_combinations():
        if hash(new_facility) not in seen:
            # it seems keeping hashes instead of objects gives a nice performance boost
            seen.add(hash(new_facility))
            heapq.heappush(queue, new_facility)
