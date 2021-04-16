#!/usr/bin/python
# -*- coding: utf-8 -*-

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
"""
@Moomal: Updated to read the per second data, and convert to pandas dataframe.
"""
import logging
import math
import os
from time import sleep
import pandas as pd
import datetime

os.chdir(r"C:\Patrice_Home_March_2019\txt\20190322")
Path = r"C:\Patrice_Home_March_2019\txt\20190322"

#os.chdir(r"C:\Patrice_Home_March_2019\txt\20190323")
#Path = r"C:\Patrice_Home_March_2019\txt\20190323"


V_OFFSET = 0.029257809743285179
COEFF_FIX = 1.0286532640457153
PIP = 0
PIST = 383
ADC_CAL_BC = 0.01134735532104969
ADC_CAL_MC = 0.0031619332730770111

V_MAX_EDF = 332.
V2A_Coeff = 0.027

#define ADC_TO_V( ADC ) ( ADC * Adc_Cal_Mc + Adc_Cal_Bc )

SIN_TAB_MAX  =  ( 1 << 13 )                     #8192 = 2^13
SIN_TAB_MASK =  ( SIN_TAB_MAX - 1 )
Sin_Tab = [0] * SIN_TAB_MAX                     #list of 8192 initialized to zero

for c in range(0, SIN_TAB_MAX ):
    Sin_Tab[ c ] = math.sin ( (2 * math.pi * c ) / SIN_TAB_MAX );

#############################################################################
def Load_Raw( File ):

    f = None
    
    Rtn = []

    try:
        f = open( File , 'r')

        while 1:
            l = f.readline()
            if not l:
                break
            T,V,I = l.split()

            Rtn.append( ( float(T),int(V),int(I) ) ) 

        f.close()
    except IOError:
        logging.warn( "Unable to read "+File )
        return None

    return Rtn

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
    filename_power = "power_data_patrice_house_March_190322_modified_"
    filename_power += str( datetime.date.today( ) )
    filename_power += ".csv"
    
    
    for i in range( 1, len( Raw_Data ) - 5 ):
        
        T, V, Adc_V_Tore = Raw_Data[ i ]
        #print(T)
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
                to_append =[T,COEFF_FIX * abs( Sum_E / Sum_T )]
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
            
            # Instant intensity/ current calculation
            V_Tore = max( ( Adc_V_Tore * ADC_CAL_MC + ADC_CAL_BC ) - V_OFFSET, 0 )
            I_In_Ampere = V_Tore / V2A_Coeff
            
            # Instant energy 
            E += 2 * I_In_Ampere * V_In_Volt * ( T - Last_T )            
       
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
    #print("Total cycles counted",count)
    #sleep(1)
        


#############################################################################
List_of_files = os.listdir( Path )
len_file = len( List_of_files )
n_loaded = 0

for File in os.listdir( Path ):
    
    n_loaded += 1
    print( "loaded ......", n_loaded , "out of " , len_file )
    Raw_Data = Load_Raw( File )
    Compute_Raw_Data( Raw_Data, File )
    


