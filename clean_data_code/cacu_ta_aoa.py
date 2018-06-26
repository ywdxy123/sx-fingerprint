from calculation import Azimuth, Distance


def caculating(raw_data):
    # 计算样本的ta和aoa
    raw_data['ta'] = raw_data.apply(
        lambda s: round(Distance.get_distance_hav(s.Latitude, s.Longitude, s.latitude, s.longitude) / 76.98, 0), axis=1)
    raw_data['aoa'] = raw_data.apply(
        lambda s: Azimuth.bearing(s.Latitude, s.Longitude, s.latitude, s.longitude), axis=1)
    return raw_data