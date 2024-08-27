import matplotlib.pyplot as plt
import csv
import re
from obstacles import get_obstacle_indices

obstacle_indices, grid = get_obstacle_indices()

def read_paths_from_csv(filename):
    paths = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse path from CSV row
            path_str = row['Path']
            # Extract tuples using regex
            matches = re.findall(r'\(([^)]+)\)', path_str)
            path = [tuple(map(float, match.split(', '))) for match in matches]
            paths.append(path)
    return paths

def plot_individual_paths(paths):
    for index, path in enumerate(paths):
        plt.figure(figsize=(10, 8))
        # Unzip the path into two lists: latitudes and longitudes
        lats, lons = zip(*path)
        plt.plot(lons, lats, marker='o', linestyle='-', label=f'Path {index + 1}')

        # Plot obstacles using the flattened grid index
        num_cols = len(grid[0])  # Number of columns in the grid

        for flat_index in obstacle_indices:
            # Convert flat index back to 2D grid coordinates
            i = flat_index // num_cols
            j = flat_index % num_cols
            lat, lon = grid[i][j]
            plt.fill(
                [lon - 0.015, lon + 0.015, lon + 0.015, lon - 0.015],
                [lat - 0.015, lat - 0.015, lat + 0.015, lat + 0.015],
                color='red', alpha=0.5, label='Obstacle' if flat_index == obstacle_indices[0] else ""
            )

        # Prevent the legend from showing "Obstacle" label multiple times
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Path {index + 1}')
        plt.grid(True)
        plt.show()

def main():
    # Read paths from CSV
    paths = read_paths_from_csv('aco_paths.csv')

    print(obstacle_indices)
    # Plot each path individually
    plot_individual_paths(paths)

if __name__ == "__main__":
    main()
