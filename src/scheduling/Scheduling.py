# -*- coding: utf-8 -*-

from enum import IntEnum, auto
import random
from deap import tools

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

        return self.begin < other.end and self.end > other.begin

    def __str__(self):
        return f'{self.begin}-{self.end}'

times = [10, 12, 14, 16, 18, 20]
time_ranges = [TimeRange(times[x], times[x + 1]) for x in range(len(times) - 1)]

class Matter(object):

    def __init__(self, location, occupation_map, begin_time, end_time):
        self.location = location
        self.occupation_map = occupation_map
        self.time_range = TimeRange(begin_time, end_time)

    def __str__(self):
        return f'matter: {self.time_range.__str__()} location: {self.location}'

class Person(object):

    __next_id = None

    def __init__(self, occupation, person_id = None):
        self.__initialize_id()

        self.occupation = occupation
        if(person_id is None):
            self.id = self.__next_id[occupation]
            self.__next_id[occupation] += 1
        else:
            self.id = person_id

        self.assigned_matters = []

    @classmethod
    def __initialize_id(self):
        if(self.__next_id is not None):
            return

        self.__next_id = {}
        for occupation in Occupation:
            self.__next_id[occupation] = 0

    def assignTo(self, matter):
        self.assigned_matters.append(matter)

    def clone(self):
        return Person(self.occupation, self.id)

    def judge_overlap(self, overlap_list):
        for x in range(len(time_ranges)):
            overlap = 0
            for assigned_matter in self.assigned_matters:
                overlap += 1 if assigned_matter.time_range.overlappedTo(time_ranges[x]) else 0

            overlap_list[x] += 0 if overlap <= 1 else overlap - 1

    def judge_distance(self):
        assigned_locations = [x.location for x in self.assigned_matters]
        location_count = [assigned_locations.count(location) for location in Location]
        distance = sum([ 1 if count > 0 else 0 for count in location_count])
        return 0 if distance < 1 else distance - 1

    def __str__(self):
        return f'Person: id={self.id} occupation={self.occupation} assigned_matters={[x.__str__() for x in self.assigned_matters]}'

class Schedule(object):

    matters = None
    persons = None

    @classmethod
    def initialise(cls, matters, persons):
        cls.matters = matters
        cls.persons = persons

    def __init__(self, list_map = None):
        self.__create_person_map()
        if(list_map == None):
            self.__create_schedule_list()
            self.assign_person()
        else:
            self.__create_schedule_list(list_map)

    def __create_person_map(self):
        self.person_map = {}
        for occupation in Occupation:
            self.person_map[occupation] = []

        for person in self.persons:
            self.person_map[person.occupation].append(person.clone())

    def __create_schedule_list(self, list_map = None):
        self.list_map = {}
        for occupation in Occupation:
            self.list_map[occupation] = []

            if(list_map == None):
                for matter in self.matters:
                    assigned_persons = random.sample(self.person_map[occupation], matter.occupation_map[occupation])

                    self.list_map[occupation].extend(assigned_persons)

            else:
                self.list_map[occupation].extend([[x for x in self.person_map[occupation] if x.id == person.id][0]\
                                                   for person in list_map[occupation]])

    def assign_person(self):
        for occupation in Occupation:
            assigned_list= self.list_map[occupation]
            begin = 0

            for matter in self.matters:
                assigned_count = matter.occupation_map[occupation]
                matter_assigned_list = assigned_list[begin:begin + assigned_count]
                for person in matter_assigned_list:
                    person.assignTo(matter)

                begin += assigned_count


    def __eval_overlap(self):
        overlap_list = [0 for _ in range(len(time_ranges))]

        for occupation in Occupation:
            for person in self.person_map[occupation]:
                person.judge_overlap(overlap_list);

        return - sum(overlap_list)

    def __eval_distance(self):
        distance = 0;
        for occupation in Occupation:
            for person in self.person_map[occupation]:
                distance += person.judge_distance()

        return - distance

    def evaluate(self):
        self.fitness = self.__eval_overlap() * 100 + self.__eval_distance()

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

    def console_out_simple(self):
        for occupation in Occupation:
            print([person.__str__() for person in self.list_map[occupation]])

    def console_out_persons(self):
        for occupation in Occupation:
            for person in self.person_map[occupation]:
                print(person.__str__())

    def try_mutate(self, prob):
        for occupation in Occupation:
            for x in range(len(self.list_map[occupation])):
                if(random.random() < prob):
                    self.list_map[occupation][x] = random.sample(self.person_map[occupation], 1)[0]

def try_mate(schedules, prob):
    for child1, child2 in zip(schedules[::2], schedules[1::2]):

        if random.random() < prob:
            for occupation in Occupation:
                tools.cxTwoPoint(child1.list_map[occupation], child2.list_map[occupation])


def create_matters():
    matters = []
    locations = [loc for loc in Location]
    person_count = range(3)
    probs = [1, 4, 10, 20, 100]

    for _ in range(40):
        location = random.choice(locations)
        occupation_map = {}
        for occupation in Occupation:
            occupation_map[occupation] = random.choice(person_count)

        rd = random.randint(0, 99)
        for x in range(len(probs)):
            if(rd < probs[x]):
                index = random.randint(0, x)
                begin_time = times[index]
                end_time = times[index + len(times) - 1 - x]
                break

        matters.append(Matter(location, occupation_map, begin_time, end_time))

    return matters

def create_persons():
    persons = []

    for occupation in Occupation:
        persons.extend([Person(occupation) for _ in range(20)])

    return persons

def create_schedules():
    Schedule.initialise(create_matters(), create_persons())
    schedules = [Schedule() for _ in range(100)]
    for schedule in schedules:
#         schedule.console_out()
        schedule.evaluate()
#         print(schedule.fitness)

    return schedules

