import pandas as pd
import time
from sqlalchemy import create_engine
from Fingerprint.Mymodel.endow_neigh_ci import Preprocessing
from Fingerprint.Mymodel.forecast import Forecast

if __name__ == '__main__':
    # 对MR数据进行预测
    # 输入指纹库
    time_start = time.time()
    xdrfingerprint = pd.read_csv(
        'E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\\train3.csv')

    # 输入参数表
    parameter = pd.read_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\train_test_data\parameter4.csv')

    # 连接数据库，输入mr数据
    conn = create_engine('mysql+pymysql://root:hantele@192.168.6.10:5029/weizhi?charset=utf8')
    cmd = "select CELLID as servingcell,NEIGHBOR1PCI as pci0, " \
          "NEIGHBOR2PCI as pci1,NEIGHBOR3PCI as pci2, NEIGHBOR4PCI as pci3," \
          "NEIGHBOR5PCI as pci4,NEIGHBOR6PCI as pci5,NEIGHBOR7PCI as pci6," \
          "NEIGHBOR8PCI as pci7,NEIGHBOR1FREQ as frequency0,  NEIGHBOR2FREQ as frequency1," \
          "NEIGHBOR3FREQ as frequency2,NEIGHBOR4FREQ as frequency3," \
          "NEIGHBOR5FREQ as frequency4,NEIGHBOR6FREQ as frequency5," \
          "NEIGHBOR7FREQ as frequency6,NEIGHBOR8FREQ as frequency7," \
          "SERVINGRSRP as servingrsrp, NEIGHBOR1RSRP as rsrp0," \
          "NEIGHBOR2RSRP as rsrp1, NEIGHBOR3RSRP as rsrp2,NEIGHBOR4RSRP as rsrp3," \
          "NEIGHBOR5RSRP as rsrp4, NEIGHBOR6RSRP as rsrp5, NEIGHBOR7RSRP as rsrp6," \
          "NEIGHBOR8RSRP as rsrp7 from UE_MR limit 100000"
    cmd1="select * from UE_MR_zhujiang_ava limit 1000"
    file = pd.read_sql(cmd1, conn)

    file.to_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\UE_MR_test\mr_data3.csv')

    # 预处理，合并频点以及pci
    pre = Preprocessing(file)
    data = pre.clean()
    data.shape
    # 预测经纬度
    predictions = Forecast(xdrfingerprint, parameter, data)
    predictions.multi_predict()
    res = predictions.userdata[['lng_pre', 'lat_pre']]
    # 输出结果
    res.to_csv('E:\Position_project\Fingerprint\Fingerprint_zhujiang\\UE_MR_test\mr_prediction4.csv',index=False)
    time_end = time.time()
    print('totally cost', time_end - time_start)