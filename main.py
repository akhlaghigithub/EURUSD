# This part is related to import libraries
import numpy as np
import pandas as pd
import csv

# This part is related to read dataset
table_ds_1h = pd.read_csv('dataset/eurusd_hour.csv')
table_ds_1m = pd.read_csv('dataset/eurusd_minute.csv')
table_ds_1m.drop('AO', axis=1, inplace=True)
table_ds_1m.drop('AH', axis=1, inplace=True)
table_ds_1m.drop('AL', axis=1, inplace=True)
table_ds_1m.drop('AC', axis=1, inplace=True)
table_ds_1m.drop('ACh', axis=1, inplace=True)

print(table_ds_1m.tail(1392))
x = 24
y = 60
for i in range(len(table_ds_1m.tail(1392))):
    yy = int(table_ds_1m['Time'][i].split(':')[1])
    yy2 = int(table_ds_1m['Time'][i + 1].split(':')[1])

    xx = int(table_ds_1m['Time'][i].split(':')[0])
    xx2 = int(table_ds_1m['Time'][i + 1].split(':')[0])

    dd = table_ds_1m['Date'][i]

    if yy == 59 :
        if yy2 > 1 :
            for j in range(yy2):
                print(dd + ' ' + str(xx2) + ':' + str(j))
    else :
        if yy2 - yy > 1 :
            for k in range(yy2 - yy):
                print(dd + ' ' + str(xx2) + ':' + str(k))




