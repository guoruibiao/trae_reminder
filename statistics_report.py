#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# Remove the code to set the Chinese font
# plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 定义统计目录
statistics_dir = 'statistics'

# 获取所有日期的日志文件
log_files = [f for f in os.listdir(statistics_dir) if f.endswith('.log')]

# 按日期排序
log_files.sort()

# 初始化一个空的DataFrame
all_data = pd.DataFrame(columns=['Time', 'Reminder Message'])

# 遍历每个日志文件
for log_file in log_files:
    # 解析日期
    date_str = log_file.split('.')[0]
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    # 读取日志文件
    with open(os.path.join(statistics_dir, log_file), 'r') as f:
        lines = f.readlines()
    # 解析每行数据
    for line in lines:
        parts = line.strip().split(': ', 1)
        if len(parts) == 2:
            time_str, message = parts
            time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            # 将数据添加到DataFrame中
            all_data = pd.concat([all_data, pd.DataFrame({'Time': [time], 'Reminder Message': [message]})], ignore_index=True)

# 按天统计提醒次数
daily_counts = all_data['Time'].dt.date.value_counts().sort_index()

# 绘制提醒次数的时间序列图
plt.figure(figsize=(3, 2))
plt.plot(daily_counts.index.astype(str), daily_counts.values)
# Change the title to English
plt.title('Daily Reminder Count')
# Change the x-axis label to English
plt.xlabel('Date')
plt.ylabel('Reminder Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Change the printed text to English
print('Daily reminder count statistics:')
print(daily_counts)