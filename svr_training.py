import multiprocessing

import pandas as pd
from sklearn.svm import SVR


class Training:
    """
    输入指纹库数据，然后对每个栅格的样本，分开进行经度和维度的训练
    """
    def __init__(self, xdrfingerprint):
        self.xdr = xdrfingerprint

    def train_helper(self, df_area):
        # 单个栅格训练，返回训练好的经度和纬度的SVR模型
        pX = df_area[['servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5', 'rsrp6', 'rsrp7']]
        py_lng = df_area['longitude']
        py_lat = df_area['latitude']
        svr_lng = SVR(kernel='rbf', C=0.001, gamma=0.5, epsilon=1e-12, max_iter=200000, tol=1e-12,
                      shrinking=False)
        svr_lat = SVR(kernel='rbf', C=0.001, gamma=0.5, epsilon=1e-12, max_iter=200000, tol=1e-12,
                      shrinking=False)
        svr_lng.fit(pX, py_lng)
        svr_lat.fit(pX, py_lat)
        return svr_lng, svr_lat

    def train(self, id):
        # 单个栅格进行训练（经度和纬度分开进行），参数表， 包含经（纬）度的拉个朗日乘子以及对应阈值b
        parameter = pd.DataFrame(columns=['areaid', 'sampleid', 'alpha_lng', 'b_lng', 'alpha_lat', 'b_lat'])
        df_area = self.xdr[self.xdr.areaid == id]
        df_area.fillna(value=0, inplace=True)
        svr_lng, svr_lat = self.train_helper(df_area)
        parameter['areaid']=df_area['areaid']
        parameter['sampleid'] = df_area['sampleid']
        parameter.index = range(parameter.shape[0])
        parameter.loc[svr_lat.support_, 'alpha_lat']=svr_lat.dual_coef_[0]
        parameter.loc[svr_lng.support_, 'alpha_lng']=svr_lng.dual_coef_[0]
        parameter['b_lng']=svr_lng.intercept_[0]
        parameter['b_lat'] = svr_lat.intercept_[0]
        parameter.fillna(value=0, inplace=True)   # 对非支持向量补0
        return parameter

    def multi_train(self):
        # 多进程训练(全核)
        areaids = self.xdr.areaid.unique()
        results = []
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        for id in areaids:
            results.append(pool.apply_async(self.train, (id,)))
        pool.close()
        pool.join()
        pars = []
        for res in results:
            pars.append(res.get())
        parameter_all = pd.concat(pars, ignore_index=True)
        parameter_all = parameter_all[['areaid','sampleid','alpha_lng','b_lng','alpha_lat','b_lat']] # 调整列名顺序
        return parameter_all


if __name__ == '__main__':
    xdrfingerprint = pd.read_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\train3.csv')
    xdrfingerprint.fillna(value=0, inplace=True)
    # xdrfingerprint = xdrfingerprint[xdrfingerprint.areaid==7408002558900]
    t = Training(xdrfingerprint)
    parameter = t.multi_train()
    parameter.to_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\parameter3.csv',index=False)
