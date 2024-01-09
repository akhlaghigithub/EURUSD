# This part is related to import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicators as ind


# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/eurusd_hour.csv')

# This is a loop to check the rows which, if there is no candle data, will be constructed by averaging the 5 candles before and after it.
for i in range(len(table_ds_1h['Date'])):
    # Time of current and next candle
    h_now = int(table_ds_1h['Time'][i].split(':')[0])
    h_next = int(table_ds_1h['Time'][i + 1].split(':')[0])
    # Day of current and next candle
    d_now = table_ds_1h['Date'][i]
    d_next = table_ds_1h['Date'][i+1]
    # check remain candles in loop and if there are less than 5 candles have to change numbers of candles which are participated in mean
    if len(table_ds_1h) - i > 4:
        from_mean = i - 5
        to_mean = i + 5
    else:
        from_mean = i - 5
        to_mean = len(table_ds_1h)
    # check if current candle and next are in a same day
    if d_now == d_next:
        # check if hour is less than 23
        if h_now != 23:
            # check if hour of current and next candles have difference more than 1
            if h_next - h_now > 1:
                # calculate mean of each column
                average_BO = table_ds_1h.loc[from_mean:to_mean, 'BO'].mean()
                average_BH = table_ds_1h.loc[from_mean:to_mean, 'BH'].mean()
                average_BL = table_ds_1h.loc[from_mean:to_mean, 'BL'].mean()
                average_BC = table_ds_1h.loc[from_mean:to_mean, 'BC'].mean()
                average_BCh = average_BO - average_BC
                # a loop for create rows with mean information
                for j in range(h_now + 1, h_next):
                    now_time = str(j) + ':00'
                    new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                    index_to_insert = i
                    table_ds_1h = pd.concat([table_ds_1h.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1h.iloc[index_to_insert:]]).reset_index(drop=True)
# create a csv file and add rows (new dataset)
new_file_path = 'dataset/1h_EURUSD_to_2005.csv'
table_ds_1h.to_csv(new_file_path, index=False)


# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/1h_EURUSD_to_2005.csv')

# create columns of Moving and RSI and Momentum with importing indicators
table_ds_1h['moving 15'] = ind.moving_func(15, table_ds_1h)
table_ds_1h['moving 30'] = ind.moving_func(30, table_ds_1h)
table_ds_1h['moving 60'] = ind.moving_func(60, table_ds_1h)
table_ds_1h['RSI 14'] = ind.rsi_func(14, table_ds_1h)
table_ds_1h['Momentum 14'] = ind.momentum_func(14, table_ds_1h)

# create a csv file and add rows (new dataset)
new_file_path = 'dataset/EurUsd_with_indicators.csv'
table_ds_1h.to_csv(new_file_path, index=False)

# use new dataset
table_ds_1h_new = pd.read_csv('dataset/EurUsd_with_indicators.csv')

"""
    create columns of:
    1- status Moving = checking status moving for each candle so that if moving 15 is higher than other and 60 is lower than other for BUY position. Also same situation for Sell position.
    2- difference between moving 15, 30 , 60 = this feature will be used if there is a relationship between difference and success rate.
    3- checking how many times and how candles touch moving 15 in a appropriate position
"""
list_status_moving = []
list_diff_15_30 = []
list_diff_30_60 = []
list_touch_15_from_top = []
list_touch_15_from_below = []
for i in range(len(table_ds_1h_new['Date'])):
    # why 60? because after 60 candles we can calculate moving average 60
    if i < 60:
        status_moving = 'not'
        diff_15_30 = 'not'
        diff_30_60 = 'not'
        touch_15_from_top = 'not'
        touch_15_from_below = 'not'
    else:
        if (table_ds_1h_new['moving 15'][i] > table_ds_1h_new['moving 30'][i]) and (table_ds_1h_new['moving 30'][i] > table_ds_1h_new['moving 60'][i]):
            status_moving = 'buy'
            diff_15_30 = table_ds_1h_new['moving 15'][i] - table_ds_1h_new['moving 30'][i]
            diff_30_60 = table_ds_1h_new['moving 30'][i] - table_ds_1h_new['moving 60'][i]
            if (table_ds_1h_new['BO'][i] > table_ds_1h_new['moving 15'][i]) and (table_ds_1h_new['moving 15'][i] > table_ds_1h_new['BL'][i]):
                touch_15_from_top = 'yes'
                touch_15_from_below = 'not'
            elif (table_ds_1h_new['BO'][i] < table_ds_1h_new['moving 15'][i]) and (table_ds_1h_new['BC'][i] > table_ds_1h_new['moving 15'][i]):
                touch_15_from_top = 'not'
                touch_15_from_below = 'yes'
            else:
                touch_15_from_top = 'not'
                touch_15_from_below = 'not'
        elif (table_ds_1h_new['moving 15'][i] < table_ds_1h_new['moving 30'][i]) and (table_ds_1h_new['moving 30'][i] < table_ds_1h_new['moving 60'][i]):
            status_moving = 'sell'
            diff_15_30 = table_ds_1h_new['moving 30'][i] - table_ds_1h_new['moving 15'][i]
            diff_30_60 = table_ds_1h_new['moving 60'][i] - table_ds_1h_new['moving 30'][i]
            if (table_ds_1h_new['BO'][i] > table_ds_1h_new['moving 15'][i]) and (table_ds_1h_new['moving 15'][i] > table_ds_1h_new['BC'][i]):
                touch_15_from_top = 'yes'
                touch_15_from_below = 'not'
            elif (table_ds_1h_new['BO'][i] < table_ds_1h_new['moving 15'][i]) and (table_ds_1h_new['BH'][i] > table_ds_1h_new['moving 15'][i]):
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
table_ds_1h_new['status moving'] = list_status_moving
table_ds_1h_new['diff 15 and 30'] = list_diff_15_30
table_ds_1h_new['diff 30 and 60'] = list_diff_30_60
table_ds_1h_new['touch 15 from top'] = list_touch_15_from_top
table_ds_1h_new['touch 15 from below'] = list_touch_15_from_below

