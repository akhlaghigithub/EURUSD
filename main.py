# This part is related to import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicators as ind
# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/eurusd_hour.csv')

table_ds_1h['moving 15'] = ind.moving_func(15, table_ds_1h)
table_ds_1h['moving 30'] = ind.moving_func(30, table_ds_1h)
table_ds_1h['moving 60'] = ind.moving_func(60, table_ds_1h)
table_ds_1h['RSI 14'] = ind.rsi_func(14, table_ds_1h)
table_ds_1h['Momentum 14'] = ind.momentum_func(14, table_ds_1h)

# create a csv file and add rows (new dataset)
new_file_path = 'test.csv'
table_ds_1h.to_csv(new_file_path, index=False)

rows_here = range(len(table_ds_1h)-1000,len(table_ds_1h))
plt.figure(figsize=(60,2))
plt.plot(rows_here, table_ds_1h['Momentum 14'][len(table_ds_1h)-1000:len(table_ds_1h)])
plt.show()
