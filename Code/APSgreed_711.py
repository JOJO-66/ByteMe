from openpyxl.drawing.image import Image
from openpyxl import Workbook
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import time
from datetime import datetime,timedelta

starttime = time.time()

file_path = 's/s_2.xlsx'
xls = pd.ExcelFile(file_path)

def auto_resize_column(excel_path):
    """自适应列宽度"""
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
                # Necessary to avoid error on empty cells
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column].width = adjusted_width
    workbook.save(excel_path)

def transpose(arr):
    list1 = list()
    arr_len = len(arr)
    for i in range(len(arr[0])):
        list1.append(list())
        for j in range(arr_len):
            list1[-1].append(arr[j][i])
    return list1


def fill(arr, column):
    for i in range(len(data[column])):
        if (pd.isna(data[column][i])):
            data[column][i] = data[column][i-1]


work_orders = pd.read_excel(xls, sheet_name='工单')  # 根据实际情况修改sheet名称
work_order = work_orders.values.tolist()
sum = len(work_order)
order = work_order[0][7]
c = []
d = []
for i in range(sum):
    c.append(i+1)
    d.append(work_order[i][0])
routing = pd.read_excel(xls, sheet_name='工艺路线')
data = routing.values.tolist()
del (data[0])
data = transpose(data)
del (data[1])
fill(data, 0)
fill(data, 1)
fill(data, 2)
for i in range(len(data[0])):
    if (pd.isna(data[3][i])):
        data[3][i] = '/'
for i in range(len(data[0])):
    if (pd.isna(data[4][i])):
        data[4][i] = 0
    else:
        data[4][i] = int(data[4][i])
fill(data, 5)
fill(data, 6)
fill(data, 7)
for i in range(5, 8):
    for j in range(len(data[i])):
        data[i][j] = int(data[i][j])
del (data[8])
data.append([])
for i in range(len(data[0])):
    for j in range(len(work_order)):
        if (data[0][i] == work_order[j][0]):
            data[8].append(work_order[j][3])
data.append([])
for i in range(len(data[0])):
    for j in range(len(work_order)):
        if (data[0][i] == work_order[j][0]):
            data[9].append(work_order[j][4])
data.append([])
for i in range(len(data[0])):
    for j in range(len(work_order)):
        if (data[0][i] == work_order[j][0]):
            data[10].append(work_order[j][6])
fill(data,10)
data.append([])
for i in range(len(data[0])):
    for j in range(len(work_order)):
        if (data[0][i] == work_order[j][0]):
            data[11].append(work_order[j][5])
for i in range(len(data[0])):
    if (pd.isna(data[11][i])):
        data[11][i] = '/'
# print(data)

name = []

resource_calendar = pd.read_excel(xls, sheet_name='资源日历')
rc = resource_calendar.values.tolist()
r = [[], []]
for i in range(len(rc)):
    if (pd.isna(rc[i][0])):
        break
    else:
        r[0].append(rc[i][2])
        r[1].append(int(rc[i][4]))

f = [True] * len(data[0])
ff = [True]*len(data[0])
fff = False
s = []
t = {'开始时间': [],
     '结束时间': []}
nt = 0
gx = []
resou = []
bm = []

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


def has_preceding_task(idx):
    for item in range(len(data[1])):
        if (data[0][item] == data[11][idx]):
            if (f[item] == True):
                return False
    return True

def has_preceding_tasks(idx):
    for item in range(len(data[1])):
        if (data[0][item] == data[0][idx] and data[1][item] == data[2][idx]):
            if (f[item] == True):
                return False
    return True


def force(id):
    if data[2][id] == '/' or has_preceding_tasks(id):
        return True
    return False

def force2(id):
    if data[11][i]=='/' or has_preceding_task(id):
        return True
    return False

def not_in_s(ii):
    for iii in range(len(s)):
        for jjj in range(len(s[iii])):
            if ii == s[iii][jjj]:
                return False
    return True


def count_nt(nt):
    min_t = max(t['结束时间'])
    for et in t['结束时间']:
        if (et > nt and et <= min_t):
            min_t = et
    return min_t


def rec(index):
    for i in range(len(d)):
        if (data[0][index] == d[i]):
            return c[i]

# 贪心完成正排


