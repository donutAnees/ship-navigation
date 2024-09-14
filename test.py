import math
def calculate_distance(x1, y1, x2, y2):
    # Euclidean Formula
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def get_grid_identifier(x, y, grid_point_rows,grid_point_cols):
    """
    Calculate the grid identifier based on coordinates (x, y).
    Given a point on the top right corner of a grid, we return the grid index
    (0,0) (0,1) 
         1    
    (1,0) (1,1)
    For the above grid, if we input top index (0,1) we get the grid index 1
    """
    # Top Right in cartesian, bottom right in our grid
    grid_index = ((grid_point_rows - 1) * (y - 1)) + x
    return grid_index
def helper_line_low(x0, y0, x1, y1, grid_point_rows, grid_point_cols):
    grids = []
    distances = []
    # Calculate the slope (m)
    m = (y1 - y0) / (x1 - x0)

    # xi stores how we want to traverse in the for loop, forward or backward
    xi = 1 # If 1 we go up
    if(m < 0):
        xi = -1 # If -1 we go down

    offset = 0
    # If we reversing, we get the top left point therefore we use this offset to add 1 to x if we are
    if(m < 0):
        offset = 1

    # Calculate the y-intercept (c)
    c = y0 - m * x0

    # Tracks the previous point
    prev_x, prev_y = x0, y0 

    # There will be the case where a line passes through 2 grids at once, to identify such we need to iterate though y and see
    # if the line passes though this and the x is a float, if it is a float it means the line cuts in the middle. To avoid 
    # unneccesary iteration we can just check y, whenever it crosses some integer value
    for x in range(x0+xi,x1+xi,xi):
        # Calculate y for the given x
        y = m * x + c
        # Check if the line cuts two grids at the same time, calculate for both grids if it does
        # int(y) != y is for seeing if the line is going through values like (2,3) (1,1) where y is integer in such case we can ignore, since it is passing through a integer point
        # rather than a float point which is what cuts through 2 grids
        if( int(prev_y) < int(y) and x != x1 and int(y) != y): # Suppose previous y is 2.9 and current y is 3.1 then there is an intersection between
            # suppose y = 2.2 and x intersection is 8.5
            y_floor = math.floor(y) # Stores the floor of y = 2, we use this to find the bottom grid
            x_inter = (y_floor - c)/ m # Stores the intersection = 8.5
            # Gets the first grid, top right point will be current x = 9 and y = 2
            grids.append(get_grid_identifier(x + offset,y_floor,grid_point_rows,grid_point_cols))  
            distances.append(calculate_distance(prev_x, prev_y, x_inter, y_floor)) 
            # Gets the second grid, top right point will be current x = 9 and y = 3
            grids.append(get_grid_identifier(x + offset,math.ceil(y),grid_point_rows,grid_point_cols)) 
            distances.append(calculate_distance(x_inter, y_floor, x, y)) 
        # Calculate for one grid
        else:
            grids.append(get_grid_identifier(x + offset,math.ceil(y),grid_point_rows,grid_point_cols)) 
            distances.append(calculate_distance(prev_x, prev_y, x, y)) 
        prev_x = x
        prev_y = y

    return grids , distances  
# Test for helper_line_low (simple case with no grid intersection)


def helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols):
    grids = []
    distances = []
    # Calculate the slope (m)
    m = (y1 - y0) / (x1 - x0)

    # yi stores how we want to traverse in the for loop, forward or backward
    yi = 1 # If 1 we go up
    if(m < 0):
        yi = -1 # If -1 we go down

    offset = 1
    # If we reversing, we get the bottom right point therefore we use this offset to add 1 to y if we are
    if(m < 0):
        offset = 0

    # Calculate the y-intercept (c)
    c = y0 - m * x0

    # Tracks the previous point to calculate the distance
    prev_x, prev_y = x0, y0 

   # Iterate over y from y0 to y1 (going downwards)
    for y in range(y0, y1, yi):
        # Calculate x for the given y
        x = (y - c) / m

        # Check if the line cuts two grids at the same time
        if (int(prev_x) < int(x) and int(x) != x):
            # suppose x = 1.2 and y intersection is 3.5
            x_floor = math.floor(x) # Stores the floor of x = 1
            y_inter = m * x_floor + c # Stores the intersection = 3.5
            # Gets the first grid, top right point will be current x = 1 and y = 4
            grids.append(get_grid_identifier(x_floor + 1, y, grid_point_rows, grid_point_cols))
            distances.append(calculate_distance(prev_x, prev_y, x_floor, y_inter)) 
            # Gets the second grid, top right point will be current x = 2 and y = 4
            grids.append(get_grid_identifier(x_floor + 1, y + 1, grid_point_rows, grid_point_cols)) 
            distances.append(calculate_distance(x_floor, y_inter, x, y)) 
        else:
            grids.append(get_grid_identifier(math.floor(x) + 1, y + offset, grid_point_rows, grid_point_cols))
            distances.append(calculate_distance(prev_x, prev_y, x, y))
        prev_x = x
        prev_y = y

    return grids, distances


