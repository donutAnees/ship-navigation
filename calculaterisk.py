'''
Calculates the navigation risk using wind angle and wave angle that affect the movement of the ship.
'''

def find_relative_angles(ship_heading, wave_direction, wind_direction) -> tuple[float]:
    '''Calculates the angles that wind direction and wave direction make with the ship's direction.
        Returns:
            1. wind angle relative to the direction of the moving ship
            2. wave angle relative to the direction of the moving ship
        Parameters:
            ship_heading -> Direction that the ship's bow points at the given time
            wave_direction -> Direction of waves relative to true North
            wind_direction -> Direction of wind generated waves relative to true North
    '''
    # we check if the relative angle is greater than 180 and if so, we subtract the value from 360.
    # this is to ensure that the final value of the relative wind and wave angles are always between 0 to 180 degrees
    # this alteration helps consider the angles always within a line perpendicular to the ship's body

    wind_threshold = abs(ship_heading - wind_direction)
    if wind_threshold > 180:
        wind_angle = 360 - wind_threshold 
    else:
        wind_angle = wind_threshold

    wave_threshold = abs(ship_heading - wave_direction)
    if wave_threshold > 180:
        wave_angle = 360 - wave_threshold
    else:
        wave_angle = wave_threshold

    return (wind_angle, wave_angle)

def navigation_risk(wind_angle, wave_angle) -> tuple[float, int]:
    '''Calculates the ship's navigation risk due to the angles that the wind and wave make with respect to the ship's heading.
        Returns:
            1. combined navigation risk for the ship at a given point in the ocean
            2. a 0 (not risky) or 1 (risky) to indicate whether the current conditions pose a navigation risk
        Parameters:
            wind_angle -> Angle made by the wind with respect to the ship's movement
            wave_angle -> Angle made by the wave with respect to the ship's movement
    '''
    # consider the area as an xy-plane, taking the ship's heading along the x-axis
    # if the wind angle (or wave angle) is closer to the y-axis, it is considered more risky for the ship navigation
    # if the wind angle (or wave angle) is closer to the x-axis, it is considered less risky for the ship navigation
    
    wind_risk = abs(90 - wind_angle) # less than 45 degrees (risky), more than 45 degrees (not risky)
    wave_risk = abs(90 - wave_angle)

    total_risk = wind_risk + wave_risk
    # if even one of the parameters is below the required threshold then it must be risky for navigation
    if (wind_risk < 45 or wave_risk < 45):
        risky = 1 # conditions are risky
    else:
        risky = 0 # conditions are not risky
        
    return (total_risk, risky)
   