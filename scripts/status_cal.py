# -*- coding: utf-8 -*-

#defining status
def status_cal(prev_status,mtm, SL, TP, df_, i):
    if prev_status in ["","SL","TP","CB"]:
        status = df_.at[i,'signal']
    else:
        if df_.at[i,'adftest'] == "NO":
            status = "CB"
        else:
            if mtm == "":
                status = ""
            else:
                if mtm<SL:
                    status="SL"
                else:
                    if mtm>TP:
                        status="TP"
                    else:
                        status = prev_status

    return status