# This part is related to import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicators as ind
# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/EurUsd_with_indicators.csv')

list_status_moving = []
list_diff_15_30 = []
list_diff_30_60 = []
list_touch_15_from_top = []
list_touch_15_from_below = []
for i in range(len(table_ds_1h['Date'])):
    if i < 60:
        status_moving = 'not'
        diff_15_30 = 'not'
        diff_30_60 = 'not'
        touch_15_from_top = 'not'
        touch_15_from_below = 'not'
    else:
        if (table_ds_1h['moving 15'][i] > table_ds_1h['moving 30'][i]) and (table_ds_1h['moving 30'][i] > table_ds_1h['moving 60'][i]):
            status_moving = 'buy'
            diff_15_30 = table_ds_1h['moving 15'][i] - table_ds_1h['moving 30'][i]
            diff_30_60 = table_ds_1h['moving 30'][i] - table_ds_1h['moving 60'][i]
            if (table_ds_1h['BO'][i] > table_ds_1h['moving 15'][i]) and (table_ds_1h['moving 15'][i] > table_ds_1h['BL'][i]):
                touch_15_from_top = 'yes'
                touch_15_from_below = 'not'
            elif (table_ds_1h['BO'][i] < table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][i] > table_ds_1h['moving 15'][i]):
                touch_15_from_top = 'not'
                touch_15_from_below = 'yes'
            else:
                touch_15_from_top = 'not'
                touch_15_from_below = 'not'
        elif (table_ds_1h['moving 15'][i] < table_ds_1h['moving 30'][i]) and (table_ds_1h['moving 30'][i] < table_ds_1h['moving 60'][i]):
            status_moving = 'sell'
            diff_15_30 = table_ds_1h['moving 30'][i] - table_ds_1h['moving 15'][i]
            diff_30_60 = table_ds_1h['moving 60'][i] - table_ds_1h['moving 30'][i]
            if (table_ds_1h['BO'][i] > table_ds_1h['moving 15'][i]) and (table_ds_1h['moving 15'][i] > table_ds_1h['BC'][i]):
                touch_15_from_top = 'yes'
                touch_15_from_below = 'not'
            elif (table_ds_1h['BO'][i] < table_ds_1h['moving 15'][i]) and (table_ds_1h['BH'][i] > table_ds_1h['moving 15'][i]):
                touch_15_from_top = 'not'
                touch_15_from_below = 'yes'
            else:
                touch_15_from_top = 'not'
                touch_15_from_below = 'not'
        else:
            status_moving = 'not'
            diff_15_30 = 'not'
            diff_30_60 = 'not'
            touch_15_from_top = 'not'
            touch_15_from_below = 'not'
    list_status_moving.append(status_moving)
    list_diff_15_30.append(diff_15_30)
    list_diff_30_60.append(diff_30_60)
    list_touch_15_from_top.append(touch_15_from_top)
    list_touch_15_from_below.append(touch_15_from_below)
table_ds_1h['status moving'] = list_status_moving
table_ds_1h['diff 15 and 30'] = list_diff_15_30
table_ds_1h['diff 30 and 60'] = list_diff_30_60
table_ds_1h['touch 15 from top'] = list_touch_15_from_top
table_ds_1h['touch 15 from below'] = list_touch_15_from_below
print(table_ds_1h)
count_buy_status = 0
count_sell_status = 0
for i in range(len(table_ds_1h['Date'])):
    if table_ds_1h['status moving'][i] == 'buy':
        count_buy_status += 1
    elif table_ds_1h['status moving'][i] == 'sell':
        count_sell_status += 1
print(f'buy = {count_buy_status}')
print(f'sell = {count_sell_status}')