# This part is related to import libraries
import numpy as np
import pandas as pd

# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/eurusd_hour.csv')

for i in range(len(table_ds_1h['Date'])):

    h_now = int(table_ds_1h['Time'][i].split(':')[0])
    h_next = int(table_ds_1h['Time'][i + 1].split(':')[0])

    year = int(table_ds_1h['Date'][i].split('/')[2])
    d_now = table_ds_1h['Date'][i]
    d_next = table_ds_1h['Date'][i+1]
    if year > 2000:
        break
    elif year < 2000:
        pass
    elif year == 2000:
        if len(table_ds_1h) - i > 4:
            from_mean = i - 5
            to_mean = i + 5
        else:
            from_mean = i - 5
            to_mean = len(table_ds_1h)

        if d_now == d_next:
            if h_now != 23:
                if h_next - h_now > 1:
                    average_BO = table_ds_1h.loc[from_mean:to_mean, 'BO'].mean()
                    average_BH = table_ds_1h.loc[from_mean:to_mean, 'BH'].mean()
                    average_BL = table_ds_1h.loc[from_mean:to_mean, 'BL'].mean()
                    average_BC = table_ds_1h.loc[from_mean:to_mean, 'BC'].mean()
                    average_BCh = average_BO - average_BC
                    for j in range(h_now + 1, h_next):
                        now_time = str(j) + ':00'
                        new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                        index_to_insert = i
                        table_ds_1h = pd.concat([table_ds_1h.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1h.iloc[index_to_insert:]]).reset_index(drop=True)

print(table_ds_1h.shape)
new_file_path = '1h_EURUSD_to_2005.csv'  # Replace with the desired path for the new CSV file
table_ds_1h.to_csv(new_file_path, index=False)


