# -*- coding: utf-8 -*-
from scripts.timeit import timeit
from numpy import log

@timeit
def zscore(df_,lag):
    log_ratio = log(df_["ask_AUD"]) - log(df_["ask_NZD"])
    log_avg_lag = log_ratio.rolling(window=lag).mean()
    log_std_lag = log_ratio.rolling(window=lag).std()
    df_["Z_score"] = (log_ratio - log_avg_lag)/log_std_lag
    df_["Z_score"] = df_["Z_score"].fillna(0)
    return df_