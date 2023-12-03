from ioh import get_problem, logger, ProblemClass
import numpy as np
dimension = 10
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

prob, l = create_problem(1)

# x = np.array([1 for i in range(dimension)])

# print(prob(x))  

offsprings = np.random.randint(2, size=(10, dimension))
# print(offsprings, prob(offsprings))
for i in offsprings:
    print(i, prob(i))

rank = np.argsort(prob(offsprings))

sorted_offsprings = offsprings[rank]
print("Sorted offsprings")
for i in sorted_offsprings:
    print(i, prob(i))

mu_ = 5

parent = sorted_offsprings[:mu_]
parent_f = prob(parent)

print("Parent")
for i in range(len(parent)):
    print(parent[i], parent_f[i])