#4
from math import sin, cos, tan, pi, sqrt


class Lattice:
    # 划分栅格，将样本经纬度转换为UTM坐标系下的坐标，对UTM坐标系下的坐标进行处理合并，作为该样本所归属的栅格id
    eqr = 6378137
    plr = 6356752.314
    k0 = 0.9996
    e = sqrt(1 - (plr / eqr) ** 2)
    elsq = e ** 2 / (1 - e ** 2)
    A0 = 6367449.146
    B0 = 16038.42955
    C0 = 16.83261333
    D0 = 0.021984404
    E0 = 0.000312705
    s1 = 4.84814e-06

    def __init__(self, modify_data):
        self.data = modify_data

    def get_areaid(self, lat, lng):
        lat = lat * pi / 180
        if lng < 0:
            var1 = int((180 + lng) / 6) + 1
        else:
            var1 = int(lng / 6) + 31
        var2 = 6 * var1 - 183
        var3 = lng - var2
        p = var3 * 3600 / 10000
        s = Lattice.A0 * lat - Lattice.B0 * sin(2 * lat) + Lattice.C0 * sin(4 * lat) - Lattice.D0 * sin(6 * lat) + Lattice.E0 * sin(
            8 * lat)
        nu = Lattice.eqr / sqrt(1 - (Lattice.e * sin(lat)) ** 2)
        K1 = s * Lattice.k0
        K2 = nu * sin(lat) * cos(lat) * (Lattice.s1 ** 2) * Lattice.k0 * 5e7
        K3 = ((Lattice.s1 ** 4) * nu * sin(lat) * (cos(lat) ** 3)) / 24 * (5 - tan(lat) ** 2 + 9 * Lattice.elsq * (
                cos(lat) ** 2) + 4 * (Lattice.elsq ** 2) * (cos(lat) ** 4)) * Lattice.k0 * 1e16
        K4 = nu * cos(lat) * Lattice.s1 * Lattice.k0 * 1e4
        K5 = ((Lattice.s1 * cos(lat)) ** 3) * (nu / 6) * (1 - tan(lat) ** 2 + Lattice.elsq * (cos(lat) ** 2)) * Lattice.k0 * 1e12
        easting = 5e5 + (K4 * p + K5 * (p ** 3))
        northing = K1 + K2 * p * p + K3 * (p ** 4)

        if lat < 0:
            northing = 1e7 + northing
        easting = easting - easting % 100
        northing = northing - northing % 100
        areaid = str(int(easting)) + str(int(northing))
        return areaid

    def divide(self):
        self.data['areaid'] = self.data.apply(lambda s: self.get_areaid(s.loc['latitude'], s.loc['longitude']), axis=1)
        self.data['sampleid'] = self.data.index
        self.data = self.data[['areaid', 'sampleid', 'longitude', 'latitude', 'servingcell', 'cellid0',
                               'cellid1', 'cellid2', 'cellid3', 'cellid4', 'cellid5', 'cellid6', 'cellid7',
                               'servingrsrp',
                               'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5', 'rsrp6', 'rsrp7']]


if __name__ == '__main__':
    import pandas as pd

    data = pd.read_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile_final_m.csv')
    data['cellid6']=None
    data['cellid7']=None
    data['rsrp6']=None
    data['rsrp7']=None
    # data = data.iloc[:2]
    grid = Lattice(data)
    grid.divide()
    grid.data.to_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile_final_m_out.csv',
                     index=False)
