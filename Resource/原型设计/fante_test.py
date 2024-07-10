import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 读取数据
data = [
    {"Task": "MO04 GY302 资源C", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:20"},
    {"Task": "MO06 GY302 资源C", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:30"},
    {"Task": "MO05 GY302 资源C", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:25"},
    {"Task": "MO04 GY302 资源B", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:20"},
    {"Task": "MO06 GY302 资源B", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:30"},
    {"Task": "MO05 GY302 资源B", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:25"},
    {"Task": "MO04 GY302 资源A", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:20"},
    {"Task": "MO06 GY302 资源A", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:30"},
    {"Task": "MO05 GY302 资源A", "Start": "2023-04-12 00:00", "Finish": "2023-04-12 00:25"},
    {"Task": "MO05 GY304 虚拟资源", "Start": "2023-04-12 00:45", "Finish": "2023-04-12 01:00"},
    {"Task": "MO06 GY304 虚拟资源", "Start": "2023-04-12 01:30", "Finish": "2023-04-12 01:45"},
    {"Task": "MO04 GY304 虚拟资源", "Start": "2023-04-12 01:20", "Finish": "2023-04-12 01:35"},
    {"Task": "MO04 GY303 虚拟资源", "Start": "2023-04-12 00:40", "Finish": "2023-04-12 01:00"},
    {"Task": "MO05 GY303 虚拟资源", "Start": "2023-04-12 00:45", "Finish": "2023-04-12 01:05"},
    {"Task": "MO06 GY303 虚拟资源", "Start": "2023-04-12 00:50", "Finish": "2023-04-12 01:10"},
]

df = pd.DataFrame(data)
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
plt.xticks(rotation=45)
plt.xlabel('Time')
plt.ylabel('Tasks')
plt.title('Gantt Chart')
plt.grid(True)
plt.tight_layout()

# 保存图表
plt.savefig('D:/ByteMe/ByteMe/Resource/原型设计/gantt_chart.png')
plt.show()
