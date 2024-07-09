import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from deap import base, creator, tools, algorithms
import random
from datetime import datetime, timedelta

# 读取Excel文件
file_path = 'ByteMe/Resource/test/s_0.xlsx'
xls = pd.ExcelFile(file_path)

# 读取每个sheet的数据
work_orders = pd.read_excel(xls, sheet_name='工单')  # 根据实际情况修改sheet名称
routing = pd.read_excel(xls, sheet_name='工艺路线')
resource_calendar = pd.read_excel(xls, sheet_name='资源日历')
lock_schedule = pd.read_excel(xls, sheet_name='锁排程')
changeover = pd.read_excel(xls, sheet_name='设备换型')

# 转换日期格式
work_orders['计划开始日期'] = pd.to_datetime(work_orders['计划开始日期'], format='%Y/%m/%d')
work_orders['计划完工日期'] = pd.to_datetime(work_orders['计划完工日期'], format='%Y/%m/%d')
resource_calendar['开始日期'] = pd.to_datetime(resource_calendar['开始日期'], format='%Y/%m/%d')
resource_calendar['结束日期'] = pd.to_datetime(resource_calendar['结束日期'], format='%Y/%m/%d')

print(work_orders)
