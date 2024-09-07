#$ pip install aco_routing
import math
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import KDTree
from aco_routing import ACO
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
from generategrid import generate_grid
import inspect
print(inspect.signature(ACO.__init__))


lat_lon=[(9.6, 78.8),
(9.6, 78.88),
(9.6, 78.96),
(9.6, 79.04),
(9.6, 79.12),
(9.6, 79.2),
(9.6, 79.28),
(9.6, 79.36),
(9.6, 79.44),
(9.6, 79.52),
(9.6, 79.6),
(9.6, 79.68),
(9.6, 79.76),
(9.6, 79.84),
(9.6, 79.92),
(9.6, 80.0),
(9.6, 80.08),
(9.6, 80.16),
(9.52, 78.8),
(9.52, 78.88),
(9.52, 78.96),
(9.52, 79.04),
(9.52, 79.12),
(9.52, 79.2),
(9.52, 79.28),
(9.52, 79.36),
(9.52, 79.44),
(9.52, 79.52),
(9.52, 79.6),
(9.52, 79.68),
(9.52, 79.76),
(9.52, 79.84),
(9.52, 79.92),
(9.52, 80.0),
(9.52, 80.08),
(9.52, 80.16),
(9.44, 78.8),
(9.44, 78.88),
(9.44, 78.96),
(9.44, 79.04),
(9.44, 79.12),
(9.44, 79.2),
(9.44, 79.28),
(9.44, 79.36),
(9.44, 79.44),
(9.44, 79.52),
(9.44, 79.6),
(9.44, 79.68),
(9.44, 79.76),
(9.44, 79.84),
(9.44, 79.92),
(9.44, 80.0),
(9.44, 80.08),
(9.44, 80.16),
(9.36, 78.8),
(9.36, 78.88),
(9.36, 78.96),
(9.36, 79.04),
(9.36, 79.12),
(9.36, 79.2),
(9.36, 79.28),
(9.36, 79.36),
(9.36, 79.44),
(9.36, 79.52),
(9.36, 79.6),
(9.36, 79.68),
(9.36, 79.76),
(9.36, 79.84),
(9.36, 79.92),
(9.36, 80.0),
(9.36, 80.08),
(9.36, 80.16),
(9.28, 78.8),
(9.28, 78.88),
(9.28, 78.96),
(9.28, 79.04),
(9.28, 79.12),
(9.28, 79.2),
(9.28, 79.28),
(9.28, 79.36),
(9.28, 79.44),
(9.28, 79.52),
(9.28, 79.6),
(9.28, 79.68),
(9.28, 79.76),
(9.28, 79.84),
(9.28, 79.92),
(9.28, 80.0),
(9.28, 80.08,),
(9.28, 80.16),
(9.2, 78.8),
(9.2, 78.88),
(9.2, 78.96),
(9.2, 79.04),
(9.2, 79.12),
(9.2, 79.2),
(9.2, 79.28),
(9.2, 79.36),
(9.2, 79.44),
(9.2, 79.52),
(9.2, 79.6),
(9.2, 79.68),
(9.2, 79.76),
(9.2, 79.84),
(9.2, 79.92),
(9.2, 80.0),
(9.2, 80.08),
(9.2, 80.16),
(9.12, 78.8),
(9.12, 78.88),
(9.12, 78.96),
(9.12, 79.04),
(9.12, 79.12),
(9.12, 79.2),
(9.12, 79.28),
(9.12, 79.36),
(9.12, 79.44),
(9.12, 79.52),
(9.12, 79.6),
(9.12, 79.68),
(9.12, 79.76),
(9.12, 79.84),
(9.12, 79.92),
(9.12, 79.92),
(9.12, 80.0),
(9.12, 80.08),
(9.12, 80.16),
(9.12, 79.92),
(9.12, 80.0),
(9.12, 79.92),
(9.12, 79.92),
(9.12, 80.0),
(9.12, 80.08),
(9.12, 80.16)]
speed=30.492733295499843
lat_lon_set=set(lat_lon)
lat_lon=list(lat_lon_set)
print(f"len of lat_lon: {len(lat_lon_set)}")

