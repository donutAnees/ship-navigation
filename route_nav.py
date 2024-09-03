'''
This thing implements the ACO algorithm to find the shortest path between the start and end point on a grid, with real time map data.
But this shit runs for 2 hrs and still not accurate........
try increasing the step_size in the obstacles.py or reducing the ant number.
Fine-tuning the parameter can solve the pblm upto some level.
'''

import numpy as np
import random
import math
import csv
from map_handler import dummy_get_start_end_coordinates
from obstacles import get_obstacle_indices

# Get start and end coordinates using your provided function
start_coords, end_coords = (9.6, 79.2), (9.1, 79.9)  # Dummy start and end coordinates
step_size = 0.05
from grid import generate_grid_points

# Generate grid based on these coordinates
obstacle_indices, grid = get_obstacle_indices()
# Generate grid with 0.08 degree step
grid = generate_grid_points(9.6, 9.1, 78.8, 80.2, 0.08)
#print(grid)

# Flatten the grid to a list of coordinates
nodes = {i: coord for i, coord in enumerate([coord for row in grid for coord in row])}

# Function to calculate Euclidean distance between two points
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

# Find indices of start and end coordinates in the grid
start_node = min(nodes, key=lambda k: euclidean_distance(nodes[k], start_coords))
end_node = min(nodes, key=lambda k: euclidean_distance(nodes[k], end_coords))

# Parameters for ACO
num_ants = 20  # Increased number of ants to explore more paths
num_iterations = 200  # Increased number of iterations for better convergence
alpha = 0.7  # Reduced alpha to balance pheromone and heuristic importance
beta = 3.0  # Increased beta to give more importance to the heuristic (distance)
evaporation_rate = 0.1  # Reduced evaporation rate to maintain pheromone trails longer
pheromone_deposit = 2.0  # Increased pheromone deposit to reinforce good paths
tau_0 = 1.0  # Initial pheromone level remains the same

# Initialize pheromone levels on each edge
pheromone = np.full((len(nodes), len(nodes)), tau_0)

# Avoid obstacles by setting pheromone levels to 0
for i, coord in nodes.items():
    if coord in obstacle_indices:
        pheromone[i, :] = 0
        pheromone[:, i] = 0

# Function to choose the next node based on the probability distribution
def choose_next_node(probabilities):
    total = sum(prob for prob, node in probabilities)
    rand = random.uniform(0, total)
    current = 0
    for prob, node in probabilities:
        current += prob
        if current >= rand:
            return node
    return probabilities[-1][1]

# Open CSV file for writing
with open('aco_paths.csv', 'w', newline='') as csvfile:
    fieldnames = ['Iteration', 'Path', 'Distance']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # ACO main loop
    for iteration in range(num_iterations):
        all_paths = []
        all_distances = []

        for ant in range(num_ants):
            path = [start_node]
            visited = set(path)
            current_node = start_node
            total_distance = 0

            while current_node != end_node:
                probabilities = []
                for next_node in nodes:
                    if (next_node not in visited) and (next_node not in obstacle_indices):
                        pheromone_level = pheromone[current_node][next_node] ** alpha
                        heuristic_value = (1 / euclidean_distance(nodes[current_node], nodes[next_node])) ** beta
                        probability = pheromone_level * heuristic_value
                        probabilities.append((probability, next_node))

                if not probabilities:
                    break

                next_node = choose_next_node(probabilities)
                path.append(next_node)
                visited.add(next_node)
                total_distance += euclidean_distance(nodes[current_node], nodes[next_node])
                current_node = next_node

            if current_node == end_node:
                all_paths.append((path, total_distance))
                all_distances.append(total_distance)

        # Evaporate pheromone
        pheromone *= (1 - evaporation_rate)

        # Reinforce pheromone on successful paths
        if all_paths:
            shortest_path = min(all_paths, key=lambda x: x[1])
            path, distance = shortest_path

            pheromone_increase = pheromone_deposit / distance
            for i in range(len(path) - 1):
                pheromone[path[i]][path[i + 1]] += pheromone_increase
                pheromone[path[i + 1]][path[i]] += pheromone_increase  # assuming undirected graph

            # Write all paths for this iteration to the CSV file
            for path, distance in all_paths:
                path_str = " -> ".join(map(str, [nodes[node] for node in path]))
                writer.writerow({'Iteration': iteration + 1, 'Path': path_str, 'Distance': distance})

            print(f"Iteration {iteration + 1}: Best path (nodes) = {path}, Distance = {distance}")

        # Adaptive strategy: Gradually increase alpha and beta as the algorithm progresses
        if iteration > num_iterations // 2:
            alpha = min(2.0, alpha + 0.1)  # Gradually increase alpha, max 2.0
            beta = min(5.0, beta + 0.2)  # Gradually increase beta, max 5.0
