# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 19:14:52 2021

@author: useradmin
"""


from scipy.signal import correlate
import time
import logging
import math
import os
from time import sleep
import pandas as pd
import datetime
import numpy as np
from matplotlib import style
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
style.use('default')
np.seterr(divide='ignore', invalid='ignore')
#plt.rcParams['figure.constrained_layout.use'] = True

params = {'figure.autolayout': True,
          'font.family': 'Times New Roman',
          'figure.figsize': (7, 3),
          'legend.fontsize': 10.0,
          'xtick.labelsize': 10.0,
          'ytick.labelsize': 10.0,
          'font.size': 10.0,
          'lines.linewidth': 1.8

          }
pylab.rcParams.update(params)
plt.rcParams["font.family"] = "Times New Roman"


os.chdir(r"C:\OGGA dataset\G House\raw")
Path = r"C:\OGGA dataset\G House\raw"

# Coefficents

V_MAX_EDF = 332.
V2A_Coeff = 0.027

V_OFFSET = 0.02470703050494194
COEFF_FIX = 1.0150198936462402
PIP = 0
PIST = 462
ADC_CAL_BC = 0.0074799917638301849
ADC_CAL_MC = 0.0031714583747088909

# define ADC_TO_V( ADC ) ( ADC * Adc_Cal_Mc + Adc_Cal_Bc )

SIN_TAB_MAX = (1 << 13)  # 8192 = 2^13
SIN_TAB_MASK = (SIN_TAB_MAX - 1)
Sin_Tab = [0] * SIN_TAB_MAX  # list of 8192 initialized to zero

for c in range(0, SIN_TAB_MAX):
    Sin_Tab[c] = math.sin((2 * math.pi * c) / SIN_TAB_MAX)

Step_Sample = (1 / 3300.)


def m_load_data_ghiaus_house(filestring):

    Bn = os.path.basename(filestring)
    Lst = Bn.split(".")[0].split("_")
    Start_Str = "%s%s" % (Lst[1], Lst[2])
    # print(Start_Str)
    Start = int(time.mktime(time.strptime(Start_Str, '%Y%m%d%H%M')))

    f = open(filestring, 'r')
    txt_data = []
    txt_data = [line.split() for line in f]

    data = []

    T = []
    V = []
    I = []

    data_T = []
    data_V = []
    data_I = []

    for reading in txt_data:
        if reading == [] or () or None:
            continue
        else:

            # data.append(float(Start),int(reading[1]),int(reading[0]))
            # data.append(int(reading[1]))
            V = int(reading[0])
            # data0.append(int(reading[0]))
            I = int(reading[1])
            # data1.append(float(Start))
            T = float(Start)
            Start += Step_Sample

            #data.append( ( float(T),int(V),int(I) ) )
            data_T.append(float(T))
            data_V.append(int(V))
            data_I.append(int(I))

    # data=np.array(data)
    # data0=np.array(data0)
    # data1=np.array(data1)
    return data_T, data_V, data_I


def load_data_ghiaus_house(filestring):

    Bn = os.path.basename(filestring)
    Lst = Bn.split(".")[0].split("_")
    Start_Str = "%s%s" % (Lst[1], Lst[2])
    # print(Start_Str)
    Start = int(time.mktime(time.strptime(Start_Str, '%Y%m%d%H%M')))

    f = open(filestring, 'r')
    txt_data = []
    txt_data = [line.split() for line in f]

    data = []

    T = []
    V = []
    I = []

    for reading in txt_data:
        if reading == [] or () or None:
            continue
        else:

            # data.append(float(Start),int(reading[1]),int(reading[0]))
            # data.append(int(reading[1]))
            V = int(reading[0])
            # data0.append(int(reading[0]))
            I = int(reading[1])
            # data1.append(float(Start))
            T = float(Start)
            Start += Step_Sample

            data.append((float(T), int(V), int(I)))

    # data=np.array(data)
    # data0=np.array(data0)
    # data1=np.array(data1)
    return data

#############################################################################


def Compute_Raw_Data(Raw_Data, File):

    N_Point_Measured = 0
    count = 0

    Sync_Edge_T = None
    N_Points_Since_Edge = 0
    Sync_Edge_Detected_Num = 0

    E = 0.0

    Last_T, Last_V, _ = Raw_Data[0]

    Sum_E = 0
    Sum_T = 0

    df_power = pd.DataFrame(columns=["Time stamp", "Power"], index=[0])
    filename_power = "toydata_"
    filename_power += str(datetime.date.today())
    filename_power += ".csv"

    V_sec = []
    I_sec = []
    E_sec = []
    T_sec = []

    for i in range(1, len(Raw_Data) - 5):

        #
        T, V, Adc_V_Tore = Raw_Data[i]
        N_Points_Since_Edge += 1

        Sync_Edge_Detected = (
            (Last_V - Raw_Data[i + 5][1] > 20) and (Last_V > V)) and (N_Points_Since_Edge > 20)

        if Sync_Edge_Detected:

            Sync_Edge_Detected_Num += 1

            if Sync_Edge_T != None:

                if (N_Points_Since_Edge > 65) and (N_Points_Since_Edge < 69):
                    Sum_E += E
                    Sum_T += (Last_T - Sync_Edge_T)

            # Energy is summed and power is displayed when time is greater then 0.9 sec
            if Sum_T > 0.9:
                #print (T, COEFF_FIX * abs( Sum_E / Sum_T ))
                to_append = [T, COEFF_FIX * abs(Sum_E / Sum_T)]

                #print("Sum_t", Sum_T)
                a_series = pd.Series(to_append, index=df_power.columns)
                df_power = df_power.append(a_series, ignore_index=True)

                count += 1  # check how many cycles we have counted in the file
                Sum_E = 0
                Sum_T = 0

            Sync_Edge_T = T
            N_Points_Since_Edge = 0
            E = 0

        if (Sync_Edge_T != None) and (N_Points_Since_Edge > 0):

            # Instant voltage calculation
            k = int((SIN_TAB_MAX * (T - Sync_Edge_T + PIST)) /
                    0.02) & SIN_TAB_MASK
            V_In_Volt = V_MAX_EDF * Sin_Tab[k]
            V_sec.append(V_In_Volt)

            # Instant intensity/ current calculation
            V_Tore = max((Adc_V_Tore * ADC_CAL_MC + ADC_CAL_BC) - V_OFFSET, 0)
            I_In_Ampere = V_Tore / V2A_Coeff
            I_sec.append(I_In_Ampere)
            #print("I_in_ampere", Adc_V_Tore)

            # Instant energy
            E += 2 * I_In_Ampere * V_In_Volt * (T - Last_T)
            #print("T", T, "Last_T", Last_T, "diff", T - Last_T)
            E_sec.append(E)
            
            T_sec.append(T)

        Last_T = T
        Last_V = V

    df_power = df_power.dropna(axis=0, how='any')
    df_power = df_power.reset_index(drop=True)
    df_power['Time stamp'] = pd.to_datetime(
        df_power['Time stamp'], unit='s')   # Converting timestamp to utc
    df_power.set_index('Time stamp', inplace=True)
    if not os.path.isfile(filename_power):
        df_power.to_csv(filename_power)
    else:
        df_power.to_csv(filename_power, mode='a', header=False)

    # count
    # print("Total cycles counted", count)
    sleep(1)

    return E_sec, V_sec, I_sec,T_sec


#############################################################################


#############################################################################


List_of_files = os.listdir( Path )
len_file = len( List_of_files )
n_loaded = 0

for File in os.listdir( Path ):
    
    n_loaded += 1
    print( "loaded ......", n_loaded , "out of " , len_file )
    # Raw_Data = Load_Raw( File )
    # Compute_Raw_Data( Raw_Data, File )
    
    
    
    
    # 60 second interval , multiple device activation visible"
    # File = "TO_20181213_1623.raw.done.A1_IRON_HEATER_HAIRDRIER.txt"
    
    Raw_Data = load_data_ghiaus_house(File)
    E_sec, V_sec, I_sec,T_sec = Compute_Raw_Data(Raw_Data, File)
    
    # plt.plot(I_sec)
    # plt.plot(E_sec)
    #data = pd.read_csv("toydata_2020-06-15.csv")
    
    d_I = I_sec
    d_V = V_sec
    T_sec = np.array(T_sec) #convert to numpy array
    
    t_dim0 = int(T_sec.shape[0]/69)
    extra = len(T_sec)%69
    T_sec = T_sec[:-extra]
    T_sec = T_sec.reshape(t_dim0,69)
    
    
    #d_I,d_V = load_data_ghiaus_house((File ))
    
    # d_I = d_I[3245:3530+69*10]
    # d_V = d_V[3245:3530+69*10]
    # length =int( len(d_I)/69)
    # d_I = d_I[3245:3530+69*length]
    # d_V = d_V[3245:3530+69*length]
    
    #E_sec = E_sec[3200:3200+330]
    
    plt.rcParams["font.family"] = "Times New Roman"
    
    # t = np.linspace(0, 3300, len(d_I))
    
    # t = np.linspace(0, .1, 330)
    data1 = d_I
    data2 = d_V
    fig, ax1 = plt.subplots()
    
    color = 'red'
    ax1.set_xlabel('Time (ms)', fontsize=12)
    ax1.set_ylabel('Current (A)', color=color, fontsize=12)
    # ax1.plot(t, data1, color=color)
    ax1.plot(data1, color=color)
    
    ax1.tick_params(axis='y', labelcolor=color)
    plt.ylim(-9, 9)
    ax1.xaxis.major.formatter._useMathText = True
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'blue'
    # we already handled the x-label with ax1
    ax2.set_ylabel('Voltage (V)', color=color, fontsize=12)
    ax2.plot(d_V, color=color,  linestyle='dashed')
    
    # ax2.plot(t, d_V, color=color,  linestyle='dashed')
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    
    
    # Modification : Calculating zero crossing so that instead of 1 sec..
    # we extract features from cycle to cyle
    
    
    
    def calculateTheta_cycle(current, voltage):
    
        nsamples = current.size
    
        # regularize datasets by subtracting mean and dividing by s.d
        current -= current.mean()
        current /= current.std()
        voltage = voltage - voltage.mean()
        voltage = voltage/voltage.std()
    
        # Find cross-correlation
        xcorr = correlate(voltage, current)
    
        # delta time array to match xcorr
        dt = np.arange(1-nsamples, nsamples)
        recovered_time_shift = dt[xcorr.argmax()]
        # print("Recovered time shift: ", (recovered_time_shift))
    
        frequency = 50
        Sampling_frequency = 3450
        wave_period = 1/frequency
        time_delay = (1/Sampling_frequency)*recovered_time_shift
        theta_degree = 90*time_delay/wave_period
        theta_radians = (2*3.14*time_delay)/wave_period
        # print("Phase in degree :", theta_degree)
        # print("Phase in radians :", theta_radians)
    
        return theta_degree, theta_radians, recovered_time_shift
    
    
    def calculatePower_cycle(current, voltage):
    
        n = len(current)
        Power_features = np.empty([n, 9])
        for i in range(n):
            # extract current and voltage in two cycle
            # extract current and voltage in two cycle
            temp_I = current[i]
            temp_V = voltage[i]
            Irms = np.mean(temp_I**2)**0.5
            Vrms = np.mean(temp_V**2)**0.5
            # Vrms = 0.7071*np.max(temp_V)
            # Irms = 0.7071*np.max(temp_I)
    
            deg, rad, time_shift = calculateTheta_cycle(temp_I, temp_V)
    
            # print("\n\n Recovered time shift: {0}, deg {1},rad {2} ".format(
                # time_shift, deg, rad))
    
            # Instantaneous power: obtained by multiplying the instantaneous voltage and current values
            Pinst = temp_I * temp_V
            Pactive = 2*(np.mean(Pinst))  # because half cycle is used
    
            # Apparent power: obtained by multiplying the RMS values of voltage and current
            Papparent = Vrms*Irms  # FROM s = VI WHEN WE CALCULATE V = 0.7071*VPEAK
    
            # Ractive power if power triangle holds:
            # from S = \sqrt(P^2 + Q^2)
            Preactive = np.sqrt(Papparent**2 - Pactive**2)
    
            # active power = P = VI cos theta
            P = Vrms*Irms*np.cos(rad)
            # reactive power = Q = VI sind theta
            Q = Vrms*Irms*np.sin(rad)
            S = np.sqrt(np.square(P)+np.square(Q))
    
            # P=abs(Vrms*Irms*np.cos(theta_radians))
            # Q=Vrms*Irms*np.sin(theta_radians)
    
            Power_features[i, 0] = Pactive
            Power_features[i, 1] = Preactive
            Power_features[i, 2] = Papparent
            Power_features[i, 3] = Vrms
            Power_features[i, 4] = Irms
            Power_features[i, 5] = P
            Power_features[i, 6] = Q
            Power_features[i, 7] = S
            Power_features[i, 8] = rad
            
            
    
        return Power_features
    
    # calcualte zero crossing
    
    
    def zero_crossings(voltage):
        zero_crossing = np.where(np.diff(np.signbit(voltage)))[0]
    
        return zero_crossing
    
    
    zc = zero_crossings(d_V)
    
    zc_print = []
    for i in range(0, len(d_V)):
    
        if i in zc:
            zc_print.append(330)
        else:
            zc_print.append(0)
    
    # print(zc_print)
    
    
    # plt.stem(zc_print)
    
    # print("zero_crossing location",zc)
    
    # Identify and extract one cycle of current and voltage
    
    i = 0
    start = zc[i]
    current_cycle = np.zeros(69)
    voltage_cycle = np.zeros(69)
    count = 1
    
    # while i < len(zc):
    while i < len(zc):
    
        if(i+2 < len(zc)):
            i += 2
    
        else:
            break
    
        # i = i+2
        end = zc[i]
        # print("start {0},end {1}, iteration {2}".format(start, end, count))
        count += 1
    
        # CURRENT  CYCLE
    
        sel_c = d_I[start:end]
        diff = 69 - len(sel_c)
        # print("diff", diff, "count", count)
        if(diff >= 0):
            ap_len = np.zeros(diff)
            sel_c = np.append(sel_c, ap_len)
            # print("length", len(sel_c))
            current_cycle = np.vstack((current_cycle, sel_c))
            # current_cycle[:, 64:67] = 0  # correct the value
        elif(diff<0):
            sel_c = sel_c[:diff]
            current_cycle = np.vstack((current_cycle, sel_c))
            
    
      #   sel_v = d_V[start:end]
      #   diff = 69 - len(sel_v)
      # # ap_len = np.zeros(diff)
        # sel_v = np.append(sel_v, ap_len)
        # print("length", len(sel_v))
        start = end
    
        # voltage_cycle= np.vstack((voltage_cycle, sel_v))
    
    
    sel_v = d_V[zc[0]:zc[2]]
    diff = 69 - len(sel_v)
    app_v = np.zeros(diff)
    sel_v = np.append(sel_v, app_v)
    
    sel_v=list(sel_v)
    sel_v = sel_v*current_cycle.shape[0]
    sel_v = np.array(sel_v)
    voltage_cycle = sel_v.reshape(-1, 69)
    print(voltage_cycle.shape)
    
    
    
    # Time 
    
    
    PQ = calculatePower_cycle(current_cycle[1:,:], voltage_cycle[1:,:])
    
    # def calculate_harmonics(current,voltage):
    #     # Calculate harmonics not for single cycle because the number of samples
    #     # are two few for getting higher order harmonics. 69 samples per cycle
    #     # and according to nyquist criteria there should be atleast 2 the amount 
    #     # to get a single harmonic. 
    #     n_harmonics = 12
        
    #     n = len(current)
    #     harmonics = np.empty([n, n_harmonics])
    #     for i in range(n):
    #         # extract current and voltage in two cycle
    #         # extract current and voltage in two cycle
    #         temp_I = current[i]
    #         temp_V = voltage[i]
    #         Pinst = temp_I * temp_V      
    #         y = np.abs(np.fft.fft(Pinst))        
    #         harmonics[i,:]=y[:n_harmonics]  
           
    #     return harmonics
    
    
    
    # harmonics = calculate_harmonics(current_cycle[1:,:],voltage_cycle[1:,:])
    time_d = T_sec[:,0]
    time_d = pd.DataFrame(data = time_d , columns = ["Time"])
    
    P_features = PQ
    # P_features = np.hstack((PQ,harmonics))
    #Power = pd.DataFrame(data = P_features, columns =["P_active","P_reactive","Papperant","Vrms","Irms","P","Q","S","theta_rad","h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12"])
    Power = pd.DataFrame(data = P_features, columns =["P_active","P_reactive","Papperant","Vrms","Irms","P","Q","S","theta_rad"])

    Power["Time"]=time_d["Time"]
    
    
    
    Power = Power.dropna(axis=0, how='any')
    Power = Power.reset_index(drop=True)
    Power['Time'] = pd.to_datetime(
        Power['Time'], unit='s')   # Converting timestamp to utc
    Power.set_index('Time', inplace=True)
    if not os.path.isfile("Power_features_complete.csv"):
        Power.to_csv("Power_features_complete.csv",header=True)
    else:
        Power.to_csv("Power_features_complete.csv", mode='a', header=False)
    
    # Power.to_csv("Power_features_complete.csv",index =False)
