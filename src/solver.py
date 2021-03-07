from src.operation import *

from random import random, uniform


class TSPSolver:
    """Solver for TSP using Evolutionary Algorithm.

    Attributes:
        problem: The TSP to solve.
        problem_name: The name of the problem.
        answer_directory_path: The path to the directory of the TSP answer file.
        population: All the answers to the problem.
    """

    def __init__(self, tsp_problem_path: str, tsp_answer_directory_path: str, population_size: int = 100) -> None:
        """Constructs a TSP solver.

        Args:
            tsp_problem_path: The path to the TSP problem file.
            tsp_answer_directory_path: The path to the directory of the TSP answer file.
            population_size: The size of the population.
        """
        with open(tsp_problem_path, 'r') as f:
            self.problem = TSP(f)
        self.answer_directory_path = tsp_answer_directory_path
        self.problem_name = tsp_problem_path.split('/')[-1].split('.')[0]
        self.population = Population([Individual(self.problem) for i in range(population_size)])
        self.population.individuals.sort(key=lambda x: x.fitness, reverse=True)

    def _construct_answer(self, individual: Individual) -> None:
        lines = []
        lines.append('NAME : {}.tour\n'.format(self.problem_name))
        lines.append('COMMENT : Optimal tour for {}.tsp  ({})\n'.format(self.problem_name, int(individual.route_length)))
        lines.append('TYPE : TOUR\n')
        lines.append('DIMENSION : {}\n'.format(self.problem.city_num))
        lines.append('TOUR_SECTION\n')
        idx = -1
        for i in range(self.problem.city_num):
            if individual.route[i] == 1:
                idx = i
                break
        for i in range(idx, self.problem.city_num):
            lines.append('{}\n'.format(individual.route[i]))
        for i in range(idx):
            lines.append('{}\n'.format(individual.route[i]))
        lines.append('-1\n')
        lines.append('EOF\n')
        with open('{}/{}.tour'.format(self.answer_directory_path, self.problem_name), 'w') as f:
            f.writelines(lines) 

    def solve(self, recombination_method: str = 'order_crossover',
              mutation_method: str = 'swap',
              selection_method: str = 'elitism',
              parent_selection_probability: float = 0.8,
              waiting_generation: int = 200) -> None:
        """Solves the TSP with the given method.

        Args:
            recombination_method: The name of the recombination method, defaults to 'order_rossover'.
            mutation_method: The name of the mutation method, defaults to 'swap'.
            selection_method: The name of the selection method, defaults to 'elitism'.
            parent_selection_probability: The probability of selecting an individual into the mating pool.
            waiting_generation: The number of generations to wait before terminating the algorithm for no fitness improvement.
        """
        global_table = globals()
        best_individual = self.population.individuals[0]
        waiting_cnt = 0
        MUTATION_PROBABILITY = uniform(1 / self.population.size, 1 / self.problem.city_num)
        MAX_GENERATION = 1000000
        generation = 0
        while waiting_cnt < waiting_generation:
            if generation == MAX_GENERATION:
                break
            generation += 1
            # parent selection
            mating_pool = []
            while len(mating_pool) == 0:
                for individual in self.population.individuals:
                    if random() < parent_selection_probability:
                        mating_pool.append(individual)
            # recombination
            for i in range(1, len(mating_pool), 2):
                self.population.individuals += global_table[recombination_method](mating_pool[i - 1], mating_pool[i])
            # mutation
            for individual in self.population.individuals:
                if random() < MUTATION_PROBABILITY:
                    individual = global_table[mutation_method](individual)
            # survivor selection
            self.population = global_table[selection_method](self.population)
            # termination condition checking
            if self.population.individuals[0].fitness > best_individual.fitness:
                best_individual = self.population.individuals[0]
                waiting_cnt = 0
            else:
                waiting_cnt += 1
            print('generation #{}: best_fitness = {}'.format(generation, self.population.individuals[0].fitness))
        self._construct_answer(best_individual)