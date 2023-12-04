import numpy as np

# you need to install this package `ioh`. Please see documentations here:
# https://iohprofiler.github.io/IOHexp/ and
# https://pypi.org/project/ioh/
from ioh import get_problem, logger, ProblemClass
import sys
from itertools import product
from ES_utils import (
    initialize,
    one_sigma_mutation,
    individual_sigma_mutation,
    encode,
    recombination,
    comma_selection,
    plus_selection,
)


budget = 5000
# dimension =git 
# To make your results reproducible (not required by the assignment), you could set the random seed by
# `np.random.seed(some integer, e.g., 42)`
np.random.seed(42)


def s3840220_s3841863_ES(problem, fnum=18,experiments=False, **kwargs):
    # hint: F18 and F19 are Boolean problems. Consider how to present bitstrings as real-valued vectors in ES
    # initial_pop = ... make sure you randomly create the first population
    x_opt = None
    f_opt = sys.float_info.min
    mu = kwargs["mu"]
    lamda_ = kwargs["lamda_"]

    tau = 1.0 / np.sqrt(problem.meta_data.n_variables)
    tau_local = 1.0 / np.sqrt(2 * np.sqrt(problem.meta_data.n_variables))
    tau_global = 1.0 / np.sqrt(2 * problem.meta_data.n_variables)
    # Initialize

    if fnum == 19:
        parent, parent_sigma = initialize(mu, lowerbound=-1.0, upperbound=1.0, dimension=problem.meta_data.n_variables)
    else:
        parent, parent_sigma = initialize(mu, dimension=problem.meta_data.n_variables)

    # Evaluate parent
    parent_f = []
    for i in range(mu):
        parent_f.append(problem(encode(parent[i])))
        if parent_f[i] > f_opt:
            f_opt = parent_f[i]
            x_opt = parent[i].copy()

    while problem.state.evaluations < budget:
        # Offspring recombination
        offspring = []
        offspring_sigma = []
        offspring_f = []

        for i in range(lamda_):
            o, s = recombination(parent, parent_sigma, kwargs["recombination"])
            offspring.append(o)
            offspring_sigma.append(s)
        # Mutation
        if kwargs["mutation"] == "one_sigma":
            one_sigma_mutation(fnum, offspring, offspring_sigma, tau)
        elif kwargs["mutation"] == "individual_sigma":
            individual_sigma_mutation(
               fnum, offspring, offspring_sigma, tau_global=tau_global, tau_local=tau_local
            )
        # individual_sigma_mutation(offspring, offspring_sigma, tau_global=tau_global, tau_local=tau_local)

        # Offspring evaluation
        for i in range(lamda_):
            offspring_f.append(problem(encode(offspring[i])))
            if offspring_f[i] > f_opt:
                f_opt = offspring_f[i]
                x_opt = offspring[i].copy()

        if kwargs["selection"] == "comma":
            parent, parent_sigma, parent_f = comma_selection(
                offspring, offspring_sigma, offspring_f, mu
            )
        # parent, parent_sigma, parent_f = comma_selection(offspring, offspring_sigma, offspring_f, mu)
        elif kwargs["selection"] == "plus":
            parent, parent_sigma, parent_f = plus_selection(
                parent=parent,
                parent_sigma=parent_sigma,
                parent_f=parent_f,
                offspring=offspring,
                offspring_sigma=offspring_sigma,
                offspring_f=offspring_f,
                mu=mu,
            )

    # print("Best found solution: f = {}".format(f_opt))
    if experiments:
        return f_opt
    # no return value needed


def create_problem(fid: int):
    # Declaration of problems to be tested.
    problem = get_problem(
        fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO
    )

    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name="run",  # the folder name to which the raw performance data will be stored
        algorithm_name="genetic_algorithm",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l


if __name__ == "__main__":
    # this how you run your algorithm with 20 repetitions/independent run
    # combinations = 

    F18, _logger = create_problem(18,)
    for run in range(20):
        s3840220_s3841863_ES(F18)

        F18.reset()  # it is necessary to reset the problem after each independent run
    _logger.close()  # after all runs, it is necessary to close the logger to make sure all data are written to the folder

    # F19, _logger = create_problem(19)
    # for run in range(20):
    #     s3840220_s3841863_ES(F19)
    #     F19.reset()
    # _logger.close()
