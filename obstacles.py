from map_handler import dummy_get_start_end_coordinates
from grid import generate_grid_points
from map_land_areas import is_land_area


start_coords, end_coords = dummy_get_start_end_coordinates()

def detect_obstacles(start_coords, end_coords, step_size=0.04):
    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords

    # Create a bounding box to limit grid points within start and end lat/lon
    bbox = (min(start_lon, end_lon), min(start_lat, end_lat), max(start_lon, end_lon), max(start_lat, end_lat))

    obstacle_indices = []
    grid = generate_grid_points(start_lat-0.20, end_lat+0.20, start_lon-0.20, end_lon+0.20, step_size)

    for i, row in enumerate(grid):
        for j, point in enumerate(row):
            lat, lon = point
            if bbox[1] <= lat <= bbox[3] and bbox[0] <= lon <= bbox[2]:
                if is_land_area(lat, lon):
                    # Calculate the flattened grid index
                    grid_index = i * len(grid[0]) + j
                    obstacle_indices.append(grid_index)

    return obstacle_indices, grid

# obstacles = [
#         (9.3, 79.7), (9.3, 79.75), (9.3, 79.8), (9.35, 79.2),
#         (9.35, 79.25), (9.3, 79.3), (9.35, 79.35),(9.3, 79.7), (9.3, 79.75), (9.3, 79.8), (9.35, 79.2),
#         (9.2, 79.7), (9.25, 79.75), (9.25, 79.55), (9.3, 79.3),
#         (9.4, 79.6),(9.5, 79.6)
# ]
obstacle_indices, grid = detect_obstacles(start_coords, end_coords)
def get_obstacle_indices():
    return obstacle_indices, grid
obs, g = get_obstacle_indices()
print(g)
print(obs)

