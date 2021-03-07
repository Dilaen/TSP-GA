from src.entity import *

from random import sample
from typing import Tuple


# recombination method

def order_crossover(father: Individual, mother: Individual) -> List[Individual]:
    fa, mo = father.route, mother.route
    problem = father.problem
    n = len(fa)
    points = sample([i for i in range(n + 1)], 2)
    a, b = min(points), max(points)

    def crossover(parent1: List[int], parent2: List[int]) -> List[int]:
        parent1_idx = parent2_idx = b % n
        chd = [0 for i in range(a)] + parent1[a:b] + [0 for i in range(n - b)]
        fst = frozenset(parent1[a:b])
        while parent1_idx != a:
            while parent2[parent2_idx] in fst:
                parent2_idx = (parent2_idx + 1) % n
            chd[parent1_idx] = parent2[parent2_idx]
            parent1_idx = (parent1_idx + 1) % n
            parent2_idx = (parent2_idx + 1) % n
        return chd

    chd1, chd2 = crossover(fa, mo), crossover(mo, fa)
    return [Individual(problem, chd1), Individual(problem, chd2)]
    
def patially_mapped_crossover(father: Individual, mother: Individual) -> List[Individual]:
    return NotImplemented

def cycle_crossover(father: Individual, mother: Individual) -> List[Individual]:
    return NotImplemented

def edge_recombination(father: Individual, mother: Individual) -> List[Individual]:
    return NotImplemented


# mutation method

def __select_points(ind: List[int]) -> Tuple[int]:
    n = len(ind)
    points = sample([i for i in range(n)], 2)
    return min(points), max(points)

def insert(individual: Individual) -> Individual:
    ind = individual.route
    a, b = __select_points(ind)
    temp = ind[b]
    for i in range(b - 1, a, -1):
        ind[i + 1] = ind[i]
    ind[a] = temp
    return Individual(individual.problem, ind)

def swap(individual: Individual) -> Individual:
    ind = individual.route
    a, b = __select_points(ind)
    ind[a], ind[b] = ind[b], ind[a]
    return Individual(individual.problem, ind)

def inversion(individual: Individual) -> Individual:
    ind = individual.route
    a, b = __select_points(ind)
    for i in range((b - a + 1) // 2):
        ind[a + i], ind[b - i] = ind[b - i], ind[a + i]
    return Individual(individual.problem, ind)

def scramble(individual: Individual) -> Individual:
    return NotImplemented


# survivor selection method

def fitness_proportional(population: Population) -> Population:
    return NotImplemented

def tournament_selection(population: Population) -> Population:
    return NotImplemented

def elitism(population: Population) -> Population:
    return Population(sorted(population.individuals,
                             key=lambda individual: individual.fitness,
                             reverse=True)[:population.size]) 
