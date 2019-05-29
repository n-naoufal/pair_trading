# -*- coding: utf-8 -*-
"""
Created on 28 november 2018
@author: Naoufal NIFA
"""
# Import developped package 
#------------------------------------------------------------------------------
from scripts.stat_arb import stat_arb

# File parameters
#------------------------------------------------------------------------------
# first asset
file1_bid = r"data\AUDUSD_1 Min_Bid_2016.09.05_2017.06.20.csv"
file1_ask = r"data\AUDUSD_1 Min_Ask_2016.09.05_2017.06.20.csv"
file1 = [file1_bid,file1_ask]
#second asset
file2_bid = r"data\NZDUSD_1 Min_Bid_2016.09.05_2017.06.20.csv"
file2_ask = r"data\NZDUSD_1 Min_Ask_2016.09.05_2017.06.20.csv"
file2 = [file2_bid,file2_ask]

# use stored pickle files once generated 
stored = False # whether a pickle file is stored or not

# file frequency & time parameters 
nbr_hours_day = 24 # from 0.00 a.m to 11.59p.m 
red_per = 1 # in the file possible values 0 for seconds, 1 for minutes, 2 for hours
freq = 1 # frequency in the file

# Startegy
strategy = 2    # 1 mean reversing strategy /  2 trend tracking  


# co-integration parameters 
#------------------------------------------------------------------------------
# adf test 
period_adf = [2,2.2,2.3] # in days
strategy_adf = 1  # 1 mean of (60,90,120), 2 for weighted average, 3 all three t-stat < critical value, 4 min(t_stat) <critical_value
confidence_percentage = 10 #confidence percentage for the statistic test -- critical_value = -2.57


# Z-score parameters 
#------------------------------------------------------------------------------
lag = 100 # for Zscore lag in minuts
threshold = 1.3


# Real tested period
#------------------------------------------------------------------------------
red_per_h = 0 # hour
red_per_m = 0 # minute 
red_per_d = 200 # day 

# Trading parameters
#------------------------------------------------------------------------------
N=1 #lot size for AUD
M=1 #lot size for NZD
multiple_backtests = False
pip_unit = 0.0001

# Perform multiple or single backtests
#------------------------------------------------------------------------------

#multiple backtests
l = []
if multiple_backtests:
    for sl in range(-8, -7):
        for tp in range(8,9):
            sl *= pip_unit
            tp *= pip_unit
            
            print("ESSAI: SL=" + str(sl) + "pips TP=" + str(tp) + "pips")
            df = stat_arb(file1, file2, strategy, period_adf, strategy_adf, lag, confidence_percentage \
             ,threshold, pip_unit, sl, tp, N, M, stored, red_per_d, red_per_h, red_per_m, red_per, nbr_hours_day, freq)
            res = df["pnl"].iloc[-1]
            if res != "null":   
                l.append([sl,tp,res])
    print(l)
else:
    # Single backtest
    sl = -108
    tp = 150
    sl *= pip_unit
    tp *= pip_unit
    df = stat_arb(file1, file2,strategy,  period_adf, strategy_adf, lag, confidence_percentage \
             ,threshold, pip_unit, sl, tp, N, M, stored, red_per_d, red_per_h, red_per_m, red_per, nbr_hours_day, freq)
    res = df["pnl"].iloc[-1]
    if res != '':
        print("PNL:",round(res * int(1/pip_unit),1),"pips")    