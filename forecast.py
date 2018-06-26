import math
import time
import multiprocessing
from collections import defaultdict

import pandas as pd


class Forecast:
    def __init__(self, xdrfingerprint, parameter, userdata):
        self.xdr = xdrfingerprint
        self.userdata = userdata
        self.para = parameter

    def get_cell_sample(self, record):
        # 根据服务小区id找到候选栅格(小区覆盖栅格中所有样本)
        return self.xdr[self.xdr.servingcell == record.loc['servingcell']]

    def cacu_euc_dis(self, sample, record):
        # 计算单条记录与指纹库下样本的欧式距离， 暂未考虑ta/aoa（注意6个邻区的排列顺序是不固定的）
        # 返回记录与每个样本的欧式距离平方
        dist = (record.loc['servingrsrp'] - sample.loc['servingrsrp']) ** 2
        cell_col = ['cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4', 'cellid5', 'cellid6', 'cellid7']
        rsrp_col = ['rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5', 'rsrp6', 'rsrp7']
        record_dict = defaultdict(lambda: 0)
        sample_dict = defaultdict(lambda: 0)
        for c, r in zip(cell_col, rsrp_col):
            if not pd.isnull(record.loc[c]):
                record_dict[record.loc[c]] = record.loc[r]
            if not pd.isnull(sample.loc[c]):
                sample_dict[sample.loc[c]] = sample.loc[r]
        common_keys = set(record_dict.keys()) & set(sample_dict.keys())
        for key in common_keys:
            dist += (record_dict[key] - sample_dict[key]) ** 2
        for s_key, s_value in sample_dict.items():
            if s_key not in common_keys:
                dist += s_value ** 2
        return dist

    def get_best_areaid(self, record):
        # 从候选栅格中挑选出最佳的栅格，并返回记录与栅格内所有样本的距离平方
        # 记录到栅格的距离定义为记录到栅格下样本的最小欧式距离
        lattice_dis = defaultdict(lambda: 0)
        lattice_dot = defaultdict(lambda: 0)
        df_cell = self.get_cell_sample(record)
        cand_areaid = df_cell.areaid.unique()  # 获取候选的areaid
        if len(cand_areaid) > 0:
            for item in cand_areaid:
                temp = df_cell[df_cell.areaid == item]  # 获取栅格下样本
                temp['dist'] = temp.apply(lambda s: self.cacu_euc_dis(s, record), axis=1)  # 计算记录与单个样本的欧式距离
                lattice_dot[item] = temp
                lattice_dis[item] = temp['dist'].min()
            best_areaid = min(lattice_dis, key=lattice_dis.get)  # 与记录最近的栅格最为最佳匹配栅格
            return lattice_dot[best_areaid], best_areaid
        else:
            return None

    def svr_predict(self, dot):
        # svr预测经纬度
        dot['kernel_dott'] = dot.dist.apply(lambda d: math.exp(-0.08 * d))
        merget = pd.merge(dot, self.para, on='sampleid')
        dot['kernel_dot'] = dot.dist.apply(lambda d: math.exp(-0.5 * d))
        merge = pd.merge(dot, self.para, on='sampleid')
        longitude = sum(merget.apply(lambda s: s.loc['kernel_dott'] * s.loc['alpha_lng'], axis=1)) + merget.iloc[0][
            'b_lng']
        latitude = sum(merge.apply(lambda s: s.loc['kernel_dot'] * s.loc['alpha_lat'], axis=1)) + merge.iloc[0]['b_lat']
        return longitude, latitude

    def single_predict(self, record):
        # 预测单条记录的经纬度
        res = self.get_best_areaid(record)
        if res is not None:
            dot, best_areaid = res
            return self.svr_predict(dot)
        else:
            return None

    def multi_predict(self):
        # 多进程预测
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
        results = defaultdict(lambda: 0)
        for index, row in self.userdata.iterrows():
            results[index] = pool.apply_async(self.single_predict, (row,))
        for key, value in results.items():
            lnglat = value.get()
            if lnglat is not None:
                self.userdata.loc[key, 'lng_pre'], self.userdata.loc[key, 'lat_pre'] = value.get()[0], value.get()[1]


if __name__ == '__main__':
    time_start = time.time()
    xdrfingerprint = pd.read_csv(
        'E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\train3.csv')
    parameter = pd.read_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\parameter3.csv')
    test_data = pd.read_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\test3.csv')
    # columns = ['servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5', 'rsrp6', 'rsrp7']
    # xdrfingerprint.fillna(value=0,inplace=True)
    # test_data.fillna(value=0,inplace=True)
    # xdrfingerprint[columns]=StandardScaler().fit_transform(xdrfingerprint[columns])
    # test_data[columns] =StandardScaler().fit_transform(test_data[columns])
    forecast = Forecast(xdrfingerprint, parameter, test_data)
    forecast.multi_predict()

    from calculation.residual_analysis import residues

    res_data = forecast.userdata[['servingcell', 'longitude', 'latitude', 'lng_pre', 'lat_pre']]
    res_data.to_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\test_res_4.csv', index=False)
    res_data.dropna(inplace=True)
    time_end = time.time()
    df1 = res_data[['longitude', 'latitude']]
    df2 = res_data[['lng_pre', 'lat_pre']]
    df2.columns = ['longitude', 'latitude']
    res = residues(df1, df2)
    print(res.dis_prop())
    print('totally cost', time_end - time_start)
    res.show()
