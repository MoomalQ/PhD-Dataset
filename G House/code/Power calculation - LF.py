# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 13:44:43 2021

@author: Moomal Qureshi

Original file : raw_to_power by Patrice Bouchand

@Moomal - Modified: updated to read per second data and convertion to pandas dataframe.

@Moomal - to do : write Vrms + Irms per sec to file also, the modified code from "updated_irms.py" works for single file with n = 3250
"""

#############################################################################
#                                                                           #
# File: raw_to_pow.py                                                       #
#                                                                           #
# Author:       Patrice Bouchand / OGGA / pbouchand@ogga.fr                 #
#                                                                           #
# Created:       26/05/2020                                                 #
#                                                                           #
#                                                                           #
#############################################################################

import math
import os
import pandas as pd
import datetime
import numpy as np


os.chdir(r"C:\OGGA dataset\G House\raw")
Path = r"C:\OGGA dataset\G House\raw"

# Coefficents

V_MAX_EDF = 332.
V2A_Coeff = 0.027

V_OFFSET=0.02470703050494194
COEFF_FIX=1.0150198936462402
PIP=0
PIST=462
ADC_CAL_BC=0.0074799917638301849
ADC_CAL_MC=0.0031714583747088909

#define ADC_TO_V( ADC ) ( ADC * Adc_Cal_Mc + Adc_Cal_Bc )

SIN_TAB_MAX  =  ( 1 << 13 )                     #8192 = 2^13
SIN_TAB_MASK =  ( SIN_TAB_MAX - 1 )
Sin_Tab = [0] * SIN_TAB_MAX                     #list of 8192 initialized to zero

for c in range(0, SIN_TAB_MAX ):
    Sin_Tab[ c ] = math.sin ( (2 * math.pi * c ) / SIN_TAB_MAX );

# Data


#filestring= "TO_20181213_1622.raw.done.A1_IRON_HEATER_HAIRDRIER.txt"  # file lenght few seconds long, perhaps registering single device activation
#filestring = "TO_20181213_1623.raw.done.A1_IRON_HEATER_HAIRDRIER.txt"  # 60 second interval , multiple device activation visible
#filestring_3 = "TO_20181213_1624.raw.done.A2_IRON_HEATER_HAIRDRIER.txt"  # file lenght few seconds long, perhaps registering single device activation
#filestring = "TO_20181213_1625.raw.done.A2_IRON_HEATER_HAIRDRIER.txt"  # 60 second interval , multiple device activation visible
#filestring = "TO_20181213_1626.raw.A2_IRON_HEATER_HAIRDRIER.txt"       # 60 second interval, multiple device activation
#filestring_6 = "TO_20181213_1627.raw.done.A3_HEATER_HAIRDRIER_LAPTOP.txt" # 30 second, multiple device activation
#filestring_7 = "TO_20181213_1629.raw.done.A4_HEATER_HAIRDRIER_LAPTOP.txt"# 41 second,multiple device activation
#filestring = "TO_20181213_1632.raw.done.A5_HEATER_HAIRDRIER_LAMP.txt"   #60 second, multiple device activaion
#filestring_9 = "TO_20181213_1630.raw.A4_HEATER_HAIRDRIER_LAPTOP.txt"      #30 second, multiple device activation
#filestring_10 = "TO_20181213_1633.raw.A5_HEATER_HAIRDRIER_LAMP.txt"       #40 second, multiple activation not visible




#############################################################################
import time
Step_Sample = ( 1 / 3300. )

def load_data_ghiaus_house(filestring):

    Bn = os.path.basename( filestring )
    Lst = Bn.split(".")[0].split( "_" )
    Start_Str = "%s%s" % ( Lst[1], Lst[2] )
    #print(Start_Str)
    Start = int( time.mktime(time.strptime( Start_Str, '%Y%m%d%H%M' ) ) )

    f = open ( filestring, 'r')
    txt_data = []
    txt_data= [ line.split() for line in f]

    data = []

    T = []
    V =[]
    I = []

    for reading in txt_data:
        if reading == [] or () or None :
            continue
        else:

            #data.append(float(Start),int(reading[1]),int(reading[0]))
            #data.append(int(reading[1]))
            V = int(reading[0])
            #data0.append(int(reading[0]))
            I = int(reading[1])
            #data1.append(float(Start))
            T = float(Start)
            Start += Step_Sample


            data.append( ( float(T),int(V),int(I) ) )



    #data=np.array(data)
    #data0=np.array(data0)
    #data1=np.array(data1)
    return  data

#############################################################################
def Compute_Raw_Data( Raw_Data, File ):
    N_Point_Measured = 0
    count = 0

    Sync_Edge_T = None
    N_Points_Since_Edge = 0
    Sync_Edge_Detected_Num = 0

    E = 0.0

    Last_T, Last_V, _ = Raw_Data[0]

    Sum_E = 0
    Sum_T = 0

    df_power = pd.DataFrame( columns = ["Time stamp","Power"], index = [0] )
    filename_power = "Toydata_Created_"
    filename_power += str( datetime.date.today( ) )
    filename_power += ".csv"

    V_sec = []
    I_sec = []
    E_sec = []


    for i in range( 1, len( Raw_Data ) - 5 ):

        T, V, Adc_V_Tore = Raw_Data[ i ]            #Removing T because toy dataset doesn't have T
        N_Points_Since_Edge += 1

        Sync_Edge_Detected = ( ( Last_V - Raw_Data[ i + 5][1] > 20 )  and ( Last_V > V ) ) and ( N_Points_Since_Edge > 20 )

        if Sync_Edge_Detected:

            Sync_Edge_Detected_Num += 1

            if Sync_Edge_T != None:

                if ( N_Points_Since_Edge > 65 ) and ( N_Points_Since_Edge < 69 ):
                    Sum_E +=  E
                    Sum_T += ( Last_T - Sync_Edge_T )

            # Energy is summed and power is displayed when time is greater then 0.9 sec
            if Sum_T > 0.9:
                #print (T, COEFF_FIX * abs( Sum_E / Sum_T ))
                to_append =[T, COEFF_FIX * abs( Sum_E / Sum_T )]
                a_series = pd.Series(to_append, index = df_power.columns)
                df_power = df_power.append(a_series, ignore_index=True)
                count+=1                                                       #check how many cycles we have counted in the file
                Sum_E = 0
                Sum_T = 0

            Sync_Edge_T = T
            N_Points_Since_Edge = 0
            E = 0

        if ( Sync_Edge_T != None ) and ( N_Points_Since_Edge > 0 ):

            # Instant voltage calculation
            k = int( ( SIN_TAB_MAX * ( T - Sync_Edge_T + PIST ) ) / 0.02 ) & SIN_TAB_MASK
            V_In_Volt = V_MAX_EDF * Sin_Tab[ k ]
            V_sec.append(V_In_Volt)

            # Instant intensity/ current calculation
            V_Tore = max( ( Adc_V_Tore * ADC_CAL_MC + ADC_CAL_BC ) - V_OFFSET, 0 )
            I_In_Ampere = V_Tore / V2A_Coeff
            I_sec.append(I_In_Ampere)

            # Instant energy
            E += 2 * I_In_Ampere * V_In_Volt * ( T - Last_T )
            E_sec.append(E)

        Last_T = T
        Last_V = V

    df_power = df_power.dropna( axis = 0, how = 'any' )
    df_power = df_power.reset_index( drop = True )
    df_power[ 'Time stamp' ] = pd.to_datetime( df_power[ 'Time stamp' ] , unit = 's' )   # Converting timestamp to utc
    df_power.set_index( 'Time stamp' , inplace = True )
    if not os.path.isfile( filename_power ):
        df_power.to_csv( filename_power )
    else:
        df_power.to_csv( filename_power, mode = 'a', header = False )

    #count
    print("Total cycles counted",count)
    #sleep(1)

    return E_sec,V_sec, I_sec




#############################################################################

for File in os.listdir( Path ):

    Raw_Data = load_data_ghiaus_house( File)
    E_sec, V_sec, I_sec = Compute_Raw_Data( Raw_Data, File)
    
    
    
   
# d_I = I_sec
# d_V = V_sec

# def calc_power_sec(d_V, d_I):

#     '''
#     Input:   Voltage, Current
#     Output:  Calculate , Irms, App_Power
#     '''

       
#     sq_v=np.square(d_V)
#     sum_v=np.sum(sq_v, axis=1)
#     #print("Here")
#     Vrms=np.sqrt(sum_v/3250)
#     Vrms=220      
    
    
#     sq_i=np.square(d_I)
#     tot_sum_i=np.sum(sq_i,axis=1)
#     Irms=np.sqrt((tot_sum_i*2)/3250)    
    
#     App_Power=Vrms*Irms
   

#     return (Vrms, Irms, App_Power)


# n = 3250                                                                # number of datapoints in the list 

# d_V = [d_V [ i * n : ( i + 1 )  * n ] for i in range( ( len ( d_V ) + n - 1) // n ) ]   #Reshape data

# d_I = [ d_I[ i * n : ( i + 1 ) * n ] for i in range( ( len ( d_I ) + n - 1) // n ) ]   
    
# drop_index = len( d_V )-1                                                   #dropping last index

# d_V = pd.DataFrame( d_V )

# d_V = d_V.drop( drop_index )
    
# d_I = pd.DataFrame( d_I )

# d_I = d_I.drop( drop_index )   

# #calculate dataframe Vrms, Irms, Active Power , Reactive Power
    
# Vrms, Irms, App_Power = calc_power_sec( d_V , d_I )

# df =pd.read_csv("Toydata_Created_2021-04-01.csv")
# import matplotlib.pyplot as plt
# plt.figure()
# plt.plot(df["Power"])


# df["Irms"] = I_sec
# df["Vrms"] = V_sec

# plt.plot(df["Irms"]*df["Vrms"])

# new = df.to_csv("updated_irms_toy.csv")