def haversine(lat1,lon1,lat2,lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1,lon1,lat2,lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371 # radious in km
    return c*r

G=nx.Graph()
for coord in lat_lon:
    G.add_node(coord)
'''
print(f"Graph G: {G}")
pos = nx.spring_layout(G)
nx.draw(G,pos,with_labels=True, node_color='lightblue', node_size=5)
plt.show()
'''

num_nodes=(len(lat_lon))

def generate_start_end_pairs(num_nodes):
    pairs = []
    for start in range(num_nodes):
        for end in range(num_nodes):
            if start != end:
                pairs.append((start, end))
    return pairs
pairs=generate_start_end_pairs(num_nodes)

num_of_ants=10 # 2- ->10
num_of_itrs=30
ant_max_steps=100 #1000 ->100
alpha=1.0 #importance of pheromone
beta=0.07 #importance of heuristic factor
rho=0.3 # pheromone evaporation coeff
q=1.0 #pheromone increase intensity coeff

def initialize_pheromone_matrix():
    pheromone_matrix = np.ones((num_nodes, num_nodes)) / num_nodes
    return pheromone_matrix

phrm=initialize_pheromone_matrix()
print(phrm)
print(phrm.shape)
print('_'*10)
pheromone_matrix = np.ones((126,126))
print(pheromone_matrix.shape)
print(pheromone_matrix)

start_node=random.choice(lat_lon)
end_node=random.choice(lat_lon)
print(start_node)
print(end_node)

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

def get_dist_mat():
    num_points = len(lat_lon)
    distance_matrix = np.zeros((num_points, num_points))
    for i,coor1 in enumerate(lat_lon):
        for j,coor2 in enumerate(lat_lon):
            if i!=j:
                #distance_matrix[i,j]=haversine(coor1[0],coor1[1],coor2[0],coor2[1])
                distance_matrix[i,j]=euclidean_distance(coor1,coor2)
    return distance_matrix

distance_matrix=get_dist_mat()

def calculate_heuristic(point, end_point):
    # the inverse of the dist to the end_point is the heuristhicccc
    return 1.0/distance_matrix[lat_lon.index(point),lat_lon.index(end_point)]
    #return 1.0 / np.linalg.norm(np.array(point) - np.array(end_point))

def select_next_node(current_node, pheromone_matrix, alpha, beta, end_point):
    curr_index=lat_lon.index(current_node)
    distances=distance_matrix[curr_index]
    pheromone_levels=pheromone_matrix[curr_index]
    
    distances = np.clip(distances, a_min=1e-10, a_max=None) #avoids zero distances
    probabilities=((pheromone_levels ** alpha) * ((1/distances) ** beta)) #or is it 1/distances
    probabilities /= probabilities.sum()
    # za roulette selection
    next_node_idx = np.random.choice(len(lat_lon), p=probabilities)
    next_node = lat_lon[next_node_idx]
    return next_node

def simulate_ants(start_point, end_point, pheromone_matrix, alpha, beta):
    paths = []
    for _ in range(num_of_ants):
        current_node = start_point
        path = [current_node]
        while current_node != end_point:
            next_node = select_next_node(current_node, pheromone_matrix, alpha, beta, end_point)
            path.append(next_node)
            current_node = next_node
        paths.append(path)
    return paths

def update_pheromone(paths, pheromone_matrix, rho, q):
    new_pheromone_matrix = pheromone_matrix * (1 - rho)
    for path in paths:
        path_length = len(path)
        pheromone_deposit = q / path_length
        for i in range(len(path) - 1):
            node_from = lat_lon.index(path[i])
            node_to = lat_lon.index(path[i + 1])
            new_pheromone_matrix[node_from, node_to] += pheromone_deposit
            new_pheromone_matrix[node_to, node_from] += pheromone_deposit 
    return new_pheromone_matrix

for iteration in range(num_of_itrs):
    paths = simulate_ants(start_node, end_node, pheromone_matrix, alpha, beta)
    pheromone_matrix = update_pheromone(paths, pheromone_matrix, rho, q)

shortest_path = min(paths, key=len)
print("Shortest Path:", shortest_path)

def visualize_path(G, path, start_node, end_node):
    # Create a copy of the graph to modify for visualization
    H = G.copy()

    # Create a color map for nodes
    node_colors = ['lightblue'] * len(G.nodes)
    
    # Highlight the nodes in the path
    path_nodes = set(path)
    for node in path_nodes:
        node_colors[list(G.nodes).index(node)] = 'lightgreen'
    
    # Create edge colors based on the path
    edge_colors = []
    for edge in H.edges:
        if edge in zip(path, path[1:]) or edge in zip(path[1:], path):
            edge_colors.append('red')
        else:
            edge_colors.append('lightgrey')
    
    # Highlight the start and end nodes
    node_colors[list(G.nodes).index(start_node)] = 'yellow'
    node_colors[list(G.nodes).index(end_node)] = 'yellow'
    
    # Draw the graph
    pos = nx.spring_layout(H)
    plt.figure(figsize=(12, 8))

    # Draw nodes and edges
    nx.draw_networkx_nodes(H, pos, node_color=node_colors, node_size=300)
    nx.draw_networkx_edges(H, pos, edgelist=H.edges, edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(H, pos, labels={node: node for node in H.nodes}, font_size=10)
    
    # Draw the path specifically
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(H, pos, edgelist=path_edges, edge_color='blue', width=4)
    
    # Highlight the start and end nodes with labels
    nx.draw_networkx_nodes(H, pos, nodelist=[start_node, end_node], node_color='yellow', node_size=500)
    nx.draw_networkx_labels(H, pos, labels={start_node: 'Start', end_node: 'End'}, font_size=12, font_color='black')

    plt.title("Shortest Path Visualization")
    plt.show()


visualize_path(G, shortest_path, start_node, end_node)
