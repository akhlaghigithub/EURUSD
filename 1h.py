# This part is related to import libraries
import numpy as np
import pandas as pd

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
new_file_path = '1h_EURUSD_to_2005.csv'
table_ds_1h.to_csv(new_file_path, index=False)


