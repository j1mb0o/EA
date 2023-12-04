import numpy as np
import sys

# pop_size = 3
# tournament_k = 10
# mutation_rate = 0.02
# crossover_probability = 0.5

# Uniform Crossover
def uniform_crossover(p1, p2, crossover_probability):
    if(np.random.uniform(0,1) < crossover_probability):
        for i in range(len(p1)) :
            if np.random.uniform(0,1) < 0.5:
                t = p1[i]
                p1[i] = p2[i]
                p2[i] = t
    return p1,p2    

# 1-point Crossover
def one_point_crossover(p1, p2, crossover_probability):
    if(np.random.uniform(0,1) < crossover_probability):
        point = np.random.randint(1, len(p1))
        for i in range(point,len(p1)):
            t = p1[i]
            p1[i] = p2[i]
            p2[i] = t
    return p1,p2

# n-point Crossover
def n_point_crossover(parent1, parent2, n, crossover_probability):
    if np.random.uniform(0,1) < crossover_probability:
        points = np.sort(np.random.choice(len(parent1), n, replace=False))
        # print("Points are:",points)
        offspring1 = np.empty_like(parent1)
        offspring2 = np.empty_like(parent2)

        parent_switch = False
        start_point = 0

        for point in points:
            if not parent_switch:
                offspring1[start_point:point] = parent1[start_point:point]
                offspring2[start_point:point] = parent2[start_point:point]
            else:
                offspring1[start_point:point] = parent2[start_point:point]
                offspring2[start_point:point] = parent1[start_point:point]

            parent_switch = not parent_switch
            start_point = point

        if not parent_switch:
            offspring1[start_point:] = parent1[start_point:]
            offspring2[start_point:] = parent2[start_point:]
        else:
            offspring1[start_point:] = parent2[start_point:]
            offspring2[start_point:] = parent1[start_point:]

        return offspring1, offspring2
    else:
        return parent1, parent2



# Standard bit mutation using mutation rate p
def bit_flip_mutation(p, mutation_rate):
    for i in range(len(p)) :
        if np.random.uniform(0,1) < mutation_rate:
            p[i] = 1 - p[i]
    return p


def swap_mutation(p,mutation_rate):
    for i in range(len(p)):
        if np.random.uniform(0,1) < mutation_rate:
            point = np.random.randint(0,len(p))
            p[i],p[point] = p[point],p[i]
    return p


def proportional_seletion(parent, parent_f):
    # Plusing 0.001 to avoid dividing 0
    f_min = min(parent_f)
    f_sum = sum(parent_f) - (f_min - 0.001) * len(parent_f)
    
    rw = [(parent_f[0] - f_min + 0.001)/f_sum]
    for i in range(1,len(parent_f)):
        rw.append(rw[i-1] + (parent_f[i] - f_min + 0.001) / f_sum)
    
    select_parent = []
    for i in range(len(parent)) :
        r = np.random.uniform(0,1)
        index = 0
        # print(rw,r)
        while(r > rw[index]) :
            index = index + 1
        
        select_parent.append(parent[index].copy())
    return select_parent


def tournament_seletion(parent, parent_f, tournament_k):
    # Using the tournament selection
    select_parent = []
    for i in range(len(parent)) :
        pre_select = np.random.choice(len(parent_f),tournament_k,replace = False)
        max_f = sys.float_info.min
        for p in pre_select:
            if parent_f[p] > max_f:
                index = p
                max_f = parent_f[p]
        select_parent.append(parent[index].copy())
    return select_parent