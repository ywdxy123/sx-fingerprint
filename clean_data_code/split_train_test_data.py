#5
# 将数据切分为训练数据集与测试数据集
import pandas as pd
import numpy as np
outfile = pd.read_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile_final_m_out.csv')
inds = np.array(outfile.index)
split_point = int(outfile.shape[0]*0.1)
np.random.shuffle(inds)
test_inds = inds[:split_point]
train_inds = inds[split_point:]
outfile.iloc[test_inds].to_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\test3.csv',index=False)
outfile.iloc[train_inds].to_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\train3.csv',index=False)