# create a csv file and add rows (new dataset) for touch moving
new_file_path = 'dataset/EurUsd_for_touch_moving.csv'
table_ds_1h_new.to_csv(new_file_path, index=False)


# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/EurUsd_for_touch_moving.csv')

list_type_trade = []
list_result_trade = []
count_buy_status = 0
count_buy_below_status = 0
count_sell_status = 0
count_sell_top_status = 0
status_buy = 0
status_buy_below = 0
status_sell = 0
status_sell_top = 0
list_buy_trade = []
list_buy_below_trade = []
list_sell_trade = []
list_sell_top_trade = []
list_type_buy_gain = []
list_type_buy_below_gain = []
list_type_sell_gain = []
list_type_sell_top_gain = []
for i in range(len(table_ds_1h['Date'])):
    if i < 60:
        type_trade = 'no trade'
        list_type_trade.append(type_trade)
        result_trade = 'no trade'
        list_result_trade.append(result_trade)
    else:
        # Strategy BUY TOP = Moving 15 > 30 > 60 and if price is touching Moving 15 from top then trade BUY position
        if (table_ds_1h['status moving'][i] == 'buy') and (table_ds_1h['touch 15 from top'][i] == 'yes'):
            type_trade = 'Buy from Top'
            list_type_trade.append(type_trade)
            count_buy_status += 1
            # STOP LOSS: Checking the candles before the moment of trading and choosing a candle at the lowest closing price compared to the next and previous 5 candles
            for j in range(i - 5, 0, -1):
                if (table_ds_1h['BC'][j] < table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 1]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 2]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 3]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 4]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 5]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 1]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 2]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 3]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 4]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 5]):
                    stop_loss_for_buy = table_ds_1h['BC'][j]
                    # TAKE PROFIT: adding a custom amount (difference between STOP LOSS and MOVING 15) to Moving 15
                    take_profit_for_buy = table_ds_1h['moving 15'][i] + (table_ds_1h['moving 15'][i] - stop_loss_for_buy)
                    break
            # TP or SL : Checking the candles after the moment of the trade, so that it first touches the TP or the SL
            for k in range(i, len(table_ds_1h['Date'])):
                if table_ds_1h['BH'][k] > take_profit_for_buy:
                    status_buy += 1
                    list_buy_trade.append('profit')
                    result_trade = 'profit'
                    break
                elif table_ds_1h['BL'][k] < stop_loss_for_buy:
                    status_buy -= 1
                    list_buy_trade.append('loss')
                    result_trade = 'loss'
                    break
                list_type_buy_gain.append(status_buy)
            list_result_trade.append(result_trade)
        # Strategy BUY BELOW = Moving 15 > 30 > 60 and if price is touching Moving 15 from below then trade BUY position
        elif (table_ds_1h['status moving'][i] == 'buy') and (table_ds_1h['touch 15 from below'][i] == 'yes'):
            type_trade = 'Buy from Below'
            list_type_trade.append(type_trade)
            count_buy_below_status += 1
            # STOP LOSS: Checking the candles before the moment of trading and choosing a candle at the lowest closing price compared to the next and previous 5 candles
            for j in range(i - 5, 0, -1):
                if (table_ds_1h['BC'][j] < table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 1]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 2]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 3]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 4]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j + 5]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 1]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 2]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 3]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 4]) and (table_ds_1h['BC'][j] < table_ds_1h['BC'][j - 5]):
                    stop_loss_for_buy_below = table_ds_1h['BC'][j]
                    # TAKE PROFIT: adding a custom amount (difference between STOP LOSS and close) to close
                    take_profit_for_buy_below = table_ds_1h['BC'][i] + (table_ds_1h['BC'][i] - stop_loss_for_buy_below)
                    break
            # TP or SL : Checking the candles after the moment of the trade, so that it first touches the TP or the SL
            for k in range(i, len(table_ds_1h['Date'])):
                if table_ds_1h['BH'][k] > take_profit_for_buy_below:
                    status_buy_below += 1
                    list_buy_below_trade.append('profit')
                    result_trade = 'profit'
                    break
                elif table_ds_1h['BL'][k] < stop_loss_for_buy_below:
                    status_buy_below -= 1
                    list_buy_below_trade.append('loss')
                    result_trade = 'loss'
                    break
                list_type_buy_below_gain.append(status_buy_below)
            list_result_trade.append(result_trade)
        # Strategy SELL BELOW = Moving 15 < 30 < 60 and if price is touching Moving 15 from below then trade SELL position
        elif (table_ds_1h['status moving'][i] == 'sell') and (table_ds_1h['touch 15 from below'][i] == 'yes'):
            type_trade = 'Sell from Below'
            list_type_trade.append(type_trade)
            count_sell_status += 1
            # STOP LOSS: Checking the candles before the moment of trading and choosing a candle at the highest closing price compared to the next and previous 5 candles
            for j in range(i - 5, 0, -1):
                if (table_ds_1h['BC'][j] > table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 1]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 2]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 3]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 4]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 5]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 1]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 2]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 3]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 4]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 5]):
                    stop_loss_for_sell = table_ds_1h['BC'][j]
                    # TAKE PROFIT: reducing a custom amount (difference between STOP LOSS and MOVING 15) from Moving 15
                    take_profit_for_sell = table_ds_1h['moving 15'][i] - (stop_loss_for_sell - table_ds_1h['moving 15'][i])
                    break
            # TP or SL : Checking the candles after the moment of the trade, so that it first touches the TP or the SL
            for k in range(i, len(table_ds_1h['Date'])):
                if table_ds_1h['BH'][k] > stop_loss_for_sell:
                    status_sell -= 1
                    list_sell_trade.append('loss')
                    result_trade = 'loss'
                    break
                elif table_ds_1h['BL'][k] < take_profit_for_sell:
                    status_sell += 1
                    list_sell_trade.append('profit')
                    result_trade = 'profit'
                    break
                list_type_sell_gain.append(status_sell)
            list_result_trade.append(result_trade)
        # Strategy SELL Top = Moving 15 < 30 < 60 and if price is touching Moving 15 from top then trade SELL position
        elif (table_ds_1h['status moving'][i] == 'sell') and (table_ds_1h['touch 15 from top'][i] == 'yes'):
            type_trade = 'Sell from Top'
            list_type_trade.append(type_trade)
            count_sell_top_status += 1
            # STOP LOSS: Checking the candles before the moment of trading and choosing a candle at the highest closing price compared to the next and previous 5 candles
            for j in range(i - 5, 0, -1):
                if (table_ds_1h['BC'][j] > table_ds_1h['moving 15'][i]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 1]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 2]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 3]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 4]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j + 5]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 1]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 2]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 3]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 4]) and (table_ds_1h['BC'][j] > table_ds_1h['BC'][j - 5]):
                    stop_loss_for_sell_top = table_ds_1h['BC'][j]
                    # TAKE PROFIT: reducing a custom amount (difference between STOP LOSS and close) from close
                    take_profit_for_sell_top = table_ds_1h['BC'][i] - (stop_loss_for_sell_top - table_ds_1h['BC'][i])
                    break
            # TP or SL : Checking the candles after the moment of the trade, so that it first touches the TP or the SL
            for k in range(i, len(table_ds_1h['Date'])):
                if table_ds_1h['BH'][k] > stop_loss_for_sell_top:
                    status_sell_top -= 1
                    list_sell_top_trade.append('loss')
                    result_trade = 'loss'
                    break
                elif table_ds_1h['BL'][k] < take_profit_for_sell_top:
                    status_sell_top += 1
                    list_sell_top_trade.append('profit')
                    result_trade = 'profit'
                    break
                list_type_sell_top_gain.append(status_sell_top)
            list_result_trade.append(result_trade)
        else:
            type_trade = 'no trade'
            list_type_trade.append(type_trade)
            result_trade = 'no trade'
            list_result_trade.append(result_trade)


