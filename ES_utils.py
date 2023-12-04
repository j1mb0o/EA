import numpy as np

np.random.seed(42)

def initialize(mu, dimension, upperbound=1.0, lowerbound=0.0):
    parent = []
    parent_sigma = []
    for i in range(mu):
        parent.append(
            np.random.uniform(low=lowerbound, high=upperbound, size=dimension)
        )
        parent_sigma.append(0.05 * (upperbound - lowerbound))

    return parent, parent_sigma


def one_sigma_mutation(fnum, parent, parent_sigma, tau):
    for i in range(len(parent)):
        parent_sigma[i] = parent_sigma[i] * np.exp(np.random.normal(0, tau))
        for j in range(len(parent[i])):
            if fnum == 18:
                parent[i][j] = parent[i][j] + np.random.normal(0, parent_sigma[i])
                parent[i][j] = parent[i][j] if parent[i][j] < 1.0 else 1.0
                parent[i][j] = parent[i][j] if parent[i][j] > 0.0 else 0.0
            else:
                parent[i][j] = parent[i][j] + np.random.normal(0, parent_sigma[i])
                parent[i][j] = parent[i][j] if parent[i][j] < 1.0 else 1.0
                parent[i][j] = parent[i][j] if parent[i][j] > -1.0 else -1.0

def individual_sigma_mutation(fnum, parent, parent_sigma, tau_global, tau_local):
    g = np.random.normal(0, 1)
    for i in range(len(parent)):
        parent_sigma[i] = parent_sigma[i] * np.exp(
            tau_global * g + tau_local * np.random.normal(0, 1)
        )
        for j in range(len(parent[i])):
            if fnum== 18:
                parent[i][j] = parent[i][j] + np.random.normal(0, parent_sigma[i])
                parent[i][j] = parent[i][j] if parent[i][j] < 1.0 else 1.0
                parent[i][j] = parent[i][j] if parent[i][j] > 0.0 else 0.0
            else:
                parent[i][j] = parent[i][j] + np.random.normal(0, parent_sigma[i])
                parent[i][j] = parent[i][j] if parent[i][j] < 1.0 else 1.0
                parent[i][j] = parent[i][j] if parent[i][j] > -1.0 else -1.0

def encode(x):
    return [1 if i >= 0.5 else 0 for i in x]

def recombination(parent, parent_sigma, recombination_type="discreet"):
    # Discreet recombination
    if recombination_type == "discreet":
        [p1, p2] = np.random.choice(len(parent), 2, replace=False)
        choice = np.random.randint(2, size=len(parent[0]))
        offspring = np.where(choice == 0, parent[p1], parent[p2])
        sigma = np.where(choice == 0, parent_sigma[p1], parent_sigma[p2])
        sigma = sigma.mean()

    elif recombination_type == "intermediate":
        [p1, p2] = np.random.choice(len(parent), 2, replace=False)
        offspring = (parent[p1] + parent[p2]) / 2
        sigma = (parent_sigma[p1] + parent_sigma[p2]) / 2

    elif recombination_type == "globlal_discrete":
        choice = np.random.randint(len(parent), size=len(parent[0]))
        offspring = np.array([parent[choice[i]][i] for i in range(len(parent[0]))])
        sigma = np.array(
            [parent_sigma[choice[i]] for i in range(len(parent[0]))]
        ).mean()

    # global intermediate recombination
    else:
        offspring = np.average(parent, axis=0)
        sigma = np.array(parent_sigma).mean()


    return offspring, sigma

def comma_selection(offspring, offspring_f, offspring_sigma,mu):

    rank = np.argsort(offspring_f)[::-1]
    sorted_offspring = np.array(offspring)[rank]
    sorted_offspring_sigma = np.array(offspring_sigma)[rank]
    sorted_offspring_f = np.array(offspring_f)[rank]
    parent = sorted_offspring[:mu]
    parent_sigma = sorted_offspring_sigma[:mu]
    parent_f = sorted_offspring_f[:mu]
        
    return parent, parent_sigma, parent_f

def plus_selection(parent, parent_f, parent_sigma, offspring, offspring_f, offspring_sigma, mu):

    candidates = np.vstack((parent, offspring))
    candidates_f = np.hstack((parent_f, offspring_f))
    candidates_sigma = np.hstack((parent_sigma, offspring_sigma))

    rank = np.argsort(candidates_f)[::-1]
    sorted_candidates = np.array(candidates)[rank]
    sorted_candidates_sigma = np.array(candidates_sigma)[rank]
    sorted_candidates_f = np.array(candidates_f)[rank]

    return sorted_candidates[:mu], sorted_candidates_sigma[:mu], sorted_candidates_f[:mu]