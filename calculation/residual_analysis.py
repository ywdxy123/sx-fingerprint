import matplotlib.pyplot as plt
import pandas as pd

from calculation.Distance import get_distance_hav


class residues:
    # 预测结果的残差分析
    def __init__(self, df1, df2):
        self.rpos = df1
        self.ppos = df2

    def lng_residues(self):
        # 经度的残差（乘以1e4）分析
        lng_res = (self.rpos['longitude'] - self.ppos['longitude']) * 1e4
        plt.subplot(221)
        plt.scatter(lng_res.index, lng_res.values, marker='+')

    def lat_residues(self):
        # 纬度的残差（乘以1e4）分析
        lat_res = (self.rpos['latitude'] - self.ppos['latitude']) * 1e4
        plt.subplot(222)
        plt.scatter(lat_res.index, lat_res.values, marker='*')

    def distance(self):
        df = pd.concat([self.rpos, self.ppos], axis=1)
        df.columns = ['lng1', 'lat1','lng2', 'lat2']
        df['dis_res'] = df.apply(
            lambda s: get_distance_hav(s.loc['lat1'], s.loc['lng1'], s.loc['lat2'], s.loc['lng2']), axis=1)
        return df

    def dis_residues(self):
        # 距离的残差分析
        df = self.distance()
        plt.subplot(212)
        plt.scatter(df.index, df.dis_res, marker='o')

    def show(self):
        self.lng_residues()
        self.lat_residues()
        self.dis_residues()
        plt.show()

    def dis_prop(self):
        # 各区间内比例分析
        df = self.distance()
        p = {'10m以内': 0, '10~20m': 0, '20~50m': 0, '50~100m': 0, '100m以上': 0, '预测失败': 0}
        p['10m以内'] = df[df.dis_res <= 10].shape[0] / df.shape[0]
        p['10~20m'] = df[(df.dis_res > 10) & (df.dis_res <= 20)].shape[0] / df.shape[0]
        p['20~50m'] = df[(df.dis_res > 20) & (df.dis_res <= 50)].shape[0] / df.shape[0]
        p['50~100m'] = df[(df.dis_res > 50) & (df.dis_res <= 100)].shape[0] / df.shape[0]
        p['100m以上'] = df[df.dis_res > 100].shape[0] / df.shape[0]
        p['预测失败'] = df[df.dis_res.isnull() == True].shape[0] / df.shape[0]
        return p

