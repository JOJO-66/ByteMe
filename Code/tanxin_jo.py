import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from deap import base, creator, tools, algorithms
import random
from datetime import datetime, timedelta

# 读取Excel文件
file_path = 's/s_0.xlsx'
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

# 贪心算法排程
schedule_result = []

# 按优先级排序工单
work_orders = work_orders.sort_values(by=['优先级', '计划开始日期'])

for _, work_order in work_orders.iterrows():
    wo_id = work_order['工单编号']
    material_id = work_order['物料编号']
    
    # 获取该工单的工艺路线
    operations = routing[routing['物料编码'] == material_id]
    
    for _, operation in operations.iterrows():
        op_id = operation['工序']
        required_resources = operation['资源名称'].split(',')
        start_time = work_order['计划开始日期']
        
        # 为每个工序分配资源
        for resource in required_resources:
            resource_info = resource_calendar[resource_calendar['资源名称'] == resource]
            resource_info = resource_info[resource_info['开始日期'] <= start_time]
            resource_info = resource_info[resource_info['结束日期'] >= start_time]
            
            if not resource_info.empty:
                # 选择第一个可用资源
                res_id = resource_info.iloc[0]['资源编号']
                schedule_result.append({
                    '工单编号': wo_id,
                    '物料编号': material_id,
                    '工序': op_id,
                    '资源组': resource,
                    '资源组ID': res_id,
                    '资源数量': operation['资源需求'],
                    '计划开始时间': start_time,
                    '计划结束时间': start_time + timedelta(minutes=operation['准备工时'] + operation['作业工时'])
                })
                # 更新资源的可用时间
                start_time += timedelta(minutes=operation['准备工时'] + operation['作业工时'] + operation['后置工时'])
                resource_calendar.loc[resource_calendar['资源编号'] == res_id, '开始日期'] = start_time

# 输出排程结果
schedule_df = pd.DataFrame(schedule_result)
print(schedule_df)

# 保存到Excel
schedule_df.to_excel('/mnt/data/schedule_result.xlsx', index=False)
