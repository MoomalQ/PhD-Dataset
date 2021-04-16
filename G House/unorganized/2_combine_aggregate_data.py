# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:08:15 2019

@author: mqureshi
"""

import os
import pandas as pd

os.chdir(r"C:\Users\mqureshi\Desktop\online_disaggregation_with_toy_data\1_Data preparation_toy_dataset\data\power")
#Path=r"C:\Users\mqureshi\Desktop\online_disaggregation_with_toy_data\1_Data preparation_toy_dataset\data\power"



n_loaded=0
List_of_files=os.listdir()
len_file=len(List_of_files)

data=pd.DataFrame()

for file in os.listdir():
    n_loaded+=1
    print( "loaded ......",n_loaded,"out of ",len_file)
    df=pd.read_csv(file, )
    data=data.append(df,ignore_index=True)
    
 

os.chdir(r"C:\Users\mqureshi\Desktop\online_disaggregation_with_toy_data\1_Data preparation_toy_dataset\data\combined")
data.to_csv("combined_consumption_aggregate_iron_heater_hairdryer_power_consumption_200508.csv", index = False)
