import pandas as pd
import numpy as np

data = {
    '工单编号': ['MO04', 'MO04', 'MO04', 'MO04', 'MO04', 'MO05', 'MO05', 'MO05', 'MO05', 'MO05', 'MO06', 'MO06', 'MO06', 'MO06', 'MO06'],
    '物料编码': ['FG04', 'FG04', 'FG04', 'FG04', 'FG05', 'FG05', 'FG05', 'FG05', 'FG06', 'FG06', 'FG06', 'FG06'],
    '计划开始日期': [20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412, 20230412],
    '计划完工日期': [20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423, 20230423],
    '工序': ['GY302', 'GY302', 'GY302', 'GY303', 'GY304', 'GY302', 'GY302', 'GY302', 'GY303', 'GY304', 'GY302', 'GY302', 'GY302', 'GY303', 'GY304'],
    '前置工序': ['/', '/', '/', 'GY302', 'GY303', '/', '/', '/', 'GY302', 'GY303', '/', '/', '/', 'GY302','GY303'],
    '资源名称': ['资源A', '资源B', '资源C', '/', '/', '资源A', '资源B', '资源C', '/', '/', '资源A', '资源B', '资源C', '/', '/'],
    '资源需求': [1.0, 1.0, 2.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0],
    '准备工时': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    '作业工时': [10.0, 10.0, 10.0, 10.0, 5.0, 15.0, 15.0, 15.0, 10.0, 5.0, 20.0, 20.0, 20.0, 10.0, 5.0],
    '后置工时': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
}

r = {'资源名称': ['资源A', '资源B', '资源C'],
     '资源总量': [10.0, 10.0, 20.0]}

f = [True] * len(data['工单编号'])
ff = [True]*len(data['工单编号'])
s = []
t = {'开始时间':[],
     '结束时间':[]}

def r_index(a):
    i = 0
    for i in range(len(r['资源名称'])):
        if r['资源名称'][i] == a:
            return i

def some_true(f):
    for item in f:
        if item:
            return True
    return False

def has_preceding_tasks(idx):
    for item in range(len(data['工序'])):
        if(data['工单编号'][item]==data['工单编号'][idx] and data['工序'][item]==data['前置工序'][idx]):
            if(f[item]==True):
                return False
    return True

def force(id):
    if data['前置工序'][id] == '/' or has_preceding_tasks(id):
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
        min_date = 30000000
        index = -1
        jj = 0
        for i in range(len(data['工单编号'])):
            if data['计划开始日期'][i] <= min_date and not_in_s(i) and f[i]==True:
                min_date = data['计划开始日期'][i]
                index = i
                if(data['资源名称'][index]!='/'):
                    j = r_index(data['资源名称'][index])
                    if r['资源总量'][j] >= data['资源需求'][index] and force(index):
                        r['资源总量'][j] -= data['资源需求'][index]
                        count+=1
                        s.append([])
                        s[count].append(index)
                        #ff = 1
                        t['开始时间'].append(nt) 
                        t['结束时间'].append(nt+data['准备工时'][index]+data['作业工时'][index]+data['后置工时'][index])
                        for k in range(len(data['工单编号'])):
                            if data['工序'][k]==data['工序'][index] and data['工单编号'][k]==data['工单编号'][index] and k != index:
                                jj = r_index(data['资源名称'][k])
                                if(r['资源总量'][jj]>=data['资源需求'][k]) and force(k):
                                    r['资源总量'][jj] -= data['资源需求'][k]
                                    s[count].append(k)
                else:
                    if force(index):
                        #st = 0
                        count+=1
                        s.append([])
                        s[count].append(index)
                        t['开始时间'].append(nt) 
                        t['结束时间'].append(nt+data['准备工时'][index]+data['作业工时'][index]+data['后置工时'][index])
        print(t)
        nt = count_nt(nt)
        for tt in range(len(t['结束时间'])):
            if(nt==t['结束时间'][tt]):
                for p in s[tt-fct]:
                    f[p] = False
                del(s[tt-fct])
                count-=1
                fct+=1
        for ai in range(len(data['资源需求'])):
            if(f[ai]==False and ff[ai]==True):
                if(data['资源名称'][ai]!='/'):
                    jj = r_index(data['资源名称'][ai])
                    r['资源总量'][jj] += data['资源需求'][ai]
                    ff[ai] = False

greedy_scheduling()