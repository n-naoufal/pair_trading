
def convert_time_index(red_per, period_adf, red_per_d, red_per_h, red_per_m, nbr_hours_day, freq):
    red_per_d += max(period_adf)
    if (red_per==0): #seconds level
        ind_red = ((red_per_d * nbr_hours_day * 60 * 60) + (red_per_h * 60 * 60) + (red_per_m * 60))/ freq
    elif (red_per==1): #minutes level
        ind_red = ((red_per_d * nbr_hours_day * 60) + (red_per_h * 60) + red_per_m)/ freq 
    elif (red_per==2): #hours level
        ind_red = ((red_per_d * nbr_hours_day) + red_per_h + int(red_per_m/60))/ freq
    ind_red = int(ind_red) # an index must be integer
    return ind_red