# sx-fingerprint
这是实习过程中的接手的指纹库项目，主要思路为，根据前期进行的路测数据信息采集，采集longitude,latitude,servingcellid,servingcellpci
,servingcellrsrp,frequency0~7,pci0~7,rsrp0~7等字段。

一：建立初始指纹库
（1）：
为了训练效果，对将要录入到指纹库的路测数据记录做如下预处理：
Step1删除邻区数据少于3个的记录
Step2删除servingcell，servingrsrp，longitude或latitude为空的记录。
（2）：
邻区之间的frequency和PCI通常是两两不同的，所以合并频点和PCI作为区别邻区的id
（3）：
根据经纬度生成栅格编号areaid和样本号sampleid
二：SVR训练
采用栅格下的样本数据对每个栅格的经(纬)度的支持向量机回归(SVR)模型进行训练，获取模型参数并建立参数表。
三：预测经纬度
采用逐步提高预测精度的方式。该部分首先根据MR记录的服务小区id获取可能的栅格id，再计算记录与候选栅格下所有样本的欧式距离，得到记录到每个候选栅格的距离，距离最小的即为匹配最佳的栅格，最后根据第二部分获得的参数表计算待测样本的经纬度。

