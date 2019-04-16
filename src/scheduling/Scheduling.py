# -*- coding: utf-8 -*-

from enum import IntEnum, auto
import random
import copy

class Location(IntEnum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()

class Occupation(IntEnum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()

class TimeRange(object):

    def __init__(self, begin_time, end_time):
        self.begin = begin_time
        self.end = end_time

    def overlappedTo(self, other):
        if(not isinstance(other, TimeRange)):
            return False

        return self.begin >= other.end or self.end <= other.begin

class Matter(object):

    def __init__(self, location, occupation_map, begin_time, end_time):
        self.location = location
        self.occupation_map = occupation_map
        self.time_range = TimeRange(begin_time, end_time)

    def __str__(self):
        return f'matter: {self.time_range.begin} - {self.time_range.end} location: {self.location}'

class Person(object):

    __next_id = None

    def __init__(self, occupation, id = None):
        self.__initialize_id()

        self.occupation = occupation
        if(id is None):
            self.id = self.__next_id[occupation]
            self.__next_id[occupation] += 1
        else:
            self.id = id

        self.assigndTimes = []

    @classmethod
    def __initialize_id(self):
        if(self.__next_id is not None):
            return

        self.__next_id = {}
        for occupation in Occupation:
            self.__next_id[occupation] = 0

    def assignTo(self, matter):
        self.assigndTimes.append(matter.time_range)

    def clone(self):
        return Person(self.occupation, self.id)

#    def judge_overlapp(self):


class Schedule(object):

    matters = None
    persons = None

    @classmethod
    def initialise(cls, matters, persons):
        cls.matters = matters
        cls.persons = persons

    def __init__(self):
        self.__create_person_map()
        self.__create_schedule_list()

    def __create_person_map(self):
        self.person_map = {}
        for occupation in Occupation:
            self.person_map[occupation] = []

        for person in self.persons:
            self.person_map[person.occupation].append(person)

    def __create_schedule_list(self):
        self.list_map = {}
        for occupation in Occupation:
            self.list_map[occupation] = []

            for matter in self.matters:
                assigned_persons = random.sample(self.person_map[occupation], matter.occupation_map[occupation])
                for assigned_person in assigned_persons:
                    assigned_person.assignTo(matter)

                self.list_map[occupation].extend(assigned_persons)

#    def __eval_overlap(self):


    def evaluate(self):
        return self.__eval_overlap()

    def console_out(self):
        iterators = {}
        for occupation in Occupation:
            iterators[occupation] = iter(self.list_map[occupation])

        for matter in self.matters:
            print(matter)

            for occupation in Occupation:
                print(occupation, end=": ")
                for _ in range(matter.occupation_map[occupation]):
                    print(next(iterators[occupation]), end=" ")
                print()

def create_matters():
    matters = []
    locations = [loc for loc in Location]
    person_count = range(3)
    times = [10, 12, 14, 16, 18, 20]

    for _ in range(20):
        location = random.choice(locations)
        occupation_map = {}
        for occupation in Occupation:
            occupation_map[occupation] = random.choice(person_count)
        time = random.sample(times, 2)
        begin_time = min(time)
        end_time = max(time)
        matters.append(Matter(location, occupation_map, begin_time, end_time))

    return matters

def create_persons():
    persons = []

    for occupation in Occupation:
        persons.extend([Person(occupation) for _ in range(20)])

    return persons

def main():
    Schedule.initialise(create_matters(), create_persons())
    schedules = [Schedule() for _ in range(100)]
    for schedule in schedules:
        schedule.console_out()
        print(schedule.evaluate())

if __name__ == "__main__":
    main()
