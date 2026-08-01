import itertools
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import pandas as pd
import time
import os


def draw_tsp_route(permutation, coordinates,fitness):
    """
    Draws a network representation of a given TSP permutation.
    
    # Parameters:
    # - permutation: List of node indices representing the visiting order
    # - coordinates: Dictionary {node: (x, y)} with node positions
    # """
    # G = nx.DiGraph()
    # # Add nodes
    # for node, pos in coordinates.items():
    #     G.add_node(node, pos=pos)
    # # Add edges based on the given permutation
    # for i in range(len(permutation) - 1):
    #     G.add_edge(permutation[i], permutation[i + 1])
    # G.add_edge(permutation[-1], permutation[0])  # Completing the cycle 
    # # Extract positions for drawing
    # pos = nx.get_node_attributes(G, 'pos')
    # plt.clf()  # Clear the previous plot
    # plt.title(f'TSP Route Length {fitness}')
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='black', node_size=500, font_size=10)
    # nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='red', width=2, arrows=True)
    # plt.draw()

def calculate_distance (data,n):
    distance = np.ones((n, n)) * np.inf
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j:
                distance[i,j] = np.sqrt((data[i,1]-data[j,1])**2 + (data[i,2]-data[j,2])**2 )
    return distance

def calculate_fitness(ROUTE,distance,n):
    fitness = 0
    for i in range(n-1):
        x = int(ROUTE[i])
        y = int(ROUTE[i+1])
        fitness = fitness + distance[x,y]
    orig = int(ROUTE[0])
    fitness = fitness + distance[y,orig]
    return fitness
def is_permutation (arr,n):
    return np.array_equal(np.sort(arr), np.arange(0, n))

def ox_crossover(i1, i2, POP, rng):
    PARENT1 = POP[i1, 0:n].astype(int)
    PARENT2 = POP[i2, 0:n].astype(int)
    [pos1, pos2] = sorted(rng.integers(0, n, size=2))
    OS = np.full(n, -1)
    OS[pos1:pos2] = PARENT1[pos1:pos2]
    k = 0
    for i in range(n):
        if OS[i] != -1:
            continue
        while PARENT2[k] in OS:
            k += 1
        OS[i] = PARENT2[k]
    return OS

def anx_crossover(i1, i2, POP, rng):
    parent1 = POP[i1, 0:n].astype(int)
    parent2 = POP[i2, 0:n].astype(int)
    OS = []
    visited = set()
    current_city = rng.choice(parent1)
    current_parent = [parent1, parent2]
    p_index = 0
    while len(OS) < n:
        OS.append(current_city)
        visited.add(current_city)
        idx = np.where(current_parent[p_index] == current_city)[0][0]
        next_idx = (idx + 1) % n
        next_city = current_parent[p_index][next_idx]
        if next_city in visited:
            p_index = 1 - p_index
            idx = np.where(current_parent[p_index] == current_city)[0][0]
            next_idx = (idx + 1) % n
            next_city = current_parent[p_index][next_idx]
            if next_city in visited:
                unvisited = list(set(parent1) - visited)
                if unvisited:
                    next_city = rng.choice(unvisited)
                else:
                    break
        current_city = next_city
    return np.array(OS)

def exchange_mutation(route, rng):
    a, b = rng.choice(len(route), size=2, replace=False)
    route[a], route[b] = route[b], route[a]
    return route

def inversion_mutation(route, rng):
    a, b = sorted(rng.choice(len(route), size=2, replace=False))
    route[a:b+1] = np.flip(route[a:b+1])
    return route

def scramble_mutation(route, rng):
    a, b = sorted(rng.choice(len(route), size=2, replace=False))
    route[a:b+1] = rng.permutation(route[a:b+1])
    return route

def displacement_mutation(route, rng):
    a, b = sorted(rng.choice(len(route), size=2, replace=False))
    subseq = route[a:b+1]
    rest = np.delete(route, np.s_[a:b+1])
    insert_at = rng.integers(0, len(rest)+1)
    return np.insert(rest, insert_at, subseq)

def insert_mutation(route, rng):
    a, b = sorted(rng.choice(len(route), size=2, replace=False))
    elem = route[a]
    route = np.delete(route, a)
    route = np.insert(route, b, elem)
    return route

def edge_recombination_crossover(i1, i2, POP, n, rng):
    P1 = POP[i1, 0:n].astype(int)
    P2 = POP[i2, 0:n].astype(int)
    def build_edge_map(P1, P2):
        edge_map = defaultdict(set)
        for p in [P1, P2]:
            for i in range(n):
                city = p[i]
                left = p[(i - 1) % n]
                right = p[(i + 1) % n]
                edge_map[city].update([left, right])
        return edge_map
    edge_map = build_edge_map(P1, P2)
    current = rng.choice(P1)
    offspring = [current]
    visited = {current}
    while len(offspring) < n:   
        for c in edge_map:
            edge_map[c].discard(current)
        candidates = [c for c in edge_map[current] if c not in visited]
        if not candidates:
            unvisited = list(set(P1) - visited)
            current = rng.choice(unvisited)
        else:
            min_len = min(len(edge_map[c]) for c in candidates)
            filtered = [c for c in candidates if len(edge_map[c]) == min_len]
            current = rng.choice(filtered)
        offspring.append(current)
        visited.add(current)
    return np.array(offspring)

