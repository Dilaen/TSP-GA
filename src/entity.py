from typing import List, Callable, IO, Optional


class TSP:
    """Represents a Traveling Salesperson Problem.

    Attributes:
        city_num: The number of cities.
        graph: A matrix of distances between every pair of cities.
    """

    def __init__(self, tsp_file: IO) -> None:
        """Constructs a TSP from the given file.
        """
        START_ROW = 6
        cities = []
        lines = tsp_file.readlines()
        for i in range(START_ROW, len(lines) - 1):
            lst = lines[i].split()
            x, y = float(lst[1]), float(lst[2])
            cities.append((x, y))
        self.city_num = len(cities)
        self.graph = [[0.0 for j in range(self.city_num)] for i in range(self.city_num)]
        from math import sqrt
        for i in range(self.city_num):
            for j in range(i + 1, self.city_num):
                self.graph[i][j] = self.graph[j][i] = \
                    sqrt((cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2)


class Individual:
    """Represents an answer to the TSP.

    Attributes:
        problem: The problem to which this individual belongs.
        route: The route of the answer.
        route_length: The total length of the route.
        fitness: The fitness of this individual.
    """
    
    def __init__(self, problem: TSP, route: Optional[List[int]] = None, fitness_func: Callable[[float], float] = lambda x: 1 / x) -> None:
        """Construct an individual from the given route in the given problem.

        The fitness of this individual is passed to argument fitness_func to calculate.
        """
        self.problem = problem
        if route:
            self.route = route
        else:
            self.route = [i for i in range(1, problem.city_num + 1)]
            from random import shuffle
            shuffle(self.route)
        self.route_length = 0.0
        for i in range(self.problem.city_num):
            self.route_length += self.problem.graph[self.route[i - 1] - 1][self.route[i] - 1]
        self.fitness = fitness_func(self.route_length)

class Population:
    """Represents a pool of answers to the TSP.

    Attrubutes:
        size: The size of the population.
        individuals: All the answers of this Population.
    """
    
    def __init__(self, individuals: List[Individual]) -> None:
        """Constructs a population with the given individuals.
        """
        self.individuals = individuals
        self.size = len(individuals)