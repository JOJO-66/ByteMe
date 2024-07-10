import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path = 's/s_1.xlsx'
xls = pd.ExcelFile(file_path)

def transpose(arr):
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

work_orders = pd.read_excel(xls, sheet_name='工单') #根据实际情况修改sheet名称 
work_order = work_orders.values.tolist()
sum = len(work_order)
c = []
d = []
for i in range(sum):
    c.append(i+1)
    d.append(work_order[i][0])
routing = pd.read_excel(xls, sheet_name='工艺路线')
data = routing.values.tolist()
del(data[0])
data = transpose(data)
del(data[1])
fill(data,0)
fill(data,1)
fill(data,2)
for i in range(len(data[0])):
    if(pd.isna(data[3][i])):
        data[3][i] = '/'
for i in range(len(data[0])):
    if(pd.isna(data[4][i])):
        data[4][i] = 0
    else:
        data[4][i] = int(data[4][i])
fill(data,5)
fill(data,6)
fill(data,7)
for i in range(5,8):
    for j in range(len(data[i])):
        data[i][j] = int(data[i][j])
del(data[8])
data.append([])
for i in range(len(data[0])):
    for j in range(len(work_order)):
        if(data[0][i]==work_order[j][0]):
            data[8].append(work_order[j][3])

#print(data)

name = []

resource_calendar = pd.read_excel(xls, sheet_name='资源日历')
rc = resource_calendar.values.tolist()
r = [[],[]]
for i in range(len(rc)):
    if(pd.isna(rc[i][0])):
        break
    else:
        r[0].append(rc[i][2])
        r[1].append(int(rc[i][4]))

f = [True] * len(data[0])
ff = [True]*len(data[0])
s = []
t = {'开始时间':[],
     '结束时间':[]}

def r_index(a):
    i = 0
    for i in range(len(r[0])):
        if r[0][i] == a:
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

def rec(index):
    for i in range(len(d)):
        if(data[0][index]==d[i]):
            return c[i] 

def greedy_scheduling():
    nt = 0
    j = -1
    count = -1
    fct = 0
    while some_true(f):
        min_date = '3000/00/00'
        index = -1
        jj = 0
        i = 0
        while(i<len(data[0])):
        #for i in range(len(data[0])):
            if data[8][i] <= min_date and not_in_s(i) and f[i]==True:
                min_date = data[8][i]
                index = i
                if(data[3][index]!='/'):
                    j = r_index(data[3][index])
                    if r[1][j] >= data[4][index] and force(index):
                        flag = True
                        rec_r = []
                        rec_r.append([j,data[4][index],index])
                        step = 0
                        for k in range(len(data[0])):
                            if data[1][k]==data[1][index] and data[0][k]==data[0][index] and k != index:
                                jj = r_index(data[3][k])
                                if(r[1][jj]>=data[4][k]) and force(k):
                                    #r[1][jj] -= data[4][k]
                                    #s[count].append(k)
                                    rec_r.append([jj,data[4][k],k])
                                    step+=1
                                else:
                                    flag = False
                                    break
                            #else:
                            #    break
                        #r[1][j] -= data[4][index]
                        if flag==True:
                            count+=1
                            s.append([])
                            for z in range(len(rec_r)):
                                s[count].append(rec_r[z][2])
                                r[1][rec_r[z][0]] -= rec_r[z][1]
                            name.append(rec(rec_r[0][2]))
                            t['开始时间'].append(nt) 
                            t['结束时间'].append(nt+data[5][index]+data[6][index]+data[7][index])     
                else:
                    if force(index):
                        count+=1
                        s.append([])
                        s[count].append(index)
                        name.append(rec(index))
                        t['开始时间'].append(nt) 
                        t['结束时间'].append(nt+data[5][index]+data[6][index]+data[7][index])
        #print(t)
            i += 1+step
            step = 0
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
                    r[1][jj] += data[4][ai]
                    ff[ai] = False
    print(t)

def plot_gantt():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 替换sans-serif字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决坐标轴负数的负号显示问题
    
    colorr = ['#8CD77F','#B1DFE7','#B9E9C8','#AEC4E5','#D28670']

    for i in range(len(name)):
        plt.barh(y=name[i],width=(t['结束时间'][i]-t['开始时间'][i]-data[5][name[i]])/20,left = t['开始时间'][i]/20,edgecolor='white',color=colorr[name[i]])
 
    # plt.text(1, 2, "AS00", verticalalignment="center", horizontalalignment="center")
 
    plt.title("甘特图")  # 图形标题
    # plt.xlabel("当前时间")  # x轴标签
    # plt.ylabel("人员")  # y轴标签
 
    # y轴坐标显示

    plt.yticks(c,d)
    # x轴坐标显示
    ct = int (max(t['结束时间'])/20)+1
    xx = []
    x_name = []
    for i in range(ct):
        xx.append(i)
        x_name.append((i)*20)

    plt.xticks(xx, x_name)
 
    plt.show()

greedy_scheduling()
plot_gantt()