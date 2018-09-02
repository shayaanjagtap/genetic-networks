#! /usr/bin/env python3

# code tutorial sourced from : https://lethain.com/genetic-algorithms-cool-name-damn-simple/

import random
from random import randint

def individual(length, min, max):
    '''a member of the population'''
    return [randint(min, max) for x in range(length)]


def population(count, length, min, max):
    '''create a number of individuals to form a population'''
    return [individual(length, min, max) for x in range(count)]


# must judge how effective an individual solution is - create an evalutation method
from operator import add # basically imports a way to use '+' as a function
from functools import reduce
def fitness(individual, target):
    '''determine the fitness of an individual'''

    sum = reduce(add, individual, 0)
    return abs(target-sum)


def grade(pop, target):
    '''grading an entire populations fitness'''
    summed = reduce(add, [fitness(x, target) for x in pop], 0)
    return summed / (len(pop) * 1.0)


def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, target), x) for x in pop]
    graded = [ x[1] for x in sorted(graded)] # returns the top individuals by fitness
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[:retain_length:]:
        if random_select > random.uniform(0,1):
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random.uniform(0,1):
            pos_to_mutate = randint(0, len(individual)-1)
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # breed the individuals
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:half] + female[half:]
            children.append(child)

        parents.extend(children)

    return parents
