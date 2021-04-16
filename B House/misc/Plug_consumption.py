# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:14:07 2019

@author: mqureshi
"""

import os
import pandas as pd
from plug_load import load_file_plug
import matplotlib.pyplot as plt
import matplotlib.dates as matdates

os.system('cls')
os.chdir(r"C:\Patrice_Home_March_2019\data")

'''
*******************************************************************************
Plug information 
*******************************************************************************
'''
# PLUG # 01 
'''
file ="AU-01553184825-1-56-179010.mes.txt"
device_name =" Device Name : Autre (other)\n"
title = "March 2019 Consumption \n"+ device_name + "File Name :"+file
'''
# PLUG # 0

file ="AU-01553363835-1-56-179058.mes.txt"
device_name =" Device Name : Autre (Plug 2) \n"
title = "March 2019 Consumption \n"+ device_name + "File Name :"+file


'''
*******************************************************************************
Load data
*******************************************************************************
'''

df = load_file_plug(file)

df=df.astype(float)                                                            # This is required to convert timestamp to datetime 
df['Time stamp'] = pd.to_datetime(df['Time stamp'],unit='s')
df=df.set_index('Time stamp')                                                  # Converting dataframe to time-indexed dataframe


'''
*******************************************************************************
Plot
*******************************************************************************
'''
#######################  Complete plot - Hourly ##############################

fig, ax = plt.subplots()


#ax.plot(df.loc['2019-03-22 13':'2019-03-22 14','Power'], marker='o', linestyle='-')
ax=df.loc['2019-3-21',"Power"].plot()
ax=df.loc['2019-3-22',"Power"].plot()
ax=df.loc['2019-3-23',"Power"].plot(marker='')

ax.set_ylabel('Daily Consumption (W)', fontsize=15)
ax.set_title(title,fontsize='larger')
ax.set_xlabel('Time',fontsize=15)

# Set x-axis major ticks to weekly interval, on Mondays
ax.xaxis.set_major_locator(matdates.HourLocator())
ax.xaxis.set_minor_locator(matdates.MinuteLocator(byminute=range(10,60,10)))
# Format x-tick labels as 3-letter month name and day number
#ax.xaxis.set_major_formatter(matdates.DateFormatter('%Y-%m-%d, %H:%M:%S'));
ax.xaxis.set_major_formatter(matdates.DateFormatter('%m-%d,%H'));
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)


#######################  Resampled over 1 hour/30 min/15 min/10 min  ##############################

fig =plt.figure()

interval='H'   # sample over 1 hour
new_title = title + "\n Time Interval: " + interval
fig.suptitle(new_title)


plt.subplot(311)

df_daily = df.loc['2019-3-21',"Power"].resample(interval).mean()
df_daily.plot()


plt.subplot(312)
df_daily = df.loc['2019-3-22',"Power"].resample(interval).mean()
df_daily.plot()

plt.subplot(313)
df_daily = df.loc['2019-3-23',"Power"].resample(interval).mean()
df_daily.plot()


# sample over 30 Min

fig =plt.figure()
interval='30T'   # sample over 1 hour
new_title = title + "\n Time Interval: " + interval
fig.suptitle(new_title)


plt.subplot(311)

df_daily = df.loc['2019-3-21',"Power"].resample(interval).mean()
df_daily.plot()


plt.subplot(312)
df_daily = df.loc['2019-3-22',"Power"].resample(interval).mean()
df_daily.plot()

plt.subplot(313)
df_daily = df.loc['2019-3-23',"Power"].resample(interval).mean()
df_daily.plot()

# sample over 15 min 

fig =plt.figure()
interval='15T'   # sample over 1 hour
new_title = title + "\n Time Interval: " + interval
fig.suptitle(new_title)


plt.subplot(311)

df_daily = df.loc['2019-3-21',"Power"].resample(interval).mean()
df_daily.plot()


plt.subplot(312)
df_daily = df.loc['2019-3-22',"Power"].resample(interval).mean()
df_daily.plot()

plt.subplot(313)
df_daily = df.loc['2019-3-23',"Power"].resample(interval).mean()
df_daily.plot()


#sample over 10 

fig =plt.figure()
interval='10T'   # sample over 1 hour
new_title = title + "\n Time Interval: " + interval
fig.suptitle(new_title)


plt.subplot(311)

df_daily = df.loc['2019-3-21',"Power"].resample(interval).mean()
df_daily.plot()


plt.subplot(312)
df_daily = df.loc['2019-3-22',"Power"].resample(interval).mean()
df_daily.plot()

plt.subplot(313)
df_daily = df.loc['2019-3-23',"Power"].resample(interval).mean()
df_daily.plot()






