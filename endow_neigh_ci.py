import multiprocessing

import pandas as pd


class Preprocessing:
    # 将邻区的频点与PCI进行拼接作为邻区的识别id，用于建立初始指纹库以及对MR数据的预处理
    def __init__(self, df):
        self.df = df

    def _endowci_helper(self, df):
        pci_col = ['pci0', 'pci1', 'pci2', 'pci3', 'pci4', 'pci5', 'pci6', 'pci7']
        fre_col = ['frequency0', 'frequency1', 'frequency2', 'frequency3', 'frequency4',
                   'frequency5', 'frequency6', 'frequency7']
        cellid_col = ['cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4', 'cellid5', 'cellid6', 'cellid7']
        for ind in df.index:
            for fre, pci, cellid in zip(pci_col, fre_col, cellid_col):
                if not pd.isnull(df.loc[ind, fre]) and not pd.isnull(df.loc[ind, pci]):
                    df.loc[ind, cellid] = int(str(int(df.loc[ind, fre])) + str(int(df.loc[ind, pci])))
        return df

    def endowci(self):
        # 拼接邻区的频点和PCI作为小区的cellid
        cellid_col = ['cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4', 'cellid5', 'cellid6', 'cellid7']
        for cellid in cellid_col:
            self.df[cellid] = None
        cpus = multiprocessing.cpu_count() - 1
        length = self.df.shape[0] // cpus
        results = []
        pool = multiprocessing.Pool(processes=cpus)
        for i in range(cpus):
            results.append(pool.apply_async(self._endowci_helper, (self.df.iloc[length * i:length * (i + 1)],)))
        pool.close()
        pool.join()
        data = []
        for res in results:
            data.append(res.get())
        data_all = pd.concat(data, ignore_index=True)
        pool.close()
        pool.join()
        if ('longitude' in data_all.columns) and ('latitude' in data_all.columns): # 建立指纹库时使用
            data_all = data_all[
                ['longitude', 'latitude', 'servingcell', 'cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4',
                 'cellid5', 'cellid6', 'cellid7', 'servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4',
                 'rsrp5', 'rsrp6', 'rsrp7']]
        else:        # 预测MR记录的经纬度时使用
            data_all = data_all[
                ['servingcell', 'cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4',
                 'cellid5', 'cellid6', 'cellid7', 'servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4',
                 'rsrp5', 'rsrp6', 'rsrp7']]
        data_all['servingcell'] = self.df.servingcell.apply(lambda x: int(x))
        return data_all

    def clean(self):
        # 去除邻区cellid有重复的样本
        data = self.endowci()
        data_cell = data[['cellid0', 'cellid1', 'cellid2', 'cellid3', 'cellid4', 'cellid5', 'cellid6', 'cellid7']]
        count = pd.DataFrame(columns=['All', 'Unique'])
        count['All'] = data_cell.count(axis=1)
        count['Unique'] = data_cell.apply(lambda s: len(set(s.dropna())), axis=1)
        dropinds = count[count.All > count.Unique].index
        data.drop(dropinds, inplace=True)
        return data


if __name__ == '__main__':
    #file = pd.read_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\\UE_MR_test\mr_test_data.csv')
    file = pd.read_csv(r'C:\Users\user\Desktop\Project\Position_project\Fingerprint\Fingerprint_zhujiang\UE_MR_test\mr_data2.csv')
    file['pci6'] = None
    file['pci7'] = None
    file['frequency6'] = None
    file['frequency7'] = None
    file['rsrp6'] = None
    file['rsrp7'] = None
    pre = Preprocessing(file.iloc[:10])
    data = pre.clean()
    print(data.shape)
    #data.to_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\\UE_MR_test\mr_test_data_res.csv',index=False)
    data.to_csv(r'C:\Users\user\Desktop\Project\Position_project\Fingerprint\Fingerprint_zhujiang\UE_MR_test\1est.csv',index=False)
