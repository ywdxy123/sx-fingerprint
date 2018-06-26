import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

p = pd.read_csv('D:\pycharm_project\\fingerprint\Road_test_data_lte\my_test\single_cell_test_data\p4.csv')
p.fillna(value=0, inplace=True)
pX = p[['servingrsrp', 'rsrp0', 'rsrp1', 'rsrp2', 'rsrp3', 'rsrp4', 'rsrp5','rsrp6','rsrp7','ta','aoa']]
py = p[['longitude', 'latitude']]
pX = StandardScaler().fit_transform(pX)
pX_train, pX_test, py_train, py_test = train_test_split(pX, py, test_size=0.1)

svr_lng = SVR(kernel='rbf', C=0.001, gamma=0.5, epsilon=0.000000001, max_iter=200000, tol=1e-12, shrinking=False)
# param_grid={'C':[0.1,0.001,1,10,100],'gamma':[2,0.5,10]}
# GS = GridSearchCV(svr_lng, param_grid=param_grid)
svr_lat = SVR(kernel='rbf', C=0.001, gamma=0.5, epsilon=0.000000001, max_iter=200000, tol=1e-12, shrinking=False)
# 经度
py_lng_train = py_train['longitude']
svr_lng.fit(pX_train, py_lng_train)
py_lng_predict = svr_lng.predict(pX_test)

# 纬度
py_lat_train = py_train['latitude']
svr_lat.fit(pX_train, py_lat_train)
py_lat_predict = svr_lat.predict(pX_test)
print(svr_lng.intercept_)

y_predict = pd.DataFrame({'latitude': py_lat_predict, 'longitude': py_lng_predict})
y_predict.to_csv('D:\pycharm_project\\fingerprint\Road_test_data_lte\my_test\single_cell_test_data\p4_predict.csv',
                 index=False)
py_test.to_csv('D:\pycharm_project\\fingerprint\Road_test_data_lte\my_test\single_cell_test_data\p4_test.csv',
               index=False)

