#1
# 读取原始路测数据并进行合并
# unique_cell为路测数据中存在的不重复小区id数据
import os
import pandas as pd
path = 'D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\lte_raw_data'
os.chdir(path)
fp = os.listdir()
mergefile = pd.read_csv(fp[0])
for i in range(1, len(fp)):
    mergefile = mergefile.append(pd.read_csv(fp[i]))
mergefile.to_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile1.csv',index=False)
unique_cell = mergefile[['LTE Cell ID','LTE PCI']]
unique_cell.columns = ['servingcell','servingpci']
unique_cell.dropna(inplace=True)
unique_cell.drop_duplicates(inplace=True)
unique_cell.to_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\\unique_cell1.csv',index=False, float_format='%0.0f')