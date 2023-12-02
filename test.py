from ioh import get_problem, logger, ProblemClass
import sys
import numpy as np

def create_problem(fid: int):
    # Declaration of problems to be tested.
    problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)

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



def encode_mean(x):
    return [1 if i >= x.mean() else 0 for i in x]



dimension=50

F18, _logger = create_problem(18)

print(F18.meta_data.n_variables)

parent = [np.random.uniform(low = 0, high = 1.0, size = 10)]
# choice = np.random.randint(2, size=len(parent[0]))
# choice = [1 for _ in range(dimension)]
# print(len(parent))
print(parent)
# print([1 if i >= np.mean(parent) else 0 for i in parent[i]])
# print([1 if i >= 0.5 else 0 for i in parent[i]])
x1 = encode(parent[0])
x2 = encode_mean(parent[0])
print(x1)
print(x2)
print(np.mean(parent))