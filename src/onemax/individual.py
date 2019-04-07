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
    __individual_mutate_pb = 0.4
    __gene_mutate_pb = 0.05

    @classmethod
    def initialize(cls, size = 100, mutate = 0.4, gene_mutate = 0.05):
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
