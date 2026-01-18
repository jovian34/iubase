def get_wind_description(cf, blowing):
    cf_offset = angle_difference(cf, blowing)
    if abs(cf_offset) <= 15:
        return "blowing out to centerfield"
    elif 15 < cf_offset <= 35:
        return "blowing out to left-centerfield"
    elif -15 > cf_offset >= -35:
        return "blowing out to right-centerfield"
    elif 35 < cf_offset <= 55:
        return "blowing out to left field"
    elif -35 > cf_offset >= -55:
        return "blowing out to right field"
    elif abs(cf_offset) >= 165:
        return "blowing in from centerfield"
    elif 165 > cf_offset >= 145:
        return "blowing in from right-centerfield"
    elif -165 < cf_offset <= -145:
        return "blowing in from left-centerfield"
    elif 145 > cf_offset >= 125:
        return "blowing in from right field"
    elif -145 < cf_offset <= -125:
        return "blowing in from left field"        
    elif 55 < cf_offset < 125:
        return "cross wind from right to left"
    elif -55 > cf_offset > -125:
        return "cross wind from left to right"
    else:
        raise ValueError
    
    
def angle_difference(angle_cf, angle_wind):
    # Calculate the initial difference
    difference = angle_cf - angle_wind

    # Normalize the difference to be within the range of 0 to 360 degrees
    normalized_difference = (difference + 360) % 360

    # Determine the direction, make negative for clock
    if normalized_difference > 180:
        angle_diff = -(360 - normalized_difference)
    else:
        angle_diff = normalized_difference

    return angle_diff