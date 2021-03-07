from src.solver import TSPSolver


problem_name_list = ['eil51', 'pcb442']
problem_list = [f'problem/instance/{problem_name}.tsp' for problem_name in problem_name_list]

for problem in problem_list:
    TSPSolver(problem, 'problem/tour').solve()