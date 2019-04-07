'''
Created on 2019/04/07

@author: minami
'''

import random

class Individual(object):
    '''
    one-max problem individual data
    '''

    __size = 100
    __individual_mutate_pb = 0.2
    __gene_mutate_pb = 0.05

    @classmethod
    def initialize(cls, size = 100, mutate = 0.2, gene_mutate = 0.05):
        '''
        set individual's mutation probability
        '''
        cls.__size = size
        cls.__individual_mutate_pb = mutate
        cls.__gene_mutate_pb = gene_mutate

    def __init__(self):
        '''
        Constructor
        '''
        self.gene = [random.randint(0, 1) for _ in range(self.__size)]

    def eval_fitness(self):
        '''
        evaluate individual's fitness
        '''
        self.fitness = sum(self.gene)

    def try_mutation(self):
        '''
        probably mutate inidividual's gene
        '''
        if(random.random() >= self.__individual_mutate_pb):
            return
        for index, value in enumerate(self.gene):
            if(random.random() < self.__gene_mutate_pb):
                self.gene[index] = type(value)(not value)

    def mate_to(self, ind2):
        size = min(len(self), len(ind2))
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        self.gene[cxpoint1:cxpoint2], ind2.gene[cxpoint1:cxpoint2] \
            = ind2.gene[cxpoint1:cxpoint2], self.gene[cxpoint1:cxpoint2]

def mate_individuals(ind1, ind2):
    ind1.mate_to(ind2)