table_ds_1h['type trade'] = list_type_trade
table_ds_1h['result trade'] = list_result_trade
# create a csv file and add rows (new dataset) for touch moving
new_file_path = 'dataset/EurUsd_with_result.csv'
table_ds_1h.to_csv(new_file_path, index=False)

print(f'buy = {count_buy_status}')
print(f'sell = {count_sell_status}')
print(f'success buy = {status_buy}')
print(f'success sell = {status_sell}')
print(f'max gain buy = {max(list_type_buy_gain)} and min = {min(list_type_buy_gain)}')
print(f'max gain sell = {max(list_type_sell_gain)} and min = {min(list_type_sell_gain)}')
print(f'buy below = {count_buy_below_status}')
print(f'sell top = {count_sell_top_status}')
print(f'success buy below = {status_buy_below}')
print(f'success sell top = {status_sell_top}')
print(f'max gain buy below = {max(list_type_buy_below_gain)} and min = {min(list_type_buy_below_gain)}')
print(f'max gain sell top = {max(list_type_sell_top_gain)} and min = {min(list_type_sell_top_gain)}')

list_buy_continue_profit = []
list_buy_continue_loss = []
profit_continue_b = 0
loss_continue_b = 0
for i in range(len(list_buy_trade)):
    if i == 0:
        if list_buy_trade[i] == 'profit':
            profit_continue_b += 1
        else:
            loss_continue_b += 1
    else:
        if list_buy_trade[i] == 'profit':
            profit_continue_b += 1
            if list_buy_trade[i-1] == 'loss':
                list_buy_continue_loss.append(loss_continue_b)
                loss_continue_b = 0
        else:
            loss_continue_b += 1
            if list_buy_trade[i-1] == 'profit':
                list_buy_continue_profit.append(profit_continue_b)
                profit_continue_b = 0


