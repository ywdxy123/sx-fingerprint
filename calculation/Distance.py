from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS = 6371  # 地球平均半径，6371km


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lon0, lat1, lon1):
    # 根据经纬度计算距离，单位m
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lon0)
    lng1 = radians(lon1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h)) * 1000

    return distance

if __name__ == '__main__':
    dist = get_distance_hav(23.12443,113.33325,23.12497888,113.3328001)
    print(dist)
