'''
Calculates the navigation risk using wind angle and wave angle that affect the movement of the ship.
'''

def find_relative_angles(ship_heading, wave_direction, wind_direction) -> tuple[float]:
    '''Calculates the angles that wind direction and wave direction make with the ship's direction.
        Returns:
            wind angle and wave angle relative to the direction of the moving ship.
        Parameters:
            ship_heading -> Direction that the ship's bow points at the given time
            wave_direction -> Direction of waves relative to true North
            wind_direction -> Direction of wind generated waves relative to true North
    '''
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

        