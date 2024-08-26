import matplotlib.pyplot as plt
import csv
import re

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
        '''if index !=99:
            continue'''
        plt.figure(figsize=(10, 8))
        # Unzip the path into two lists: latitudes and longitudes
        lats, lons = zip(*path)
        plt.plot(lons, lats, marker='o', linestyle='-', label=f'Path {index + 1}')
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Path {index + 1}')
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    # Read paths from CSV
    paths = read_paths_from_csv('aco_paths.csv')
    
    # Plot each path individually
    plot_individual_paths(paths)

if __name__ == "__main__":
    main()
