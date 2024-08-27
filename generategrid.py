from shipSpeed import shipSpeed

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
    # Generate grid with 0.08 degree step
    grid = generate_grid(9.6, 9.1, 79.2, 79.9, 0.08)
    for row in grid:
        for pos in row:
            print(pos)

    #ship speed calculation
    #def __init__(self, ship_speed, wave_height, displacement, k1, k2, k3, k4, wind_speed, angle):
    ship = shipSpeed( 30, 1.26, 200000,  1.08, 0.126, 2.77, 2.33, 15, 30)
    speed = ship.getSpeed()
    print(speed)

if __name__ == "__main__":
    main()
