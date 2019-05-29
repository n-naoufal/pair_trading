# -*- coding: utf-8 -*-

#calculating sell price
def sell_price_cal(prev_status,prev_sell_price,status, df_, i):

    if status == prev_status:
        sell_price = prev_sell_price
    else:
        if status in ["SL","TP","CB",""]:
            sell_price = ""
        else:
            if df_.at[i,'signal'] == "BUY":
                sell_price = df_.at[i,'bid_NZD']
            else:
                if df_.at[i,'signal'] == "SELL":
                    sell_price = df_.at[i,'bid_AUD']
                else:
                    sell_price = ""

    return sell_price