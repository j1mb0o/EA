# import numpy as np
# # you need to install this package `ioh`. Please see documentations here: 
# # https://iohprofiler.github.io/IOHexp/ and
# # https://pypi.org/project/ioh/
# from ioh import get_problem, logger, ProblemClass
# import sys
# # from ES_utils import initialize, one_sigma_mutation, encode, recombination
# from ESClass import EStrategy

# budget = 5000
# dimension = 50
# mu = 10
# lamda_ = 20
# # To make your results reproducible (not required by the assignment), you could set the random seed by
# # `np.random.seed(some integer, e.g., 42)`
# np.random.seed(42)



# def s3840220_s3841863_ES(problem, lambda_=20, mu=10):
#     x_opt = None
#     f_opt = sys.float_info.max

#     es = EStrategy(mu, lamda_, dimension=problem.meta_data.n_variables)

#     for i in range(mu):
#         # encoded_p = es.encode(es.parent[i])
#         prob_eval = problem(es.encode(es.parent[i]))
#         es.parent_f.append(prob_eval)
#         if es.parent_f[i] < f_opt:
#             f_opt = es.parent_f[i]
#             x_opt = es.parent[i].copy()

#     while problem.state.evaluations < budget:

#         for _ in range(lamda_):
#             o, s = es.recombination(es.parent, es.parent_sigma)
#             # es.recombination(es.parent, es.parent_sigma)
#             es.offspring_sigma.append(s)
#             es.offspring.append(o)
#         # print("Recombination done")
#         es.one_sigma_mutation(es.offspring, es.offspring_sigma)
#         # print("Mutation done")
#         for i in range(lamda_):
#             prob_eval = problem(es.encode(es.offspring[i]))
#             es.offspring_f.append(prob_eval)

#             if es.offspring_f[i] < f_opt:
#                 f_opt = es.offspring_f[i]
#                 x_opt = es.offspring[i].copy()

#         es.selection()
#         print(problem.state.evaluations)
#         # print("Selection done")
#     print("Best found solution: f = {}".format(f_opt))


#     # no return value needed 


# def create_problem(fid: int):
#     # Declaration of problems to be tested.
#     problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)

#     # Create default logger compatible with IOHanalyzer
#     # `root` indicates where the output files are stored.
#     # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
#     l = logger.Analyzer(
#         root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
#         folder_name="run",  # the folder name to which the raw performance data will be stored
#         algorithm_name="genetic_algorithm",  # name of your algorithm
#         algorithm_info="Practical assignment of the EA course",
#     )
#     # attach the logger to the problem
#     problem.attach_logger(l)
#     return problem, l


# if __name__ == "__main__":
#     # this how you run your algorithm with 20 repetitions/independent run
#     F18, _logger = create_problem(18)
#     for run in range(20): 
#         print(run)
#         s3840220_s3841863_ES(F18)
        
#         F18.reset() # it is necessary to reset the problem after each independent run
#     _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder

import numpy as np

# Assuming your sequences are in a 3x10 array
sequences = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                      [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])

# Assuming fitness values are in a separate array
fitness = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print(np.vstack((sequences, fitness)))
# # Get the indices that would sort the fitness array in descending order
# sorted_indices = np.argsort(fitness)[::-1]

# # Use these indices to reorder the sequences and fitness arrays
# sorted_sequences = sequences[sorted_indices]
# sorted_fitness = fitness[sorted_indices]

# print("Indices (Descending Order):")
# print(sorted_indices)
# print("Sorted Sequences (Descending Order):")
# print(sorted_sequences)
# print("\nSorted Fitness (Descending Order):")
# print(sorted_fitness)

