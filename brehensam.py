"""
This function is not used
"""


def bresenham_algorithm(lat1,lon1,lat2,lon2,start_lat1,start_lon2,step,grid_rows,grid_cols):
    '''
    Finds all the grids which touches the path of the ship between two coordinates
    Returns:
        A list of indexes (row, column) in the grid where the ship's path intersects.
    Parameters:
        lat1: The starting latitude of the path.
        lat2: The ending latitude of the path.
        lon1: The starting longitude of the path.
        lon2: The ending longitude of the path.
        start_lat1: The starting latitude of the grid.
        start_lon2: The starting longitude of the grid.
        step: The size of each grid.
        grid_point_rows: The number of rows of points in the grid.
        grid_point_cols: The number of cols of points in the grid.
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
    ### with no consequence. D is nothing but the difference between the current point and the next point
    ### mid.

    ### One thing to note here is that closest grids are returned here not all the grids which touch the line
    ### to make we consider all the grids, we modify this algorithm, we consider both (x, y) and (x, y + 1) 
    ### since the line will pass through both, if its not passing through the middle or if is within (x, y).
    ### Therefore if (x, y+1) is closer then we also consider (x, y) this is implemented for all the directions 
    ### But this is cause issue for lines passing through integer points like (4,5) therefore for such points 
    ### we do not include (x, y)

    ### To check if the current point the line passing through is a integer point, we do

    ### The algorithm can be extended to cover slopes between 0 and -1 by checking whether y needs to increase or decrease
    ### By switching the x and y axis an implementation for positive or negative steep slopes
    
    ### Initially normalize the lat and lon to integer coordinates, this is done by comparing with the start lat, lon
    # Convert lat/lon to grid indices
    x0 = int((lat1 - start_lat1) / step)
    y0 = int((lon1 - start_lon2) / step)
    x1 = int((lat2 - start_lat1) / step)
    y1 = int((lon2 - start_lon2) / step)


    if abs(y1 - y0) < abs(x1 - x0):
        if lat1 > lat2:
            direction = 1  # Slanting from right to left
            grids = helper_line_low(x1, y1, x0, y0, grid_rows, grid_cols, direction)
        else:
            direction = 0  # Slanting from left to right
            grids = helper_line_low(x0, y0, x1, y1, grid_rows, grid_cols, direction)
    else:
        if lon1 > lon2:
            direction = 1  # Slanting from right to left
            grids = helper_line_high(x1, y1, x0, y0, grid_rows, grid_cols, direction)
        else:
            direction = 0  # Slanting from left to right
            grids = helper_line_high(x0, y0, x1, y1, grid_rows, grid_cols, direction)

    return grids

def get_grid_identifier(x, y, grid_point_rows, grid_point_cols, direction, point_location):
    """
    Calculate the grid identifier based on coordinates (x, y).
    If direction is 1 line slants goes from left to right
        If point_location is at the top then bottom left grid is considered from that point
        If point_location is at the bottom then top right grid is considered from that point
    If direction is 0 line slants goes from right to left

    Here True is above and False is below the line for point_location

    """
    # How our grid looks like, here (0,6) (1,6) (0,5) (1,5) forms one grid
    # (0,6) (1,6) (2,6) (3,6)
    # (0,5) (1,5) (2,5) (3,5)
    # (0,4) (1,4) (2,4) (3,4)
    # (0,3) (1,3) (2,3) (3,3)
    # (0,2) (1,2) (2,2) (3,2)
    # (0,1) (1,1) (2,1) (3,1)
    # (0,0) (1,0) (2,0) (3,0)

    grid_index = 0
    if(direction == 1):
        if(point_location == False):
            # Bottom Left
            grid_index = (((grid_point_rows - 1) - y - 1)) * (grid_point_cols - 1) + x + 1
        else:
            # Top Right
            # Just decrement top right x and y by 1 to get the lower left and compute like pos = 1
            y = y - 1
            x = x - 1
            grid_index = (((grid_point_rows - 1) - y - 1)) * (grid_point_cols - 1) + x + 1
    if(direction == 0):
        if (point_location == True):  # Top left
            y = y - 1
            grid_index = (((grid_point_rows - 1) - y - 1)) * (grid_point_cols - 1) + x + 1
        else:  # Bottom right
            x = x - 1
            grid_index = (((grid_point_rows - 1) - y - 1)) * (grid_point_cols - 1) + x + 1
    print("Pos",point_location,"direction",direction,"grid",grid_index)
    return grid_index

def helper_line_low(x0, y0, x1, y1, grid_point_rows, grid_point_cols, direction):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y0
    grids = []
    for x in range(x0, x1):
        if not is_point_on_line_segment(x0, y0, x1, y1, x, y):
            grid = get_grid_identifier(x, y, grid_point_rows, grid_point_cols, direction, position)
            # Dont add if Duplicate
            if len(grids) == 0:
                grids.append(grid)
            else:
                if(grids[-1] != grid):
                    grids.append(grid)
        if D > 0:
            if not is_point_on_line_segment(x0, y0, x1, y1, x, y):
                print("New",x+1,y)
                grid = get_grid_identifier(x + 1, y, grid_point_rows, grid_point_cols, direction, position)
                if(grids[-1] != grid):
                    grids.append(grid)
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2 * dy
    return grids

def helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols, direction):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x0
    grids = []
    position = False
    ### Whenever the point changes the position between top and bottom, we flip our boolean, also whenever our line passes through a point
    for y in range(y0, y1):
        print(x,y)
        if not is_point_on_line_segment(x0, y0, x1, y1, x, y):
            grid = get_grid_identifier(x, y, grid_point_rows, grid_point_cols, direction, 1)
            # Dont add if Duplicate
            if len(grids) == 0:
                grids.append(grid)
            else:
                if(grids[-1] != grid):
                    grids.append(grid)
                position = not position
        else:
            position = not position
        if D > 0:
            if not is_point_on_line_segment(x0, y0, x1, y1, x, y):
                print(x,y+1)
                grid = get_grid_identifier(x, y + 1, grid_point_rows, grid_point_cols, direction, 0)
                if(grids[-1] != grid):
                    grids.append(grid)
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2 * dx
    return grids

def is_point_on_line_segment(x1, y1, x2, y2, px, py):
    """
    Check if a point (px, py) is on the line segment between (x1, y1) and (x2, y2).

    Parameters:
    x1, y1: Coordinates of the first point.
    x2, y2: Coordinates of the second point.
    px, py: Coordinates of the point to check.

    Returns:
    bool: True if the point (px, py) is on the line segment, False otherwise.
    """
    # Check if the point (px, py) is collinear with (x1, y1) and (x2, y2)
    # Use cross product to determine if the points are collinear
    # (x2 - x1) * (py - y1) == (px - x1) * (y2 - y1) indicates collinearity
    if (x2 - x1) * (py - y1) != (px - x1) * (y2 - y1):
        return False
    
    # Check if the point is within the bounds of the line segment
    if (min(x1, x2) <= px <= max(x1, x2)) and (min(y1, y2) <= py <= max(y1, y2)):
        return True
    
    return False