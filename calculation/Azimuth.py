from math import sin, cos, atan2


def bearing(lat1, lon1, lat2, lon2):
    # 计算方向角
    lat1 = lat1 * 0.017453293
    lon1 = lon1 * 0.017453293
    lat2 = lat2 * 0.017453293
    lon2 = lon2 * 0.017453293
    dlon = lon2 - lon1
    b = atan2(sin(dlon) * cos(lat2), (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)))
    b = (b * 57.295779513082 + 360) % 360
    return b
