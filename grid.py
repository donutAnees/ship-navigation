from shipSpeed import shipSpeed
import math

def generate_grid(start_lat, end_lat, start_lon, end_lon, step_deg):
    """
    Generates a grid of geographical coordinates (latitude, longitude) based on the specified start and end points 
    with a given step size in degrees. If the step is 0.08 degree then the grid would, account for 0.04 degree coverage.
    Parameters:
        start_lat: The starting latitude.
        end_lat: The ending latitude.
        start_lon: The starting longitude.
        end_lon: The ending longitude.
        step_deg: The step size in degrees for latitude and longitude.
    Returns:
        list: A 2D list (grid) containing tuples of (latitude, longitude).
    """
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

def calculate_orientation(grid, path):
    '''
    Calculates the orientation of the ship with respect to north in each grid, that is the bearing angle.
    Representation of the 4 direction in degree
        0 degrees: North
        90 degrees: East
        180 degrees: South
        270 degrees: West
    Returns:
        A grid which contains the orientation of the ship, if the ship doesn't travel through that grid, then it is represented as -1
    Parameter:
        grid -> The input grid containing latitude and longitude points.
        path -> The path of the ship as a list of (latitude, longitude). 
    '''
    orientations_grid = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(path) - 1):
        lat1, lon1 = path[i]
        lat2, lon2 = path[i+1]

        # https://en.wikipedia.org/wiki/Atan2 can be used to find the angle measure (in radians, between the positive x-axis 
        # and the ray from the origin to the point (x,y). https://www.movable-type.co.uk/scripts/latlong.html formula taken 
        # from here

        y = math.sin(lon1 - lon2) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)
        thetha = math.atan2(y, x) # In radian
        brng = (thetha * 180 / math.pi + 360) % 360 # In degree

        # Find the index of the lat lon for start and end in the grid

def bresenham_algorithm(lat1,lon1,lat2,lon2):
    '''
    Finds all the grids which touches the path of the ship between two coordinates
    Returns:
        A list of indexes in the grid where the ship meets.
    Parameters:
        start_lat: The starting latitude.
        end_lat: The ending latitude.
        start_lon: The starting longitude.
        end_lon: The ending longitude.
    '''
    ### Bresenham's algorithmc can be used here, which calculates which pixels should be 
    ### filled to best approximate a straight line between two endpoints. The algorithm 
    ### operates by iterating over each column (or row, depending on the line's slope) and 
    ### deciding whether to increment the row position based on an error term. This is better
    ### compared to finding the slope and multiplying as it requires floating point. This error 
    ### term tracks the difference between the actual line position and the nearest pixel. 
    ### When the error exceeds a threshold, the y-coordinate is incremented, and the error 
    ### term is adjusted. We use this to find all the grids that touches the line.

    ### The slope-intercept form of a line is written as a function of both X and Y, if for 
    ### a given point, this evaluates to 0, then that point is in the line.

    ### Algorithm: Line from Left to Right
    ### Given the constraint that the line has a slope less than or equal to 1, the algorithm 
    ### has two candidate pixels to choose from for the next step as we move to the right by
    ### one column from x to x + 1. These candidate pixels are: (x+1,y) and (x+1,y+1), rather 
    ### than evaluating both, (x+1,y + 1/2) mid is found out, if the value of this is positive 
    ### then the ideal line is below the midpoint and closer to the candidate point (x+1,y+1) 
    ### the y coordinate should increase. Otherwise, the ideal line passes through or above 
    ### the midpoint, and the y coordinate should stay the same.

    ### Alternatively, the difference between points can be used instead of evaluating f(x,y) at midpoints. 
    ### This alternative method allows for integer-only arithmetic, which is generally faster than using 
    ### floating-point arithmetic. This D can be derived D = Δy - 1/2Δx. Based upon his, if D is positive
    ### then (x+1, y+1) is chosen, else (x+1, y) is chosen. The only overhead here is the 1/2 calculation,
    ### since all we care about is sign of the accumulated difference, everything can be multiplied by 2
    ### with no consequence.

    ### The algorithm can be extended to cover slopes between 0 and -1 by checking whether y needs to increase or decrease
    ### By switching the x and y axis an implementation for positive or negative steep slopes
    if abs(lon2 - lon1) < abs(lat2 - lat1):
        if lat1 > lat2:
            points = helper_line_low(lat2, lon2, lat1, lon1)
        else:
            points = helper_line_low(lat1, lon1, lat2, lon2)
    else:
        if lon1 > lon2:
            points = helper_line_hight(lat2, lon2, lat1, lon1)
        else:
            points = helper_line_hight(lat1, lon1, lat2, lon2)

    ### One thing to note here is that points are returned here, not the grids we have to find the grid 
    ### based on the orientation of the line 
    return points


def helper_line_low(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y0
    points = []
    for x in range(x0,x1+1):
        points.append((x,y))
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2*dy
    return points

def helper_line_hight(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x0
    points = []
    for y in range(y0,y1+1):
        points.append((x,y))
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2*dx   
    return points


def main():
    # Generate grid with 0.08 degree step
    # grid = generate_grid(9.6, 9.1 , 78.8, 80.2, 0.08)
    # for row in grid:
    #     for pos in row:
    #         print(pos)

    # Testing bresenham
    # Get the list of points that the line passes through
    points = bresenham_algorithm(13, 11, 10, 17)

    # Print the points
    print("Points the line passes through:")
    for point in points:
        print(point)

    #ship speed calculation
    #def __init__(self, ship_speed, wave_height, displacement, k1, k2, k3, k4, wind_speed, angle):
    # ship = shipSpeed( 30, 1.26, 200000,  1.08, 0.126, 2.77, 2.33, 15, 30)
    # speed = ship.getSpeed()
    # print(speed)

if __name__ == "__main__":
    main()

