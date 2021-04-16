# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 14:42:29 2021

@author: Moomal Qureshi 

@Moomal: code for extending the csv file as used in Blind disaggregation paper
 (Qureshi,2021) for toy datset
 
 1. create 2 copies csv file in G House \ csv
 2. Run the script 
 3. output will be the dataset refered to as toydata consisting of few minutes of power consumption

"""


import os
import pandas as pd

os.chdir(r"C:\OGGA dataset\G House\csv")

n_loaded=0
List_of_files=os.listdir()
len_file=len(List_of_files)

data=pd.DataFrame()

for file in os.listdir():
    n_loaded+=1
    print( "loaded ......",n_loaded,"out of ",len_file)
    df=pd.read_csv(file, )
    data=data.append(df,ignore_index=True)
    
 

os.chdir(r"C:\OGGA dataset\G House")
data.to_csv("combined_consumption_aggregate_iron_heater_hairdryer.csv", index = False)


data.Power.plot()