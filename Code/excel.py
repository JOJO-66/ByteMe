import pandas as pd
import numpy as np
#该代码用于把Excel文件读出

file_path = 'ByteMe/Resource/test/ss_0.xlsx'
xls = pd.ExcelFile(file_path)

def transpose_1(arr):
    list1 = list()
    arr_len = len(arr)
    for i in range(len(arr[0])):
        list1.append(list())
        for j in range(arr_len):
            list1[-1].append(arr[j][i])
    return list1

def fill(arr,column):
    for i in range(len(data[column])):
        if(pd.isna(data[column][i])):
            data[column][i] = data[column][i-1]

work_orders = pd.read_excel(xls, sheet_name='工单') # 根据实际情况修改sheet名称 
work_order = work_orders.values.tolist()
routing = pd.read_excel(xls, sheet_name='工艺路线')
data = routing.values.tolist()
data = transpose_1(data)
del(data[1])
fill(data,0)
fill(data,1)
fill(data,2)
for i in range(len(data[0])):
    if(pd.isna(data[3][i])):
        data[3][i] = '/'
for i in range(len(data[0])):
    if(pd.isna(data[4][i])):
        data[4][i] = 0.0
fill(data,5)
fill(data,6)
fill(data,7)
del(data[8])
data.append([])
for i in range(len(data[0])):
    for j in range(len(work_order)):
        if(data[0][i]==work_order[j][0]):
            data[8].append(work_order[j][3])
print(data)
resource_calendar = pd.read_excel(xls, sheet_name='资源日历')
lock_schedule = pd.read_excel(xls, sheet_name='锁排程')
changeover = pd.read_excel(xls, sheet_name='设备换型')