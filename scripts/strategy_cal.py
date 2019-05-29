# -*- coding: utf-8 -*-

from scripts.mtm_cal import mtm_cal
from scripts.status_cal import status_cal
from scripts.buy_price_cal import buy_price_cal
from scripts.sell_price_cal import sell_price_cal
from scripts.timeit import timeit

@timeit
def strategy_cal(df_, period, N, M, SL, TP):
    pnl = 0
    prev_status = ""
    prev_sell_price = ""
    prev_buy_price = ""
    for i in df_.index:
        #calculate mtm
        mtm = mtm_cal(prev_status,prev_sell_price,prev_buy_price, M, N, df_, i)

        #assigning status
        status = status_cal(prev_status,mtm, SL, TP,df_, i)

        #assigning buy_price
        buy_price = buy_price_cal(prev_status,prev_buy_price,status, df_, i)


        #assigning sell_price
        sell_price = sell_price_cal(prev_status,prev_sell_price,status, df_, i)

        #calculate pnl
        pnl = (pnl + mtm) if status in ["TP","SL","CB"] else pnl

        #assigning prev values
        prev_sell_price = sell_price
        prev_status = status
        prev_buy_price = buy_price

        #appending calculations to the data array
        df_.set_value( i,'status',status)
        df_.set_value( i,'mtm',mtm)
        df_.set_value( i,'sell_price',sell_price)
        df_.set_value( i,'buy_price',buy_price)
        df_.set_value( i,'pnl',pnl)
        
    return df_