# Parametreler
POP_SIZES = [30]
ITERATIONS = [int(1e5)]
ER_VALUES = [0.1,0.2,0.3]
CR_VALUES = [0.5,0.7,0.9]
MR_VALUES = [0.01,0.05, 0.1]

SEEDS = range(10)
TIME_LIMIT = 60
results = []

data = np.loadtxt("dataSets/berlin52.txt")
n = len(data)
distance = calculate_distance (data,n)
coordinates = data[:, -2:] # Convert to dictionary where keys are indices and values are NumPy arrays
coordinates_dict = {i: coordinates[i] for i in range(len(coordinates))}
for ps in POP_SIZES:
    for iterations in ITERATIONS:
        for er in ER_VALUES:
            es = int(ps*er)
            for cr in CR_VALUES:
                offs = int(ps*cr)
                for mr in MR_VALUES:
                    for seed in SEEDS:
                            rng = np.random.default_rng(seed=seed)
                            start_time = time.time()
                            POP = np.zeros((ps, n + 1))
                            for i in range(ps):
                                route = rng.permutation(n)
                                fitness = calculate_fitness(route, distance, n)
                                POP[i, :n] = route
                                POP[i, n] = fitness
                            SPOP = POP[POP[:, -1].argsort()]
                            ZEUS = SPOP[0, :]
                            best_fitness = ZEUS[n]
                            best_route = ZEUS[:n]
                        
                            it = 1

                            while it < iterations and time.time() - start_time < TIME_LIMIT:
                                new_POP = []
                                elit_count = int(ps * er)
                                new_POP.extend(POP[POP[:, -1].argsort()][:elit_count])

                                while len(new_POP) < ps:
                                    i1, i2 = rng.choice(ps, 2, replace=False)
                                    if rng.random() < cr:
                                        rn1 = rng.random()
                                        if rn1 < 1/4:
                                            OS  = ox_crossover(i1, i2, POP, rng)
                                        elif rn1 < 2/4:
                                            OS  = edge_recombination_crossover(i1, i2, POP, n, rng)
                                        elif rn1 < 3/4:
                                            OS = anx_crossover(i1, i2, POP, rng)
                                        else:
                                            OS = POP[i1, :n].copy()
                                    else:
                                        OS = POP[i1, :n].copy()

                                    if rng.random() < mr:
                                        rn2 = rng.random()
                                        if rn2 < 1/5:
                                            OS = exchange_mutation( OS , rng)
                                        elif rn2 < 2/5:
                                            OS = inversion_mutation(OS , rng)
                                        elif rn2 < 3/5:
                                            OS = scramble_mutation(OS, rng)
                                        elif rn2 < 4/5:
                                            OS = displacement_mutation(OS , rng)
                                        else:
                                            OS = insert_mutation(OS, rng)

                                    fitness_offspring = calculate_fitness(OS, distance, n)
                                    new_individual = np.append(OS, fitness_offspring)
                                    new_POP.append(new_individual)

                                    for i in range(ps - len(new_POP)):
                                        ROUTE = rng.permutation(n)
                                        FITNESS = calculate_fitness(ROUTE, distance, n)
                                        new_POP.append(np.append(ROUTE, FITNESS))

                                
                                POP = np.array(new_POP)
                                SPOP = POP[POP[:, -1].argsort()]
                                HERKUL = SPOP[0, :]
                                if  HERKUL[n] < ZEUS[n]:
                                    ZEUS = HERKUL
                                    best_fitness = ZEUS[n]
                                    best_route = ZEUS[:n]
                                    print(f'Best found Zeus update of fitness: {ZEUS[n]} in generation {it} and {time.time() - start_time:.2f} seconds')
                                    # draw_tsp_route(HERKUL[0:n], coordinates_dict,HERKUL[n])
                                    # plt.pause(0.01)
                                it += 1

                            results.append([data, ps, iterations, er, cr, mr, seed, best_fitness])
                            print(f"Dataset: {data}, PS: {ps}, Iterations: {iterations}, ER: {er}, CR: {cr}, MR: {mr}, Seed: {seed}, Best Fitness: {best_fitness}")


# plt.show()
results_df = pd.DataFrame(results, columns=['Dataset', 'PS', 'Iterations', 'ER', 'CR', 'MR', 'Seed', 'Best Fitness'])
output_path = os.path.join(os.getcwd(), 'TSP_Parameter_Optimization_Results_.xlsx')
results_df.to_excel(output_path, index=False)
print(f'Results saved to {output_path}')
