#3
# 用来根据领取频点以及PCI来匹配邻区cellid
import multiprocessing

import pandas as pd

from calculation.Distance import get_distance_hav


def matching(raw_data, fscdd):
    # 匹配单个样本的cellid, 由于邻区间存在频点与pci相同的情况，所以匹配得到的cellid存在相同的情况
    fscdd.sort_values(by=['pci', 'frequency'], inplace=True)
    neigh_pci = ['pci0', 'pci1', 'pci2', 'pci3', 'pci4', 'pci5']
    neigh_fre = ['frequency0', 'frequency1', 'frequency2', 'frequency3', 'frequency4', 'frequency5']
    neigh_cellid = ['cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4', 'cellid5']
    for cellid in neigh_cellid:
        raw_data[cellid] = None
    for index, row in raw_data.iterrows():  # 遍历每条记录
        cellid_used= [row.loc['servingcell']]
        for pci, fre, cellid in zip(neigh_pci, neigh_fre, neigh_cellid):  # 分别匹配6个邻区cellid
            if row.loc[pci] and row.loc[fre]:
                try:
                    candcell = fscdd[(fscdd.pci == row.loc[pci]) & (fscdd.frequency == row.loc[fre])][
                        ['cellid', 'longitude', 'latitude']]
                    candcell.drop(candcell[candcell.cellid.isin(cellid_used)].index, inplace=True)  # 排除服务小区
                    lat = fscdd[fscdd.cellid == row.loc['servingcell']]['latitude'].values[0]  # 服务小区纬度
                    lng = fscdd[fscdd.cellid == row.loc['servingcell']]['longitude'].values[0]  # 服务小区经度
                    if len(candcell) == 1 and \
                            get_distance_hav(candcell.latitude, candcell.longitude, lat, lng) < 3000:
                        raw_data.loc[index, cellid] = candcell.cellid.iloc[0]
                        cellid_used.append(candcell.cellid.iloc[0])
                    elif len(candcell) > 1:
                        candcell['temp_distance'] = candcell.apply(
                            lambda se: get_distance_hav(se.loc['latitude'], se.loc['longitude'], lat, lng), axis=1)
                        mindist = candcell.temp_distance.min()
                        if mindist < 3000:
                            bestindex = candcell[candcell.temp_distance == mindist].index.values[0]
                            raw_data.loc[index, cellid] = candcell.loc[bestindex]['cellid']
                            cellid_used.append(candcell.loc[bestindex]['cellid'])
                    else:
                        continue
                except:
                    continue
    return raw_data[['longitude', 'latitude', 'servingcell', 'cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4',
                     'cellid5', 'servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5']]


def multi_matching(raw_data, fscdd):
    # 多进程匹配
    cpus = multiprocessing.cpu_count() - 1
    length = raw_data.shape[0] // cpus
    results = []
    pool = multiprocessing.Pool(processes=cpus)
    for i in range(cpus):
        results.append(pool.apply_async(matching, (raw_data.iloc[length * i:length * (i + 1)], fscdd)))
    pool.close()
    pool.join()
    data = []
    for res in results:
        data.append(res.get())
    data_all = pd.concat(data, ignore_index=True)
    return data_all


if __name__ == "__main__":
    raw_data = pd.read_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile_m.csv')
    fscdd = pd.read_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\gongcanbiao\\fscdd_zhujiang.csv')
    data = multi_matching(raw_data, fscdd)
    data.to_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\merge_final1.csv', index=False)
