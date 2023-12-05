from s3840220_s3841863_GA import s3840220_s3841863_GA
from itertools import product
from ioh import get_problem, logger, ProblemClass
import numpy as np
import json
# Template for the experiments
# We can run the grid search, and keep the 5 best combination sets for the plots

def create_problem(fid: int, dimension: int = 50, name: str = None):
    # Declaration of problems to be tested.
    problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)

    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name="run",  # the folder name to which the raw performance data will be stored
        algorithm_name=f"{name}",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l

def run_experiments(fid: int, 
                    dimension: int, 
                    name: str, 
                    sel_mech: str, 
                    cross_mech: str, 
                    mut_mech: str, 
                    pop_size: int, 
                    mut_rate: float, 
                    cross_prob: float, 
                    tour_k: int):
    problem, _logger = create_problem(fid, dimension, name)
    results = []
    for run in range(20): 
        x =s3840220_s3841863_GA(problem, 
                             experiments=True,
                             sel_mech=sel_mech, 
                             cross_mech=cross_mech, 
                             mut_mech=mut_mech, 
                             pop_size=pop_size, 
                             mut_rate=mut_rate, 
                             cross_prob=cross_prob, 
                             tour_k=tour_k)
        problem.reset() # it is necessary to reset the problem after each independent run
        results.append(x)


    _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder
    return np.mean(results)


if __name__ == "__main__":
    param_grid = {
        "selection_mechanism": ["proportional_seletion","tournament_seletion"],
        "crossover_mechanism": ["one_point_crossover","n_point_crossover","uniform_crossover"],
        "mutation_mechanism": ["bit_flip_mutation","swap_mutation"],
        "population_size": [50, 100, 150],
        "mutation_rate": [0.01, 0.02, 0.05],
        "crossover_probability": [0.5, 0.7],
        "tournament_k": [10, 20]
    }
    
    # Create all combinations of parameters
    param_combinations = list(product(*param_grid.values()))
    # print(param_combinations[72])
    combination_dict = {}
    print(f"Total combinations: {len(param_combinations)}")
    for i, param_set in enumerate(param_combinations):
        print(f"Running combination {i+1} of {len(param_combinations)} ({(i+1)/len(param_combinations)*100:.2f}%)")
        print(*param_set)
        res=run_experiments(19, 50, f"{param_set[0]}_{param_set[1]}_{param_set[2]}_{param_set[3]}_{param_set[4]}_{param_set[5]}_{param_set[6]}", *param_set)
        combination_dict[res] = param_set

    sorted_combinations = sorted(combination_dict.items(), key=lambda x: x[0], reverse=True)
    # export as json
    with open("results.json", "w") as f:
        json.dump(sorted_combinations, f, indent=4)

    # run_experiments(18, 50, "best", *param_combinations[72])