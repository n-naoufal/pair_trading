# -*- coding: utf-8 -*-

def signal_cal(row, strategy, threshold):
    if (strategy == 1):
        if row["Z_score"] > threshold and row["adftest"] == 'YES':
            return 'SELL' 

        elif row["Z_score"] < - threshold and row["adftest"] == 'YES':
            return 'BUY'

        else:
            return ''
    elif  (strategy == 2):
        if row["Z_score"] > threshold and row["adftest"] == 'YES':
            return 'BUY' 

        elif row["Z_score"] < - threshold and row["adftest"] == 'YES':
            return 'SELL'

        else:
            return ''