from statsmodels.api import OLS
from statsmodels.tsa.stattools import adfuller
from statistics import mean

def adf_test(ind, df_, strategy_adf, l_row_per,confidence_percentage):
    l = []
    exists = False
    for per in l_row_per:
        exists = True
        df_ind = df_.iloc[ind - per:ind].resample('H').mean()
        df_ind = df_ind[(df_ind.index.dayofweek < 5)]
        df_ind = df_ind.between_time('7:00', '19:59')
        x = df_ind["ask_AUD"]
        y = df_ind["ask_NZD"]
        model = OLS(x,y).fit() 
        l.append(adfuller(model.resid))
#        print([i for i in adfuller(model.resid)])

    if (exists):
        exists = False
        t_stat4 = l[0][4]
        if (strategy_adf == 1):
            t_stat0 = mean([i[0] for i in l])
            t_stat1 = mean([i[1] for i in l])
        elif (strategy_adf == 2):
            t_stat0 = sum(x * y for x, y in zip(l[0], l_row_per)) / sum(l_row_per)
            t_stat1 = sum(x * y for x, y in zip(l[1], l_row_per)) / sum(l_row_per)
        elif (strategy_adf ==3):
            t_stat0 = max([i[0] for i in l])
            t_stat1 = max([i[1] for i in l])
        elif (strategy_adf ==4):
            t_stat0 = min([i[0] for i in l])
            t_stat1 = min([i[1] for i in l])
            

    if t_stat0 <= t_stat4[str(confidence_percentage)+'%'] and t_stat1 <= round(1/confidence_percentage,1): #
        return ("YES",[l[i][0] for i in range(len(l_row_per))],t_stat0, t_stat1)
    else:
        return ("NO",[l[i][0] for i in range(len(l_row_per))],t_stat0,t_stat1)
        
    
