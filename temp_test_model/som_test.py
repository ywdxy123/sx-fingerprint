import pandas as pd
import numpy as np
from sompy.sompy import SOM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

p = pd.read_csv('D:\pycharm_project\\fingerprint\Road_test_data_lte\my_test\single_cell_test_data\p3.csv')
p.fillna(value=0, inplace=True)
pX = p[['servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5']]
pX=MinMaxScaler().fit_transform(pX)
py = p[['longitude', 'latitude']]
som = SOM((10, 10), pX)
# ims = []
# for i in range(1000):
#     m = som.train(10)
#     img = np.array(m.tolist(), dtype=np.uint8)
#     im = plt.imshow(m.tolist(), interpolation='none')#, animated=True)
#     ims.append([im])
# fig = plt.figure()
# ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)
# plt.show()
m = som.train(1000000)   # 自组织网络中每个网格有一个权值向量，该向量维度为输入维度
lnglat = defaultdict(lambda :[])
for i in range(p.shape[0]):
    print(pX[i,:], som._get_winner_node(pX[i,:]), m[i])
    lnglat[som._get_winner_node(pX[i,:])].append(list(p.iloc[i][['longitude', 'latitude']]))
print(lnglat)