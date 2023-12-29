# This part is related to import libraries
import numpy as np
import pandas as pd

# This part is related to read dataset
table_ds_1m = pd.read_csv('dataset/eurusd_minute.csv')
print(table_ds_1m.shape)

table_ds_1m.drop('AO', axis=1, inplace=True)
table_ds_1m.drop('AH', axis=1, inplace=True)
table_ds_1m.drop('AL', axis=1, inplace=True)
table_ds_1m.drop('AC', axis=1, inplace=True)
table_ds_1m.drop('ACh', axis=1, inplace=True)
print(table_ds_1m.shape)

for i in range(len(table_ds_1m['Date'])):
    m_now = int(table_ds_1m['Time'][i].split(':')[1])
    m_next = int(table_ds_1m['Time'][i + 1].split(':')[1])

    h_now = int(table_ds_1m['Time'][i].split(':')[0])
    h_next = int(table_ds_1m['Time'][i + 1].split(':')[0])

    year = int(table_ds_1m['Date'][i].split('-')[0])
    d_now = table_ds_1m['Date'][i]
    d_next = table_ds_1m['Date'][i+1]
    if year > 2015:
        break
    elif year < 2015:
        pass
    elif year == 2015:
        if len(table_ds_1m) - i > 4:
            from_mean = i - 5
            to_mean = i + 5
        else:
            from_mean = i - 5
            to_mean = len(table_ds_1m)


        if d_now == d_next:
            if h_now != 23 and m_now != 59:
                if m_now == 59:
                    if m_next > 0:
                        average_BO = table_ds_1m.loc[from_mean:to_mean, 'BO'].mean()
                        average_BH = table_ds_1m.loc[from_mean:to_mean, 'BH'].mean()
                        average_BL = table_ds_1m.loc[from_mean:to_mean, 'BL'].mean()
                        average_BC = table_ds_1m.loc[from_mean:to_mean, 'BC'].mean()
                        average_BCh = average_BO - average_BC
                        for j in range(m_next):
                            now_time = str(h_next) + ':' + str(j)
                            new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                            index_to_insert = i
                            table_ds_1m = pd.concat([table_ds_1m.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1m.iloc[index_to_insert:]]).reset_index(drop=True)
                else:
                    if h_next == h_now:
                        if m_next - m_now > 1:
                            average_BO = table_ds_1m.loc[from_mean:to_mean, 'BO'].mean()
                            average_BH = table_ds_1m.loc[from_mean:to_mean, 'BH'].mean()
                            average_BL = table_ds_1m.loc[from_mean:to_mean, 'BL'].mean()
                            average_BC = table_ds_1m.loc[from_mean:to_mean, 'BC'].mean()
                            average_BCh = average_BO - average_BC
                            for k in range(m_now + 1, m_next):
                                now_time = str(h_next) + ':' + str(k)
                                new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                                index_to_insert = i
                                table_ds_1m = pd.concat([table_ds_1m.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1m.iloc[index_to_insert:]]).reset_index(drop=True)
                    else:
                        average_BO = table_ds_1m.loc[from_mean:to_mean, 'BO'].mean()
                        average_BH = table_ds_1m.loc[from_mean:to_mean, 'BH'].mean()
                        average_BL = table_ds_1m.loc[from_mean:to_mean, 'BL'].mean()
                        average_BC = table_ds_1m.loc[from_mean:to_mean, 'BC'].mean()
                        average_BCh = average_BO - average_BC
                        for n in range(m_now + 1, 60):
                            now_time = str(h_now) + ':' + str(n)
                            new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                            index_to_insert = i
                            table_ds_1m = pd.concat([table_ds_1m.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1m.iloc[index_to_insert:]]).reset_index(drop=True)
                        if h_next - h_now > 1:
                            for c in range(h_now + 1, h_now):
                                for z in range(0, 60):
                                    now_time = str(c) + ':' + str(z)
                                    new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                                    index_to_insert = i
                                    table_ds_1m = pd.concat([table_ds_1m.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1m.iloc[index_to_insert:]]).reset_index(drop=True)
                        for m in range(0, m_next):
                            now_time = str(h_next) + ':' + str(m)
                            new_row_data = {'Date': d_now, 'Time': now_time, 'BO': average_BO, 'BH': average_BH, 'BL': average_BL, 'BC': average_BC, 'BCh': average_BCh}
                            index_to_insert = i
                            table_ds_1m = pd.concat([table_ds_1m.iloc[:index_to_insert], pd.DataFrame([new_row_data]), table_ds_1m.iloc[index_to_insert:]]).reset_index(drop=True)

print(table_ds_1m.shape)
new_file_path = '1m_EURUSD_to_2005.csv'  # Replace with the desired path for the new CSV file
table_ds_1m.to_csv(new_file_path, index=False)


