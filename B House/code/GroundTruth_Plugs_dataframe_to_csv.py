# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 23:48:10 2019

@author: mqureshi

Making plug dataset

"""

import pandas as pd
import os
os.system('cls')
os.chdir(r"C:\Patrice_Home_March_2019\data")
def load_file_plug(filestring):
    
    f = open ( filestring, 'r') 
    txt_data = []
    txt_data= [ line.split() for line in f]
    df1 = pd.DataFrame(columns = ["Time stamp","Power"], index = [0])
    
    for reading in txt_data: 
        if reading == [] or () or None :
            continue
        else: 
            data={"Time stamp":reading[0], "Power":reading[1] }
            df2= pd.DataFrame(data, index=[1])
            df1=df1.append(df2, ignore_index=True)
            
    
    return df1


# Plug # 1

file ="AU-01553184825-1-56-179010.mes.txt"
device_name ="Autre plug 1"

plug= load_file_plug(file)
plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plug

#plug # 2

file ="AU-01553363835-1-56-179058.mes.txt"
device_name ="Autre plug 2"

plug= load_file_plug(file)
plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug)                 


# PLUG # 03
file ="CH-01553181601-1-56-175983.mes.txt"
device_name ="Chauffage plug 3"

plug= load_file_plug(file)
plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')   

plugs=plugs.append(plug)                      


# Plug # 04

file = "CH-01553357584-1-56-176307.mes.txt"
device_name ="Plug 4 electrique Chauffage"

plug= load_file_plug(file)
plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  
plugs=plugs.append(plug)                       


#PLUG # 5 
file="ENO_RR00-01553005945-1-56-312854-21-05069B35.mes.txt"
device_name ="Plug 5"

plug= load_file_plug(file)
plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug)     

#plug # 06

file = "ENO_SP00-01553005948-1-56-311047-21-01A30151.mes.txt"
device_name ="Repasser Plug 6"

plug= load_file_plug(file)
plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  
plugs=plugs.append(plug)                     

#Plug # 07  

file = "ENO_SP01-01553005946-1-56-314419-21-01A31987.mes.txt"
device_name ="Salon Plug 7"

plug=load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')                
plugs=plugs.append(plug)  



#plug # 08


file = "ENO_SP03-01553005939-1-56-303678-21-01A2F845.mes.txt"
device_name ="Lamp Office Plug 8"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug)                   


print("here")
#plug # 09

file = "ENO_SP04-01553005944-1-56-311413-21-0194A9E1.mes.txt"
device_name ="Chambre Plug 9"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')   
plugs=plugs.append(plug)      


plug # 10

file = "ENO_SP06-01553006722-1-56-473242-21-0087A28C.mes.txt"
device_name ="Plug 10 Lave Vaisselles"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug) 


#plug # 11

file = "ENO_SP07-01553007401-1-56-381444-21-00874B2E.mes.txt"
device_name ="Laver Plug 11"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug)                      

#plug # 12

file = "ENO_VMC2S00-01553005950-1-56-311500-21-0194BE2A.mes.txt"
device_name ="Plug 12"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')   
plugs=plugs.append(plug)    


#plug # 13

file = "PR-01553174934-1-56-168950.mes.txt"
device_name ="Plug 13  Aggregate"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug) 


#plug # 14

file = "PR-01553343884-1-56-168064.mes.txt"
device_name =" Plug 14 Aggregate consumption"

plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug) 

#plug # 15

file = "TO-01553184825-1-56-179010.mes.txt"
device_name ="Plug 15 Aggregate"


plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug) 


#plug # 16

file = "TO-01553363835-1-56-179058.mes.txt"
device_name ="Plug 16 Aggregate"


plug= load_file_plug(file)
#plug= plug.astype(float) 
plug['Device']=device_name 
plug['Time stamp'] = pd.to_datetime(plug['Time stamp'],unit='s')
plug =plug.set_index('Time stamp')  

plugs=plugs.append(plug)

print("HERE")
plugs.to_csv("Plug_data.csv")

# Saving device names 
Device_names=pd.Series(plugs['Device']).unique()
# selecting specific values 

plugs[plugs['Device'].str.contains("plug 1")]

