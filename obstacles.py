from map_handler import dummy_get_start_end_coordinates
from generategrid import generate_grid


start_coords, end_coords = dummy_get_start_end_coordinates()
# grid = generate_grid(start_coords[0], end_coords[0], start_coords[1], end_coords[1], 0.05)
# obstacles = []
# obstacles = [
#     (9.3, 79.7), (9.3, 79.75), (9.3, 79.8), (9.35, 79.2),
#     (9.35, 79.25), (9.35, 79.3), (9.35, 79.35),
#     (9.2, 79.7), (9.25, 79.75), (9.25, 79.55), (9.3, 79.3),
# ]
# print(obstacles)
#
# # def lat_lon_to_grid_index(lat, lon, start_lat, start_lon, step_size):
# #     lat_index = int(abs(lat - start_lat) / step_size)
# #     lon_index = int(abs(lon - start_lon) / step_size)
# #     return lat_index, lon_index
#
# def detect_obstacles(start_coords, end_coords, obstacles, step_size=0.08):
#     start_lat, start_lon = start_coords
#     end_lat, end_lon = end_coords
#
#     # Define bounding box to consider points within start and end lat/lon
#     bbox = (min(start_lon, end_lon), min(start_lat, end_lat), max(start_lon, end_lon), max(start_lat, end_lat))
#
#     obstacle_indices = []
#     for i, row in enumerate(grid):
#         for j, point in enumerate(row):
#             lat, lon = point
#             if bbox[1] <= lat <= bbox[3] and bbox[0] <= lon <= bbox[2]:
#                 if point in obstacles:
#                     # Flattened grid index calculation
#                     grid_index = i * len(grid[0]) + j
#                     obstacle_indices.append(grid_index)
#
#     return obstacle_indices
#
#     # # for obstacle in obstacles:
#     # #     # obstacle_lat, obstacle_lon = obstacle
#     # #     # if bbox[1] <= obstacle_lat <= bbox[3] and bbox[0] <= obstacle_lon <= bbox[2]:
#     # #     #     # grid_x, grid_y = lat_lon_to_grid_index(obstacle_lat, obstacle_lon, start_lat, start_lon, step_size)
#     # #     #     if (obstacle_lat, obstacle_lon) in grid:
#     # #     #         obstacle_indices.append(grid.index((obstacle_lat, obstacle_lon)))
#     # #     if obstacle in grid:
#     # #         obstacle_indices.append(grid.index(obstacle))
#     # # return obstacle_indices
#     # for i, row in enumerate(grid):
#     #     for j, point in enumerate(row):
#     #         lat, lon = point
#     #         if bbox[1] <= lat <= bbox[3] and bbox[0] <= lon <= bbox[2]:
#     #             if point in obstacles:
#     #                 obstacle_indices.append((i, j))
#     #
#     # return obstacle_indices
#
# # Define some obstacles manually (latitude, longitude pairs)
# obstacle_indices = detect_obstacles(start_coords, end_coords, obstacles)
# def get_obstacle_indices():
#     return obstacle_indices, grid
# print("Obstacle indices:", obstacle_indices)

def detect_obstacles(start_coords, end_coords, obstacles, step_size=0.05):
    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords

    # Create a bounding box to limit grid points within start and end lat/lon
    bbox = (min(start_lon, end_lon), min(start_lat, end_lat), max(start_lon, end_lon), max(start_lat, end_lat))

    obstacle_indices = []
    grid = generate_grid(start_lat, end_lat, start_lon, end_lon, step_size)

    for i, row in enumerate(grid):
        for j, point in enumerate(row):
            lat, lon = point
            if bbox[1] <= lat <= bbox[3] and bbox[0] <= lon <= bbox[2]:
                if point in obstacles:
                    # Calculate the flattened grid index
                    grid_index = i * len(grid[0]) + j
                    obstacle_indices.append(grid_index)

    return obstacle_indices, grid

obstacles = [
        (9.3, 79.7), (9.3, 79.75), (9.3, 79.8), (9.35, 79.2),
        (9.35, 79.25), (9.3, 79.3), (9.35, 79.35),(9.3, 79.7), (9.3, 79.75), (9.3, 79.8), (9.35, 79.2),
        (9.2, 79.7), (9.25, 79.75), (9.25, 79.55), (9.3, 79.3),
        (9.4, 79.6),(9.5, 79.6)
]
def get_obstacle_indices():
    obstacle_indices, grid = detect_obstacles(start_coords, end_coords, obstacles)
    return obstacle_indices, grid
obs, g = get_obstacle_indices()
print(obs)

