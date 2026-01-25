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
        return "blowing across the field from right to left"
    elif -55 > cf_offset > -125:
        return "blowing across the field from left to right"
    else:
        raise ValueError
    

def convert_wind_direction_to_opposite(angle):
    angle = angle % 360
    return (angle + 180) % 360     


def angle_difference(angle_cf, angle_wind):
    difference = angle_cf - angle_wind
    normalized_difference = (difference + 360) % 360
    if normalized_difference > 180:
        angle_diff = -(360 - normalized_difference)
    else:
        angle_diff = normalized_difference

    return angle_diff
