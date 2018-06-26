#2
import pandas as pd

def modify(df, unique_cell):
    # 根据原始数据修正, 包括去除多余字段，更改列名，去除邻区小于3个的样本。可根据实际路测数据的情况做调整
    df.drop(['ComputerTime', 'HandsetTime', 'LTE Frequency UL', 'LTE EARFCN UL', 'LTE TimingAdvance', ], inplace=True,
            axis=1)
    df.columns = ['longitude', 'latitude', 'servingcell', 'servingpci',
                  'servingrsrp', 'frequency0', 'frequency1', 'frequency2', 'frequency3', 'frequency4',
                  'frequency5', 'pci0', 'pci1', 'pci2', 'pci3', 'pci4', 'pci5', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3',
                  'rsrp4', 'rsrp5']
    df.servingcell.fillna(method='ffill', inplace=True)
    df.drop(df[df['servingpci'].isnull() == True].index, inplace=True)
    df.drop(df[df['servingrsrp'].isnull() == True].index, inplace=True)
    df.drop(df[(df['servingcell'].isnull() == True) | (df['longitude'].isnull() == True) | (
            df['latitude'].isnull() == True)].index, inplace=True)

    dropind1 = []
    test = df[['servingcell', 'servingpci']]
    for index, item in test.iterrows():
        if unique_cell.loc[int(item.loc['servingcell'])].values != item.loc['servingpci']:
            dropind1.append(index)
    df.drop(dropind1, inplace=True)
    mergecut = df[['rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5']]
    temp = mergecut.count(axis=1)
    dropind2 = temp.loc[temp < 3].index
    df.drop(dropind2, inplace=True)
    return df

if __name__ == '__main__':
    
    df = pd.read_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile1.csv')
    unique_cell = pd.read_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\\unique_cell1.csv',
                              index_col=0)
    res = modify(df, unique_cell)
    res.to_csv('D:\pycharm_project\Fingerprint\Fingerprint_zhujiang\data_cleaned\mergefile_m1.csv',index=False)
    
