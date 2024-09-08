from aco_routing import ACO
import networkx as nx

'''
Performs Ant Colony Optimization to identify the optimal routes in the ocean.
'''
INF = 99999

# initialize the start and end coordinates of the grid
grid_start = (0,0)
grid_end = (4,5)

def create_graph(num_rows, num_cols, obstacles):
    '''Converts the points grid into a graph where the edges represent the possible paths that can be taken by the ship.
       Paths containing obstacles are represented with a cost of INF and paths without are represented with a cost of 1.
        Returns:
            An undirected graph with all possible edges and their corresponding costs
        Parameters:
            num_rows -> Number of points in a row in the grid area
            num_cols -> Number of points in a column in the grid area
            obstacles -> A list of obstacle coordinates
    '''
    # initialize the graph
    G = nx.Graph()
    # iterate through the number of rows and columns to get the grid indices
    index = 1
    grid = list()
    for row in range(num_rows):
        rows = list()
        for col in range(num_cols):
            rows.append(index)
            index+=1
        grid.append(rows)

    # print(grid) [uncomment for debugging]

    # iterate through the grid and draw edges in the graph
    for i in range(num_rows):
        for j in range(num_cols):
            if (j+1 < num_cols):
                # check if the grid to the right is an obstacle or not
                if (grid[i][j] not in obstacles and grid[i][j+1] not in obstacles):
                    G.add_edge(grid[i][j], grid[i][j+1], cost=1)
                else:
                    G.add_edge(grid[i][j], grid[i][j+1], cost=INF)
            if (i+1 < num_rows):
                # check if the grid to the bottom is an obstacle or not
                if (grid[i][j] not in obstacles and grid[i+1][j] not in obstacles):
                    G.add_edge(grid[i][j], grid[i+1][j], cost=1)
                else:
                    G.add_edge(grid[i][j], grid[i+1][j], cost=INF)  

    # print(G.nodes) [uncomment for debugging]
    # print(G.edges(data=True)) [uncomment for debugging]

    return G

def modify_graph(G, new_cost_list):
    '''Modifies the graph to update the cost of traversing through certain edges.
        Returns:
            Updated undirected graph with edges and their corresponding costs
        Parameters:
            G -> Current graph
            new_cost_list -> Mapping of specific points and the costs associated with traveling to or from them
    '''
    # get the list of grids whose costs are to be updated
    update_points = new_cost_list.keys()
    for point1,point2 in G.edges:
        # check if the grids in a given edge are present in the new update list and update accordingly
        if(point1 in update_points):
            G.add_edge(point1, point2, cost=new_cost_list[point1])
        elif(point2 in update_points):
            G.add_edge(point1, point2, cost=new_cost_list[point2])
    
    # print(G.edges(data=True)) [uncomment for debugging]

    return G

def run_aco(G, start_lat, start_lon, end_lat, end_lon, step, num_rows, num_cols):
    '''Runs the Ant Colony Optimization algorithm on the grid of points (represented as an undirected graph).
        Returns:
            1. Optimized ACO path identified
            2. Cost of traversing the path
        Parameters:
            G -> The graph that represents the grid area
            start_lat -> The latitude of the source point
            start_lon -> The longitude of the source point
            end_lat -> The latitude of the destination point
            end_lon -> The longitude of the destination point
            step -> The difference in coordinates between two adjacent points in the grid area
            num_rows -> Number of points in a row in the grid area
            num_cols -> Number of points in a column in the grid area
    '''
    # initialize the ACO object
    aco = ACO(G, ant_max_steps=100, num_iterations=100 ,ant_random_spawn=True)
    # calculate the source and destination grid indices using the starting and ending coordinates and the step value
    start_lat_diff = start_lat - grid_start[0]
    start_lon_diff = start_lon - grid_start[1]
    end_lat_diff = end_lat - grid_start[0]
    end_lon_diff = end_lon - grid_start[1]
    start_point = int(1 + (start_lat_diff / step)*num_cols + (start_lon_diff/step)) 
    end_point = int(1 + (end_lat_diff / step)*num_cols + (end_lon_diff/step))

    # print(start_point, end_point) [uncomment for debugging]

    # perform aco to calculated the shortest path
    aco_path, path_cost = aco.find_shortest_path(source=start_point, destination=end_point, num_ants=100)

    return (aco_path, path_cost)


# checking functionality [uncomment the below lines for debugging]
# G = create_graph(5, 6, [3,16,19,24,27])
# modify_graph(G, {2:INF, 6:INF})
# print(run_aco(G, 1, 1, 4, 3, 1, 5, 6))