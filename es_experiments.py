from ioh import get_problem, logger, ProblemClass
from s3840220_s3841863_ES import s3840220_s3841863_ES
from itertools import product
import numpy as np
import json


def create_problem(fid: int, dim: int=50, name: str = None):
    if name is None:
        print("Name of problem is required")
        exit(1)
    # print("Creating problem...")
    problem = get_problem(fid, dimension=dim, instance=1, problem_class=ProblemClass.PBO)

    l = logger.Analyzer(
        root="data",
        folder_name="run",
        algorithm_name=name,
        algorithm_info="ES experiments for EA course",
    )
    problem.attach_logger(l)
    return problem, l


def run_experiment(fid: int, 
                    dim: int, 
                    name: str,
                    mutation: str,
                    recombination: str,
                    selection: str,
                    mu: int,
                    lamda: int):
    problem, _logger = create_problem(fid, dim, name)
    results = []
    for run in range(20):
        x = s3840220_s3841863_ES(problem=problem,
                                fnum=fid,
                                experiments=True,        
                                mutation=mutation,
                                recombination=recombination,
                                selection=selection,
                                mu=mu,
                                lamda_=lamda)
        results.append(x)
        problem.reset()
    _logger.close()
    return np.mean(results)


if __name__ == "__main__":
    # create_problem(1, 50)
    param_dict = {
        "mutation": ["one_sigma", "individual_sigma"],
        "recombination": [
            "discreet",
            "intermediate",
            "global_discreet",
            "global_intermediate",
        ],
        "selection": ["comma", "plus"],
        "mu": [10, 50, 100],
        "lamda": [20, 100, 200],
    }

    combinations = list(product(*param_dict.values()))
    print(f"Total number of combinations: {len(combinations)}")
    comb_dict = {}

    for i, comb in enumerate(combinations):
        print(
            f"Running combination {i+1} of {len(combinations)} ({(i+1)/len(combinations)*100:.2f}%)"
        )
        res = run_experiment(
            19, 50, f"{comb[0]}_{comb[1]}_{comb[2]}_{comb[3]}_{comb[4]}", *comb
        )

        comb_dict[res] = comb

    sorted_comb = sorted(comb_dict.items(), key=lambda x:x[0] ,reverse=True)
    with open("results.json", "w") as f:
        json.dump(sorted_comb, f, indent=4)
