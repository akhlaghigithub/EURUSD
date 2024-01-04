# This part is related to import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicators as ind
# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/EurUsd_for_touch_moving.csv')

count_buy_status = 0
count_sell_status = 0
status_buy = 0
status_sell = 0
list_buy_trade = []
list_sell_trade = []
list_type_buy_gain = []
list_type_sell_gain = []
for i in range(60, len(table_ds_1h['Date'])):
    if table_ds_1h['status moving'][i] == 'buy':
        count_buy_status += 1
        for j in range(i-5, 0, -1):
            if (table_ds_1h['BC'][j] < table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 1]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 2]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 3]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 4]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 5]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 1]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 2]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 3]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 4]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 5]):
                stop_loss_for_buy = table_ds_1h['BC'][j]
                take_profit_for_buy = table_ds_1h['moving 15'][i] + (table_ds_1h['moving 15'][i] - stop_loss_for_buy)
                break
        for k in range(i, len(table_ds_1h['Date'])):
            if table_ds_1h['BH'][k] > take_profit_for_buy:
                status_buy += 1
                list_buy_trade.append(1)
                break
            elif table_ds_1h['BL'][k] < stop_loss_for_buy:
                status_buy -= 1
                list_buy_trade.append(-1)
                break
            list_type_buy_gain.append(status_buy)
    elif table_ds_1h['status moving'][i] == 'sell':
        count_sell_status += 1
        for j in range(i-5, 0, -1):
            if (table_ds_1h['BC'][j] > table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 1]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 2]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 3]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 4]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 5]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 1]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 2]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 3]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 4]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 5]):
                stop_loss_for_sell = table_ds_1h['BC'][j]
                take_profit_for_sell = table_ds_1h['moving 15'][i] - (stop_loss_for_sell - table_ds_1h['moving 15'][i])
                break
        for k in range(i, len(table_ds_1h['Date'])):
            if table_ds_1h['BH'][k] > stop_loss_for_sell:
                status_sell -= 1
                list_sell_trade.append(-1)
                break
            elif table_ds_1h['BL'][k] < take_profit_for_sell:
                status_sell += 1
                list_sell_trade.append(1)
                break
            list_type_sell_gain.append(status_sell)
print(f'buy = {count_buy_status}')
print(f'sell = {count_sell_status}')
print(f'success buy = {status_buy}')
print(f'success sell = {status_sell}')
print(f'max gain buy = {max(list_type_buy_gain)} and min = {min(list_type_buy_gain)}')
print(f'max gain sell = {max(list_type_sell_gain)} and min = {min(list_type_sell_gain)}')