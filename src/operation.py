from src.entity import *

from random import sample


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
    

def patially_mapped_crossover():
    pass

def cycle_crossover():
    pass

def edge_recombination():
    pass


def insert(individual: Individual) -> Individual:
    return NotImplemented

def swap(individual: Individual) -> Individual:
    ind = individual.route
    n = len(ind)
    points = sample([i for i in range(n)], 2)
    a, b = min(points), max(points)
    ind[a], ind[b] = ind[b], ind[a]
    return ind

def inversion(individual: Individual) -> Individual:
    return NotImplemented

def scramble(individual: Individual) -> Individual:
    return NotImplemented


def fitness_proportional(population: Population) -> Population:
    return NotImplemented

def tournament_selection(population: Population) -> Population:
    return NotImplemented

def elitism(population: Population) -> Population:
    return Population(sorted(population.individuals,
                             key=lambda individual: individual.fitness,
                             reverse=True)[:population.size]) 
