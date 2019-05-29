# -*- coding: utf-8 -*-

#calculating mtm
def mtm_cal(prev_status,prev_sell_price,prev_buy_price, M, N, df_, i):
    if prev_status == "BUY":
        mtm = (prev_sell_price-df_.at[i,'ask_NZD'])*M + (df_.at[i,'bid_AUD']-\
               prev_buy_price)*N if prev_buy_price else 0
    else:
        if prev_status == "SELL":
            mtm =(prev_sell_price-df_.at[i,'ask_AUD'])*N +(df_.at[i,'bid_NZD']\
                   -prev_buy_price)*M if prev_buy_price else 0
        else:
            mtm = ""

    return mtm
