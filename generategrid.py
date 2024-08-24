def generate_grid(start_lat, end_lat, start_lon, end_lon, step_deg):
    grid = []

    # Adjust step direction based on start and end latitudes
    if start_lat > end_lat:
        lat_step = -step_deg
    else:
        lat_step = step_deg

    # Adjust step direction based on start and end longitudes
    if start_lon > end_lon:
        lon_step = -step_deg
    else:
        lon_step = step_deg

    # Iterate over latitude from start to end with given step
    lat = start_lat
    while (lat_step > 0 and lat <= end_lat) or (lat_step < 0 and lat >= end_lat):
        row = []
        lon = start_lon
        while (lon_step > 0 and lon <= end_lon) or (lon_step < 0 and lon >= end_lon):
            row.append((round(lat, 2), round(lon, 2)))
            lon += lon_step
        grid.append(row)
        lat += lat_step

    return grid

def main():
    grid = generate_grid(9.6, 9.1 , 78.8, 80.2, 0.08)
    for row in grid:
        for pos in row:
            print(pos)

if __name__ == "__main__":
    main()

