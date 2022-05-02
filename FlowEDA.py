# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:01:07 2022

@author: allen
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('flow_expert.csv')
df = df[df['Time'] >= 0]
good_flow = df[df['Flow'] == True]
bad_flow = df[df['Flow'] == False]

print(df.columns)

for column in df.columns:
    if 'Flow' not in column:
        fig, ax = plt.subplots(1, 1)
        ax.set_title(column)
        data = [good_flow[column], bad_flow[column]]
        ax.set_xticklabels(['Good', 'Bad'])
        ax.boxplot(data)
        
fig, ax = plt.subplots(1,1)
ax.set_title('Start Direction in Relation to End Direction')
ax.scatter(bad_flow['Start Direction'], bad_flow['End Direction'], alpha=.25, label='Bad Flow')
ax.scatter(good_flow['Start Direction'], good_flow['End Direction'], alpha=.25, label='Good Flow')
ax.set_xlabel('Start Direction')
ax.set_ylabel('End Direction')
ax.legend()

fig, ax = plt.subplots(1,1)
ax.set_title('Magnitude in Relation to Time')
ax.scatter(bad_flow['Magnitude'], bad_flow['Time'], alpha=.25, label='Bad Flow')
ax.scatter(good_flow['Magnitude'], good_flow['Time'], alpha=.25, label='Good Flow')
ax.set_xlabel('Magnitude')
ax.set_ylabel('Time (seconds)')
ax.legend()
