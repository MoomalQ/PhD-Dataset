# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 22:10:12 2019

@author: mqureshi
"""

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

#plug # 14

file = "PR-01553343884-1-56-168064.mes.txt"
device_name =" Device Name : Aggregate consumption Plug 14  \n"
title = "March 2019 Consumption \n"+ device_name + "File Name :"+file

#plug # 16

file = "TO-01553363835-1-56-179058.mes.txt"
device_name =" Device Name : Aggregate consumption Plug 16 Total  \n"
title = "March 2019 Consumption \n"+ device_name + "File Name :"+file


'''
*******************************************************************************
Load data
*******************************************************************************
'''

df = load_file_plug(file)
#df=df.drop(df.index[0])
df=df[df.Power!='-']
df=df.astype(float)                                                            # This is required to convert timestamp to datetime 
df['Time stamp'] = pd.to_datetime(df['Time stamp'],unit='s')
df=df.set_index('Time stamp')                                                  # Converting dataframe to time-indexed dataframe
df=df.drop(df.index[0])







''''
*******************************************************************************
Plot
*******************************************************************************
'''
#######################  Complete plot - Hourly ##############################

fig, ax = plt.subplots()


#ax.plot(df.loc['2019-03-22 13':'2019-03-22 14','Power'], marker='o', linestyle='-')
ax=df.loc['2019-3-23':'2019-3-25',"Power"].plot(label='Total consumption')
#ax=df.loc['2019-3-24',"Power"].plot()
#ax=df.loc['2019-3-25',"Power"].plot(marker='')

ax=df.loc['2019-3-23':'2019-3-25',"Power"].resample('H').mean().plot(marker='o',markersize=8,linestyle='-',label='Hourly Mean resampled')

#ax=df.loc['2019-3-23':'2019-3-25',"Power"].rolling(window=24,center=True, min_periods=24).mean().plot(marker='o',markersize=8,linestyle='-',label='24 Hour rolling mean')
#ax=df.loc['2019-3-23':'2019-3-25',"Power"].rolling(window=12,center=True, min_periods=12).mean().plot(marker='o',markersize=8,linestyle='-',label='12 Hour rolling mean')
ax=df.loc['2019-3-23':'2019-3-25',"Power"].rolling(window=3,center=True, min_periods=3).mean().plot(marker='o',markersize=8,linestyle='-',label='3 Hour rolling mean')




ax.set_ylabel('Daily Consumption (W)', fontsize=15)
ax.set_title(title,fontsize='larger')
ax.set_xlabel('Time',fontsize=15)

ax.xaxis.set_major_locator(matdates.HourLocator())
ax.legend()


'''
df_24h=df.loc['2019-3-23':'2019-3-25',"Power"].rolling(window=24,center=True, min_periods=24).mean()

df_12h=df.loc['2019-3-23':'2019-3-25',"Power"].rolling(window=12,center=True, min_periods=12).mean()


df_3h=df.loc['2019-3-23':'2019-3-25',"Power"].rolling(window=3,center=True, min_periods=3).mean()
'''



