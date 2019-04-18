'''
Created on 2019/04/17

@author: minami
'''

import random
import Scheduling
from deap import tools
import datetime

def main():
#     random.seed(64)
    schedules = Scheduling.create_schedules()

    cross_probability = 0.5
    mutation_probability = 0.2
    gene_mutation_probability = 0.05

    print("Start Evolution!")

    start = datetime.datetime.now()

    g = 0
    fits = [schedule.fitness for schedule in schedules]

    means = []
    mins = []
    maxs = []

    length = len(schedules)
    mean = sum(fits) / length
    sum2 = sum(x*x for x in fits)
    std = abs(sum2 / length - mean**2)**0.5

    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))
    print("  Avg %s" % mean)
    print("  Std %s" % std)

    means.append(mean)
    mins.append(min(fits))
    maxs.append(max(fits))

    while max(fits) < 0 and g < 100:
        # 世代数更新
        g = g + 1
        print("-- Generation %i --" % g)

        schedules = tools.selTournament(schedules, len(schedules), 10)
        schedules = [Scheduling.Schedule(s.list_map) for s in schedules]

        Scheduling.try_mate(schedules, cross_probability)

        for mutant in schedules:
            if random.random() < mutation_probability:
                mutant.try_mutate(gene_mutation_probability)

        for schedule in schedules:
            schedule.assign_person()
            schedule.evaluate()
        fits = [schedule.fitness for schedule in schedules]

        length = len(schedules)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        means.append(mean)
        mins.append(min(fits))
        maxs.append(max(fits))

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(schedules, 1)[0]
    print("Best individual is followed")
    best_ind.console_out_persons()
    print(f"Fitness is {best_ind.fitness}")

    end = datetime.datetime.now()
    print(end - start)

    print(maxs)
    print(means)
    print(mins)

if __name__ == '__main__':
    main()
