import pandas as pd
import numpy as np

'''data = {
    0: ['MO04', 'MO04', 'MO04', 'MO04', 'MO04', 'MO05', 'MO05', 'MO05', 'MO05', 'MO05', 'MO06', 'MO06', 'MO06', 'MO06', 'MO06'],
    #'物料编码': ['FG04', 'FG04', 'FG04', 'FG04', 'FG05', 'FG05', 'FG05', 'FG05', 'FG06', 'FG06', 'FG06', 'FG06'],
    8: [20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412],
    '计划完工日期': [20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423],
    1: ['GY302', 'GY302', 'GY302', 'GY303', 'GY304', 'GY302', 'GY302', 'GY302', 'GY303', 'GY304', 'GY302', 'GY302', 'GY302', 'GY303', 'GY304'],
    2: ['/', '/', '/', 'GY302', 'GY303', '/', '/', '/', 'GY302', 'GY303', '/', '/', '/', 'GY302','GY303'],
    3: ['资源A', '资源B', '资源C', '/', '/', '资源A', '资源B', '资源C', '/', '/', '资源A', '资源B', '资源C', '/', '/'],
    4: [1.0, 1.0, 2.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0],
    5: [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    6: [10.0, 10.0, 10.0, 10.0, 5.0, 15.0, 15.0, 15.0, 10.0, 5.0, 20.0, 20.0, 20.0, 10.0, 5.0],
    7: [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
}'''

file_path = 's/s_0.xlsx'
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
#print(data)

r = {3: ['资源A', '资源B', '资源C'],
     '资源总量': [10.0, 10.0, 20.0]}

f = [True] * len(data[0])
ff = [True]*len(data[0])
s = []
t = {'开始时间':[],
     '结束时间':[]}

def r_index(a):
    i = 0
    for i in range(len(r[3])):
        if r[3][i] == a:
            return i

def some_true(f):
    for item in f:
        if item:
            return True
    return False

def has_preceding_tasks(idx):
    for item in range(len(data[1])):
        if(data[0][item]==data[0][idx] and data[1][item]==data[2][idx]):
            if(f[item]==True):
                return False
    return True

def force(id):
    if data[2][id] == '/' or has_preceding_tasks(id):
        return True
    return False

def not_in_s(ii):
    for iii in range(len(s)):
        for jjj in range(len(s[iii])):
            if ii==s[iii][jjj]:
                return False
    return True 

def count_nt(nt):
    min_t = max(t['结束时间'])
    for et in t['结束时间']:
        if(et>nt and et<=min_t):
            min_t = et
    return min_t


def greedy_scheduling():
    nt = 0
    j = -1
    count = -1
    fct = 0
    while some_true(f):
        min_date = '3000/00/00'
        index = -1
        jj = 0
        for i in range(len(data[0])):
            if data[8][i] <= min_date and not_in_s(i) and f[i]==True:
                min_date = data[8][i]
                index = i
                if(data[3][index]!='/'):
                    j = r_index(data[3][index])
                    if r['资源总量'][j] >= data[4][index] and force(index):
                        r['资源总量'][j] -= data[4][index]
                        count+=1
                        s.append([])
                        s[count].append(index)
                        #ff = 1
                        t['开始时间'].append(nt) 
                        t['结束时间'].append(nt+data[5][index]+data[6][index]+data[7][index])
                        for k in range(len(data[0])):
                            if data[1][k]==data[1][index] and data[0][k]==data[0][index] and k != index:
                                jj = r_index(data[3][k])
                                if(r['资源总量'][jj]>=data[4][k]) and force(k):
                                    r['资源总量'][jj] -= data[4][k]
                                    s[count].append(k)
                else:
                    if force(index):
                        #st = 0
                        count+=1
                        s.append([])
                        s[count].append(index)
                        t['开始时间'].append(nt) 
                        t['结束时间'].append(nt+data[5][index]+data[6][index]+data[7][index])
        print(t)
        nt = count_nt(nt)
        for tt in range(len(t['结束时间'])):
            if(nt==t['结束时间'][tt]):
                for p in s[tt-fct]:
                    f[p] = False
                del(s[tt-fct])
                count-=1
                fct+=1
        for ai in range(len(data[5])):
            if(f[ai]==False and ff[ai]==True):
                if(data[3][ai]!='/'):
                    jj = r_index(data[3][ai])
                    r['资源总量'][jj] += data[4][ai]
                    ff[ai] = False

greedy_scheduling()