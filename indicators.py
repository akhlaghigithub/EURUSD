# This part is related to import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/1h_EURUSD_to_2005.csv')
moving_15 = []
moving_30 = []
moving_60 = []
rsi_14 = []
momentum_14 = []
for i in range(len(table_ds_1h)):
    # Moving Average 15
    if i > 15:
        mov15 = table_ds_1h.loc[i - 15:i, 'BC'].mean()
    else:
        mov15 = 0
    # Moving Average 30
    if i > 30:
        mov30 = table_ds_1h.loc[i - 30:i, 'BC'].mean()
    else:
        mov30 = 0
    # Moving Average 60
    if i > 60:
        mov60 = table_ds_1h.loc[i - 60:i, 'BC'].mean()
    else:
        mov60 = 0
    # RSI 14 And Momentum 14
    if i > 14:
        # Momentum
        close_1 = table_ds_1h['BC'][i-1]
        close_14 = table_ds_1h['BC'][i-14]
        mom_14 = (close_1 / close_14) * 100
        # RSI
        sum_profit = 0
        sum_loss = 0
        for j in range(i - 14, i):
            bch = table_ds_1h['BCh'][j]
            price_close = table_ds_1h['BC'][j]
            if bch > 0:
                sum_profit = sum_profit + price_close
            else:
                sum_loss = sum_loss + price_close
        average_sum_profit = sum_profit / 14
        average_loss_profit = sum_loss / 14
        if average_loss_profit == 0:
            rsi_amount = 0
        else:
            rsi_amount = 100 - (100 / (1 + (average_sum_profit/average_loss_profit)))
    else:
        rsi_amount = 0
        mom_14 = 0
    moving_15.append(mov15)
    moving_30.append(mov30)
    moving_60.append(mov60)
    rsi_14.append(rsi_amount)
    momentum_14.append(mom_14)
table_ds_1h['moving 15'] = moving_15
table_ds_1h['moving 30'] = moving_30
table_ds_1h['moving 60'] = moving_60
table_ds_1h['RSI 14'] = rsi_14
table_ds_1h['Momentum 14'] = momentum_14

# create a csv file and add rows (new dataset)
new_file_path = '1h_EURUSD_to_2005_with_indicator.csv'
table_ds_1h.to_csv(new_file_path, index=False)