from map_handler import dummy_get_start_end_coordinates
from grid import generate_grid_points
from map_land_areas import is_land_area


start_coords, end_coords = dummy_get_start_end_coordinates()

def detect_obstacles(start_coords, end_coords, step_size=0.08):

    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords
    bbox = (min(start_lon, end_lon), min(start_lat, end_lat), max(start_lon, end_lon), max(start_lat, end_lat))

    obstacle_indices = []
    grid = generate_grid_points(start_lat-step_size, end_lat+step_size, start_lon-step_size, end_lon+step_size, step_size)

    for i, row in enumerate(grid):
        for j, point in enumerate(row):
            lat, lon = point
            if bbox[1] <= lat <= bbox[3] and bbox[0] <= lon <= bbox[2]:
                if is_land_area(lat, lon):
                    obstacle_indices.append(point)
    return obstacle_indices, grid

def calculate_midp(start_coords, end_coords, step_size=1):
    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords

    """
    calculating the midpoints representesd by the start cords and end cords 

    Parameters:
        start_lat: Start latitude.
        start_lon: Start longitude.
        end_lat: End latitude.
        end_lon: End longitude.
        step_size: Step size for grid cells.

    Returns: A list of tuples representing the midpoints of the grid cells.
    """

    midpoints=[]
    latitude = start_lat
    while (latitude + step_size <= end_lat):
        longitude = start_lon
        while (longitude + step_size <= end_lon):
            mid_lat = latitude + step_size / 2
            mid_lon = longitude + step_size / 2
            midpoints.append((round(mid_lat, 2), round(mid_lon, 2)))
            longitude += step_size
        latitude += step_size

    return midpoints

obstacle_indices, grid = detect_obstacles(start_coords, end_coords)
def get_obstacle_indices():
    return obstacle_indices, grid
obs, g = get_obstacle_indices()
print(obs)
