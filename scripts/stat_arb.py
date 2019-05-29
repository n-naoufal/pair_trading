# -*- coding: utf-8 -*-

# import script functions
from scripts.convert_time_index import convert_time_index
from scripts.read_data import read_data
from scripts.describe_data import describe_data
from scripts.adf_test import adf_test
from scripts.zscore import zscore
from scripts.signal_cal import signal_cal
from scripts.strategy_cal import strategy_cal
from scripts.timeit import timeit

# import package functions
from time import time
from datetime import datetime
from pandas import ExcelWriter, options
options.mode.chained_assignment = None

@timeit
def stat_arb(file1, file2, strategy, period_adf, strategy_adf, lag, confidence_percentage \
             ,threshold, pip_unit, SL, TP, N, M, stored, red_per_d, red_per_h, red_per_m, red_per, nbr_hours_day, freq):
    
    
# Reading & formatting data
#------------------------------------------------------------------------------
    print('')
    print('----> Reading & cleaning data')
    print('')
    
    ind_red = convert_time_index(red_per,period_adf, red_per_d, red_per_h, red_per_m, nbr_hours_day, freq)
    df_all = read_data(file1, file2, ind_red,stored)
 
# Statistical description
#------------------------------------------------------------------------------
    print('')
    print('----> data statistical description')
    print('')

    describe_data(df_all)

# Co-integration tests
#------------------------------------------------------------------------------
    print('')
    print('----> ADF test')
    print('')  
    
    start = time()
    l_row_per = []
    df_all["adftest"] = ""
    for per in period_adf:
        df_all["t-stat_"+ str(per)] = ""
        ind_red = convert_time_index(red_per, period_adf, per, 0, 0, nbr_hours_day, freq)
        l_row_per.append(ind_red)
    df_all["t-stat_mean"] = ""
    df_all["t-stat_pvalue"] = ""
    ind = df_all.index.get_loc(df_all.index.min()) + max(l_row_per)
    ind_max = df_all.index.get_loc(df_all.index.max())
    while(ind<ind_max):
        res = adf_test(ind, df_all, strategy_adf, l_row_per,confidence_percentage)
        df_all.iloc[ind:ind+60,4] = res[0]
        for i,per in enumerate(period_adf):
            df_all.iloc[ind:ind+60,5+i] = res[1][i]
        df_all.iloc[ind:ind+60,5+len(period_adf)] = res[2]
        df_all.iloc[ind:ind+60,6+len(period_adf)] = res[3]
        ind += 60
    end = time()
    print("adf_tests", round((end - start)/60,2), " min")

# Z-score
#------------------------------------------------------------------------------   
    print('')
    print('----> Z-score')
    print('')     
    df_all = zscore(df_all,lag)

# Signal description
#------------------------------------------------------------------------------   
    print('')
    print('----> Signal')
    print('')    
    
    start = time()
    df_all["signal"] = df_all.apply(signal_cal, args=(strategy, threshold,), axis=1)
    end = time()
    print("signal", round((end - start)/60,2), " min")

# Strategy: mtm/buy_price/sell_price/pnl
#------------------------------------------------------------------------------
    print('')
    print('----> Stratgey application')
    print('')       
    
    df_all["status"] = ""
    df_all["mtm"] = ""
    df_all["buy_price"] = ""
    df_all["sell_price"] = ""
    df_all["pnl"] = ""
    # skip first rows period
    mask = (df_all['adftest'] != "")
    #apply the strategy on those
    df_all.loc[mask] = strategy_cal(df_all[mask], max(period_adf), N, M, SL, TP)

# Export settings ( Excel)
#------------------------------------------------------------------------------
    print('')
    print('----> Export results')
    print('')
    
    res = df_all["pnl"].iloc[-1]
    if res != '':
        pnl_string = str(round(res * int(1/pip_unit),1)) 
    else:
        pnl_string = ""

    # name the output file 
    time_string = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
    adf_string = '-'.join([str(i) for i in period_adf])
    strategy_string = "mean_reversing" if (strategy == 1) else "trend_tracking "
    filename = "output/pair_strategy_"+strategy_string+ "_PNL_"+str(pnl_string)+"_SL_" +   \
                    str(round(SL*int(1/pip_unit))) + "_TP_" + str(round(TP*int(1/pip_unit))) +  \
                    "_Lag_" +str(lag) + "_ADF_" + adf_string + "_" +time_string + ".xlsx"
                    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = ExcelWriter(filename, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df_all.to_excel(writer,sheet_name='trades')
    
    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['trades']

    # Set up some formatting and text to highlight the panes.
    header_format = workbook.add_format({'bold': True,
                                     'align': 'center',
                                     'valign': 'vcenter',
                                     'fg_color': '#D7E4BC',
                                     'border': 1})
    worksheet.freeze_panes(1, 0)
    # Set the column width and format.
    worksheet.set_column('A:A', 20)
    for col,element in enumerate(df_all.columns):
        worksheet.write(0, col+1, element, header_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    return df_all
    
    
    