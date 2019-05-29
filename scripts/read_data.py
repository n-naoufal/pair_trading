# -*- coding: utf-8 -*-
from pandas import read_excel, read_pickle, read_csv
from scripts.timeit import timeit

@timeit
def read_data(file1, file2, ind_red, stored):
    
    if (stored):
        # read from pickle
        df_all = read_pickle('data\df_all.pkl')
    else:
        # reading first file closing bid
        df_aud_bid = read_csv(file1[0],sep=";",header = 0,parse_dates = [0], usecols = [0,4] )
        df_aud_bid.columns = ["time","bid_AUD"]
        df_aud_bid = df_aud_bid.set_index('time')
        # reading first file closing ask
        df_aud_ask = read_csv(file1[1],sep=";",header = 0,parse_dates = [0], usecols = [0,4] )
        df_aud_ask.columns = ["time","ask_AUD"]
        df_aud_ask = df_aud_ask.set_index('time')
        
        # reading second file closing bid
        df_nzd_bid = read_csv(file2[0],sep=";",header = 0,parse_dates = [0], usecols = [0,4] )
        df_nzd_bid.columns = ["time","bid_NZD"]
        df_nzd_bid = df_nzd_bid.set_index('time')
        # reading second file closing ask
        df_nzd_ask = read_csv(file2[1],sep=";",header = 0,parse_dates = [0], usecols = [0,4] )
        df_nzd_ask.columns = ["time","ask_NZD"]
        df_nzd_ask = df_nzd_ask.set_index('time')
        
        
        # merging both dataframes together 
        df_all = df_aud_bid.join(df_aud_ask).join(df_nzd_bid).join(df_nzd_ask)
        df_all.bid_AUD = df_all.bid_AUD.str.replace(',', ".").astype(float)
        df_all.ask_AUD = df_all.ask_AUD.str.replace(',', ".").astype(float)
        df_all.bid_NZD = df_all.bid_NZD.str.replace(',', ".").astype(float)
        df_all.ask_NZD = df_all.ask_NZD.str.replace(',', ".").astype(float)
        df_all.to_pickle('data\df_all')
        

    # Let's reduce our dataset
    ind = df_all.index.get_loc(df_all.index.max())
    df_all = df_all.iloc[ind - ind_red:ind]
    return df_all