list_buy_below_continue_profit = []
list_buy_below_continue_loss = []
profit_continue_b_below = 0
loss_continue_b_below = 0
for i in range(len(list_buy_below_trade)):
    if i == 0:
        if list_buy_below_trade[i] == 'profit':
            profit_continue_b_below += 1
        else:
            loss_continue_b_below += 1
    else:
        if list_buy_below_trade[i] == 'profit':
            profit_continue_b_below += 1
            if list_buy_below_trade[i-1] == 'loss':
                list_buy_below_continue_loss.append(loss_continue_b_below)
                loss_continue_b_below = 0
        else:
            loss_continue_b_below += 1
            if list_buy_below_trade[i-1] == 'profit':
                list_buy_below_continue_profit.append(profit_continue_b_below)
                profit_continue_b_below = 0

list_sell_continue_profit = []
list_sell_continue_loss = []
profit_continue_s = 0
loss_continue_s = 0
for i in range(len(list_sell_trade)):
    if i == 0:
        if list_sell_trade[i] == 'profit':
            profit_continue_s += 1
        else:
            loss_continue_s += 1
    else:
        if list_sell_trade[i] == 'profit':
            profit_continue_s += 1
            if list_sell_trade[i-1] == 'loss':
                list_sell_continue_loss.append(loss_continue_s)
                loss_continue_s = 0
        else:
            loss_continue_s += 1
            if list_sell_trade[i-1] == 'profit':
                list_sell_continue_profit.append(profit_continue_s)
                profit_continue_s = 0

list_sell_top_continue_profit = []
list_sell_top_continue_loss = []
profit_continue_s_top = 0
loss_continue_s_top = 0
for i in range(len(list_sell_top_trade)):
    if i == 0:
        if list_sell_top_trade[i] == 'profit':
            profit_continue_s_top += 1
        else:
            loss_continue_s_top += 1
    else:
        if list_sell_top_trade[i] == 'profit':
            profit_continue_s_top += 1
            if list_sell_top_trade[i-1] == 'loss':
                list_sell_top_continue_loss.append(loss_continue_s_top)
                loss_continue_s_top = 0
        else:
            loss_continue_s_top += 1
            if list_sell_top_trade[i-1] == 'profit':
                list_sell_top_continue_profit.append(profit_continue_s_top)
                profit_continue_s_top = 0

print(f'max continue profit buy : {max(list_buy_continue_profit)} and loss : {max(list_buy_continue_loss)}')
print(f'max continue profit sell : {max(list_sell_continue_profit)} and loss : {max(list_sell_continue_loss)}')
print(f'max continue profit buy below : {max(list_buy_below_continue_profit)} and loss : {max(list_buy_below_continue_loss)}')
print(f'max continue profit sell top : {max(list_sell_top_continue_profit)} and loss : {max(list_sell_top_continue_loss)}')

