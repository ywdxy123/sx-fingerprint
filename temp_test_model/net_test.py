import pandas as pd
from pybrain3.datasets.supervised import SupervisedDataSet
from pybrain3.structure.modules.tanhlayer import TanhLayer
from pybrain3.supervised.trainers.backprop import BackpropTrainer
from pybrain3.tools.shortcuts import buildNetwork
from sklearn.model_selection import train_test_split

p = pd.read_csv('D:\pycharm_project\\fingerprint\Road_test_data_lte\my_test\single_cell_test_data\p3.csv')
p.fillna(value=0, inplace=True)
pX = p[['servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5']]
py = p[['longitude', 'latitude']]
pX_train, pX_test, py_train, py_test = train_test_split(pX, py, test_size=0.1)
# 构建训练与测试数据集
training = SupervisedDataSet(pX_train.shape[1], 2)
for i in range(pX_train.shape[0]):
    training.addSample(pX_train.iloc[i], py_train.iloc[i])
testing = SupervisedDataSet(pX_test.shape[1], 2)
for i in range(pX_test.shape[0]):
    testing.addSample(pX_test.iloc[i], py_test.iloc[i])
# 构建人工神经外网络
net = buildNetwork(pX_train.shape[1], 4, 2, hiddenclass=TanhLayer, bias=True)
trainer = BackpropTrainer(net, training, learningrate=0.01)
trainer.trainEpochs(epochs=100)
predictions = net.activateOnDataset(dataset=testing)
y_predict = pd.DataFrame(predictions, columns=['longitude', 'latitude'])
print(y_predict)
