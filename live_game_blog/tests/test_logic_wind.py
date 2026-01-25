import pytest

from live_game_blog.logic import wind

testdata = [
    (45, 41, "blowing out to centerfield"),
    (0, 355, "blowing out to centerfield"),
    (90, 99, "blowing out to centerfield"),
    (135, 127, "blowing out to centerfield"),
    (180, 190, "blowing out to centerfield"),
    (270, 259, "blowing out to centerfield"),
    (320, 333, "blowing out to centerfield"),
    (45, 20, "blowing out to left-centerfield"),
    (90, 70, "blowing out to left-centerfield"),
    (135, 115, "blowing out to left-centerfield"),
    (180, 160, "blowing out to left-centerfield"),
    (270, 250, "blowing out to left-centerfield"),
    (345, 327, "blowing out to left-centerfield"),
    (45, 65, "blowing out to right-centerfield"),
    (45, 81, "blowing out to right field"),
    (45, 99, "blowing out to right field"),
    (45, 9, "blowing out to left field"),
    (45, 351, "blowing out to left field"),
    (270, 290, "blowing out to right-centerfield"),
    (359, 26, "blowing out to right-centerfield"),
    (45, 125, "blowing across the field from left to right"),
    (315, 255, "blowing across the field from right to left"),
]


@pytest.mark.parametrize("cf,blowing,expected", testdata)
def test_get_wind_direction(cf, blowing, expected):
    assert wind.get_wind_description(cf, blowing) == expected


testdata_angles = [
    (0, 180),
    (45, 225),
    (120, 300),
    (170, 350),
    (190, 10),
    (270, 90),
    (300, 120),
]


@pytest.mark.parametrize("wind_dir,blowing", testdata_angles)
def test_covert_wind_direction_to_opposite_angle(wind_dir, blowing):
    assert wind.convert_wind_direction_to_opposite(wind_dir) == blowing