"test case 1" -"positive slope"

x0, y0 = 0, 0
x1, y1 = 5, 3
grid_point_rows, grid_point_cols = 3, 3
grids, distances = helper_line_low(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
print("Grids",grids,"Distance",distances)

''' Manually verifying the grids passes through 
(0,0),(1,0.6),(2,1.2),(3,1.8),(4,2.4),(5,3)
total 7 grids'''

"Grids: [1, 2, 4, 5, 6, 8, 9] Distance: [1.16619037896906, 0.7774602526460401, 0.38873012632301995, 1.16619037896906, 0.38873012632302023, 0.7774602526460399, 1.1661903789690602]"

"test case 2" -"positve slope"

x0, y0 = 0, 0
x1, y1 = 4, 3
grid_point_rows, grid_point_cols = 3, 3
grids, distances = helper_line_low(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
print("Grids:" ,grids,"Distance:",distances)


''' Manually verifying the grids passes through 
(0,0),(1,0.75),(2,1.5),(3,2.25),(4,3)
totally 6 grids'''

"Grids: [1, 2, 4, 5, 7, 8] Distance: [1.25, 0.4166666666666666, 0.8333333333333334, 0.8333333333333331, 0.4166666666666668, 1.25]"

"test case-3 high"

def test_helper_line_high():
    x0, y0 = 1, 1
    x1, y1 = 2, 4
    grid_point_rows = 4
    grid_point_cols = 5

    grids, distances = helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
    print(grids,distances)


test_helper_line_high()
'''[5, 8, 11] [0.0, 1.0540925533894598, 1.0540925533894598]'''

"test case 4"-"slope 0 "

def test_helper_line_high():
    x0, y0 = 2, 1
    x1, y1 = 2,4
    grid_point_rows = 4
    grid_point_cols = 5

    grids, distances = helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
    print(grids,distances)


test_helper_line_high()
"zero division error"

"test case 5"-"negative slope(high)"

x0, y0 = 1, 4
x1, y1 = 4, 1
grid_point_rows, grid_point_cols = 4, 5
grids, distances = helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
print("Grids",grids,"Distance",distances)  
'''Grids [11, 9, 7] Distance [0.0, 1.4142135623730951, 1.4142135623730951]'''


"chatgpt test cases "
"test case 1-more vertical negative slope "
x0, y0 = 3, 6
x1, y1 = 6, 3
grid_point_rows, grid_point_cols = 4, 5
grids, distances = helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
print("Grids",grids,"Distance",distances)    
"Grids [19, 17, 15] Distance [0.0, 1.4142135623730951, 1.4142135623730951]"


"test case 2-more vertical negative slope"
x0, y0 = 4, 4
x1, y1 = 7, 1
grid_point_rows, grid_point_cols = 4, 5
grids, distances = helper_line_high(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
print("Grids",grids,"Distance",distances)    

"Grids [14, 12, 10] Distance [0.0, 1.4142135623730951, 1.4142135623730951]"


"test case 3-more horizontal(low)"
x0, y0 = 2, 3
x1, y1 = 7, 3
grid_point_rows, grid_point_cols = 4, 5
grids, distances = helper_line_low(x0, y0, x1, y1, grid_point_rows, grid_point_cols)
print("Grids",grids,"Distance",distances) 

"Grids [9, 10, 11, 12, 13] Distance [1.0, 1.0, 1.0, 1.0, 1.0]"