# -*- coding: utf-8 -*-

#calculating buy price
def buy_price_cal(prev_status,prev_buy_price,status, df_, i):

    if status == prev_status:
        buy_price = prev_buy_price
    else:
        if status in ["SL","TP","CB",""]:
            buy_price = ""
        else:
            if df_.at[i,'signal'] == "BUY":
                buy_price = df_.at[i,'ask_AUD']
            else:
                if df_.at[i,'signal'] == "SELL":
                    buy_price = df_.at[i,'ask_NZD']
                else:
                    buy_price = ""
    return buy_price