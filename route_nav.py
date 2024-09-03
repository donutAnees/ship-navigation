import numpy as np
import random
import math
import csv
from generategrid import generate_grid
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
# print('nodes:',nodes)

# Define the start and end nodes (using indices from the grid)
start_node = 0  # Corresponds to the first coordinate in the grid
end_node = len(nodes) - 1  # Corresponds to the last coordinate in the grid

# Parameters for ACO
num_ants = 10
num_iterations = 100
alpha = 1.0  # Pheromone importance
beta = 0.07   # Heuristic importance (inverse of distance)
evaporation_rate = 0.3
pheromone_deposit = 1.0
tau_0 = 1.0  # Initial pheromone level

# Function to calculate Euclidean distance between two nodes
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

# Initialize pheromone levels on each edge
pheromone = np.full((len(nodes), len(nodes)), tau_0)

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
                        # print("next_node:", next_node) # Avoid visited nodes and obstacles
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

        pheromone *= (1 - evaporation_rate)
        for path, distance in all_paths:
            pheromone_increase = pheromone_deposit / distance
            for i in range(len(path) - 1):
                pheromone[path[i]][path[i + 1]] += pheromone_increase
                pheromone[path[i + 1]][path[i]] += pheromone_increase  # assuming undirected graph

        if all_paths:
            shortest_path = min(all_paths, key=lambda x: x[1])
            path_nodes = [nodes[node] for node in shortest_path[0]]
            path_str = " -> ".join(map(str, path_nodes))

            writer.writerow({
                'Iteration': iteration + 1,
                'Path': path_str,
                'Distance': shortest_path[1]
            })

            print(f"Iteration {iteration + 1}: Best path (nodes) = {shortest_path[0]}, Distance = {shortest_path[1]}")

if all_paths:
    final_shortest_path = min(all_paths, key=lambda x: x[1])
    final_path_coords = [nodes[node] for node in final_shortest_path[0]]

    print(f"\nFinal best path (nodes): {final_shortest_path[0]}")
    print(f"Final best path (coordinates): {final_path_coords}")
    print(f"Final distance: {final_shortest_path[1]}")
else:
    print("No valid paths found.")