def greedy_scheduling():
    nt = 0
    j = -1
    count = -1
    fct = 0
    dts = []
    # 正排
    if order == '正排':
        while some_true(f):
            min_date = '3000/00/00'
            min_yxj = len(c)
            index = -1
            jj = 0
            i = 0
            while (i < len(data[0])):
                # for i in range(len(data[0])):
                step = 0
                if data[8][i] <= min_date and not_in_s(i) and f[i] == True and data[10][i]<=min_yxj and force2(i):
                    min_date = data[8][i]
                    min_yxj = data[10][i]
                    index = i
                    if (data[3][index] != '/'):
                        j = r_index(data[3][index])
                        if r[1][j] >= data[4][index] and force(index):
                            flag = True
                            rec_r = []
                            rec_r.append([j, data[4][index], index])
                            for k in range(len(data[0])):
                                if data[1][k] == data[1][index] and data[0][k] == data[0][index] and k != index:
                                    jj = r_index(data[3][k])
                                    if (r[1][jj] >= data[4][k]) and force(k):
                                        # r[1][jj] -= data[4][k]
                                        # s[count].append(k)
                                        rec_r.append([jj, data[4][k], k])
                                        step += 1
                                    else:
                                        flag = False
                                        break
                                # else:
                                #    break
                            # r[1][j] -= data[4][index]
                            if flag == True:
                                for y in range(len(rec_r)):
                                    s.append([])
                                    for z in range(len(rec_r)):
                                        s[len(s)-1].append(rec_r[z][2])
                                    if (nt-data[5][index] > 0):
                                        t['开始时间'].append(nt-data[5][index])
                                    else:
                                        t['开始时间'].append(nt)
                                    name.append(rec(rec_r[0][2]))
                                    gx.append(data[1][rec_r[0][2]])
                                    # +data[7][index])
                                    t['结束时间'].append(nt+data[5][index]+data[6][index])
                                    dts.append(count)
                                for z in range(len(rec_r)):
                                    r[1][rec_r[z][0]] -= rec_r[z][1]
                                    resou.append(data[3][rec_r[z][2]])
                                    bm.append(rec_r[z][2])
                                fct = 0
                                fff = True
                    else:
                        if force(index):
                            count += 1
                            s.append([])
                            fct = 0
                            fff = True
                            s[len(s)-1].append(index)
                            name.append(rec(index))
                            gx.append(data[1][index])
                            resou.append("虚拟资源")
                            bm.append(index)
                            t['开始时间'].append(nt+data[7][index])
                            t['结束时间'].append(nt+data[5][index]+data[6][index]+data[7][index])
                            dts.append(count)
                            # greed(index)
                            # print(t)
                i += 1+step
                step = 0

            nt = count_nt(nt)
            tt = 0
            while tt <len(t['结束时间']):
                if (nt == t['结束时间'][tt]):
                    l = 0
                    for p in s[tt]:
                        f[p] = False
                        l+=1
                    tt += l
                    #fct+=l
                else:
                    tt+=1
            fff = False

            '''for aa in range(len(dts)):
                if t['结束时间'][aa]>nt:
                    dts[aa] = dts[aa] - fct'''

            for ai in range(len(data[5])):
                if (f[ai] == False and ff[ai] == True):
                    if (data[3][ai] != '/'):
                        jj = r_index(data[3][ai])
                        r[1][jj] += data[4][ai]
                        ff[ai] = False
    # 倒排
    elif order == '倒排':
        while some_true(f):
            min_date = '3000/00/00'
            min_yxj = len(c)
            index = -1
            jj = 0
            i = 0
            while (i < len(data[0])):
                # for i in range(len(data[0])):
                step = 0
                if data[9][i] <= min_date and not_in_s(i) and f[i] == True and data[10][i]<=min_yxj and force2(i):
                    min_date = data[8][i]
                    min_yxj = data[10][i]
                    index = i
                    if (data[3][index] != '/'):
                        j = r_index(data[3][index])
                        if r[1][j] >= data[4][index] and force(index):
                            flag = True
                            rec_r = []
                            rec_r.append([j, data[4][index], index])
                            for k in range(len(data[0])):
                                if data[1][k] == data[1][index] and data[0][k] == data[0][index] and k != index:
                                    jj = r_index(data[3][k])
                                    if (r[1][jj] >= data[4][k]) and force(k):
                                        # r[1][jj] -= data[4][k]
                                        # s[count].append(k)
                                        rec_r.append([jj, data[4][k], k])
                                        step += 1
                                    else:
                                        flag = False
                                        break
                                # else:
                                #    break
                            # r[1][j] -= data[4][index]
                            if flag == True:
                                for y in range(len(rec_r)):
                                    s.append([])
                                    for z in range(len(rec_r)):
                                        s[len(s)-1].append(rec_r[z][2])
                                    if (nt-data[5][index] > 0):
                                        t['开始时间'].append(nt-data[5][index])
                                    else:
                                        t['开始时间'].append(nt)
                                    name.append(rec(rec_r[0][2]))
                                    gx.append(data[1][rec_r[0][2]])
                                    # +data[7][index])
                                    t['结束时间'].append(nt+data[5][index]+data[6][index])
                                    dts.append(count)
                                for z in range(len(rec_r)):
                                    r[1][rec_r[z][0]] -= rec_r[z][1]
                                    resou.append(data[3][rec_r[z][2]])
                                    bm.append(rec_r[z][2])
                                fct = 0
                                fff = True
                    else:
                        if force(index):
                            count += 1
                            s.append([])
                            fct = 0
                            fff = True
                            s[len(s)-1].append(index)
                            name.append(rec(index))
                            gx.append(data[1][index])
                            resou.append("虚拟资源")
                            bm.append(index)
                            t['开始时间'].append(nt+data[7][index])
                            t['结束时间'].append(nt+data[5][index]+data[6][index]+data[7][index])
                            dts.append(count)
                            # greed(index)
                            # print(t)
                i += 1+step
                step = 0

greedy_scheduling()
endtime = time.time()
print(endtime-starttime)

gdbh = []
for i in name:
    gdbh.append(d[i-1])

start_time = data[8][0]

new_pst_str = []
for i in range(len(t['开始时间'])):
    pst = datetime.strptime(start_time,'%Y/%m/%d')
    new_pst = pst + timedelta(minutes=t['开始时间'][i])
    new_pst_str.append(new_pst.strftime('%Y-%m-%d %H:%M'))

new_pet_str = []
for i in range(len(t['结束时间'])):
    pet = datetime.strptime(start_time,'%Y/%m/%d')
    new_pet = pet + timedelta(minutes=t['结束时间'][i])
    new_pet_str.append(new_pet.strftime('%Y-%m-%d %H:%M'))

#res = [
#    gdbh,gx,new_pst_str,new_pet_str
#]

pdata = []

for i in range(len(name)):
    pdata.append({"Task":d[name[i]-1]+" "+gx[i]+" "+resou[i],"Start":new_pst_str[i],"Finish":new_pet_str[i]})
    pdata.append({"Task":d[name[i]-1]+" "+gx[i]+" "+resou[i],"Start":new_pst_str[i],"Finish":new_pet_str[i]})

df = pd.DataFrame(pdata)
df['Start'] = pd.to_datetime(df['Start'])
df['Finish'] = pd.to_datetime(df['Finish'])

# 创建图表
fig, ax = plt.subplots(figsize=(15, 8))

# 设置颜色
colors = {'资源A': 'tab:green', '资源B': 'tab:blue', '资源C': 'tab:gray', '虚拟资源': 'tab:red'}

# 绘制任务条
for i, row in df.iterrows():
    resource = row['Task'].split()[-1]
    ax.barh(row['Task'], row['Finish'] - row['Start'], left=row['Start'], color=colors[resource])

# 设置格式
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False 
plt.xticks(rotation=45)
plt.xlabel('Time')
plt.ylabel('Tasks')
plt.title('Gantt Chart')
plt.grid(True)
plt.tight_layout()

# 保存图表
plt.savefig('gantt_chart.png')
#plt.show()

workbook = Workbook()

# 默认sheet
sheet = workbook.active
sheet.title = "openpyxl"
sheet.append(["工单编号","工序" ,"资源","计划开始时间", "计划结束时间"])  # 插入标题

res = [
    gdbh,gx,resou,new_pst_str,new_pet_str
]
res = transpose(res)
for dd in res:
    sheet.append(list(dd))  # 这里要接受的也是list把值取出来在转化一下

auto_resize_column('openpyxl.xlsx')

img = Image('gantt_chart.png')
img.anchor = "f1"
img.width = img.width*0.75
img.height = img.height*0.75
sheet.add_image(img)
workbook.save('openpyxl.xlsx')
