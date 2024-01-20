import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# base Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Introducing The Model', 'Raw Dataset', 'Cleaning and Expanding Dataset', 'Indicators', 'Analyse Method', 'Suggestions'])

# head image
tab1.image('forex.jpg')
# Tab 1: Introducing The Model
tab1.title('EURUSD Trading Project')
tab1.write('The dataset used is related to the historical data of the EurUsd currency pair from 2005 to 2020. This dataset has columns of date, time, opening price, closing price, high price, low price and change percentage.')
tab1.write('The trading model in question is based on the position of the moving average of 15, 30 and 60. The important condition for entering into transactions is to touch the price with a moving average of 15. In this model, 4 modes are considered for entering transactions, which are as follows:')
tab1.subheader('- Buy - Touch from above:')
tab1.write('In this case, the moving average of 15 should be above 30 and 30 above 60. Also, the price should touch it from the range above the moving average of 15.')
tab1.subheader('- Buy - Touch from below:')
tab1.write('In this case, the moving average of 15 should be above 30 and 30 above 60. Also, the price should touch it from the range below the moving average of 15.')
tab1.image('buy_condition.png')
tab1.subheader('- Sell - Touch from above:')
tab1.write('In this case, the moving average of 15 should be below 30 and 30 below 60. Also, the price should touch it from the range above the moving average of 15.')
tab1.subheader('- Sell - Touch from below:')
tab1.write('In this case, the moving average of 15 should be below 30 and 30 below 60. Also, the price should touch it from the range below the moving average of 15.')
tab1.image('sell_condition.png')

# Tab 2: Raw Dataset
tab2.title('Raw Dataset')
db_base = pd.read_csv('dataset/eurusd_hour.csv')
tab2.write(db_base)

# Tab 3: Data cleaning and expanding
tab3.title('Data cleaning and expanding')
tab3.write('The EURUSD dataset was available from 2005 to 2020 for a 1-hour time frame. This dataset did not have any incomplete data. But to check the trading model, it needed to be developed. For this purpose, the following items were added to the dataset:')
tab3.write('- RSI 14')
tab3.write('- Momentum 14')
tab3.write('- Moving average 15, 30 and 60')
tab3.write('In the next step, according to the model, it was necessary to identify the points of price collision with Moving average 15. These points were identified in two modes: touch from the top of the moving and touch from the bottom of the moving. In fact, these points are the starting points of transactions. Then the candles before these points were checked and the loss limit points were identified. Finally, the price gap between the loss limit and the entry point of the transaction was calculated and used to identify the profit limit.')
tab3.title('Expanded Dataset')
tab3.subheader('step 1 : clean dataset:')
tab3.write('This dataset did not have null contents. But on the other hand, the price data was missing for some hours during the day. For this reason, the dataset was completed using the average price of 10 candles (5 before and 5 after).')
# cleaning dataset button
if tab3.button('cleaning dataset'):
    tab3.write(pd.read_csv('dataset/1h_EURUSD_to_2005.csv'))
# expanding dataset button
tab3.subheader('step 2 : expanding dataset with Moving Averages and indicators:')
tab3.write('First, functions related to calculation of moving average, RSI and momentum were coded in the indicators.py file. Then, it was imported in the expand_db.py file and each indicator was added to the previous dataset.')
if tab3.button('dataset with indicators'):
    tab3.write(pd.read_csv('dataset/EurUsd_with_indicators.csv'))
# entry points dataset button
tab3.subheader('step 3 : Identification of entry points:')
tab3.write('According to the explanations given in introduction, the market entry points were identified and added to the dataset.')
if tab3.button('dataset with touching Moving Average 15'):
    tab3.write(pd.read_csv('dataset/EurUsd_for_touch_moving.csv'))
# result dataset button
tab3.subheader('step 4 : dataset with result:')
tab3.write('In the last step, by identifying the loss limit and profit limit points, the next candles were checked to determine whether each trade led to a profit or a loss. In this way, the dataset is ready for analysis.')
if tab3.button('dataset with result'):
    tab3.write(pd.read_csv('dataset/EurUsd_with_result.csv'))

# Tab 4: Indicators
tab4.title('Indicators:')
# SMA
tab4.subheader('1- Moving Average (SMA Close):')
tab4.write('SMA is calculated by adding up a set of closing prices over a specific period (e.g., 10 days) and then dividing the sum by the number of days in that period.')
tab4.image('Moving_func.png')
# RSI
tab4.subheader('2- RSI:')
tab4.write('The Relative Strength Index (RSI) is a popular momentum oscillator used in technical analysis to measure the speed and change of price movements. The RSI is typically used to identify overbought or oversold conditions in a market, which can help traders assess potential reversal points.')
tab4.image('RSI_func.png')
# Momentum
tab4.subheader('3- Momentum:')
tab4.write('momentum in forex refers to the strength and speed of price movements for a currency pair. It is like assessing how fast a car is moving in a certain direction. Traders use momentum to understand if a currency is gaining or losing strength, helping them make decisions about when to buy or sell.')
tab4.image('Momentum_func.png')


# dataset
dataset_1h = pd.read_csv('dataset/EurUsd_with_result.csv')

# custom form for checking dataset
col1, col2, col3 = tab5.columns([1, 1, 1])

with col1:
    start_year = int(st.number_input('Start Year:', min_value=2007, max_value=2020))
    end_year = int(st.number_input('End Year:', min_value=start_year, max_value=2020))

with col2:
    your_balance = int(st.number_input('Your Balance $ :', min_value=1000, max_value=10000))
    your_risk = int(st.number_input('Your Risk :', min_value=1, max_value=10))
    your_estimate = int(st.number_input('Preferred estimate % :', value=60, min_value=1, max_value=100))
    prefer_estimate = your_estimate / 100
with col3:
    your_request = st.radio('Pick one:', ['Distribution', 'Trade status', 'Classification'])

# convert dates inputs form to row record in dataset
start_date = 0
end_date = 0
for i in range(len(dataset_1h['Date'])):
    if str(dataset_1h['Date'][i][-4:]) == str(start_year):
        start_date = i
        break
if end_year == 2020:
    end_date = len(dataset_1h['Date'])
else:
    for j in range(start_date, len(dataset_1h['Date'])):
        if str(dataset_1h['Date'][j][-4:]) == str(end_year+1):
            end_date = j
            break

balance_total = your_balance
balance_buy_top = your_balance
balance_sell_top = your_balance
balance_buy_below = your_balance
balance_sell_below = your_balance
list_balance_total = []
list_balance_buy_top = []
list_balance_sell_top = []
list_balance_buy_below = []
list_balance_sell_below = []
list_time_total = []
list_time_buy_top = []
list_time_sell_top = []
list_time_buy_below = []
list_time_sell_below = []
risk_trade = your_risk / 100

list_rsi_buy_method1 = []
list_rsi_buy_method2 = []
list_rsi_sell_method1 = []
list_rsi_sell_method2 = []
list_momentum_buy_method1 = []
list_momentum_buy_method2 = []
list_momentum_sell_method1 = []
list_momentum_sell_method2 = []
list_diff15to30_buy_method1 = []
list_diff15to30_buy_method2 = []
list_diff15to30_sell_method1 = []
list_diff15to30_sell_method2 = []
list_diff30to60_buy_method1 = []
list_diff30to60_buy_method2 = []
list_diff30to60_sell_method1 = []
list_diff30to60_sell_method2 = []
list_result_buy_method1 = []
list_result_buy_method2 = []
list_result_sell_method1 = []
list_result_sell_method2 = []
list_type_trade = ['Buy From Top', 'Buy From Below', 'Sell From Top', 'Sell From Below']
list_type_trade_numeric = []
buy_top = 0
buy_below = 0
sell_top = 0
sell_below = 0

buy_top_p = 0
buy_top_l = 0
buy_below_p = 0
buy_below_l = 0
sell_top_p = 0
sell_top_l = 0
sell_below_p = 0
sell_below_l = 0

num_profit = 0
num_loss = 0

for i in range(start_date, end_date):
    if i == start_date:
        list_balance_total.append(balance_total)
        list_balance_buy_top.append(balance_buy_top)
        list_balance_sell_top.append(balance_sell_top)
        list_balance_buy_below.append(balance_buy_below)
        list_balance_sell_below.append(balance_sell_below)
        list_time_total.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
        list_time_buy_top.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
        list_time_sell_top.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
        list_time_buy_below.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
        list_time_sell_below.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
    else:
        if dataset_1h['result trade'][i] == 'profit':
            num_profit += 1
            list_balance_total.append((1 + risk_trade) * list_balance_total[len(list_balance_total) - 1])
            list_time_total.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
            if dataset_1h['type trade'][i] == 'Buy from Top':
                list_balance_buy_top.append((1 + risk_trade) * list_balance_buy_top[len(list_balance_buy_top) - 1])
                list_time_buy_top.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                buy_top += 1
                buy_top_p += 1

                list_rsi_buy_method1.append(dataset_1h['RSI 14'][i])
                list_momentum_buy_method1.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_buy_method1.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_buy_method1.append(dataset_1h['diff 30 and 60'][i])
                list_result_buy_method1.append(1)

            elif dataset_1h['type trade'][i] == 'Sell from Top':
                list_balance_sell_top.append((1 + risk_trade) * list_balance_sell_top[len(list_balance_sell_top) - 1])
                list_time_sell_top.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                sell_top += 1
                sell_top_p += 1

                list_rsi_sell_method2.append(dataset_1h['RSI 14'][i])
                list_momentum_sell_method2.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_sell_method2.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_sell_method2.append(dataset_1h['diff 30 and 60'][i])
                list_result_sell_method2.append(1)

            elif dataset_1h['type trade'][i] == 'Buy from Below':
                list_balance_buy_below.append((1 + risk_trade) * list_balance_buy_below[len(list_balance_buy_below) - 1])
                list_time_buy_below.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                buy_below += 1
                buy_below_p += 1

                list_rsi_buy_method2.append(dataset_1h['RSI 14'][i])
                list_momentum_buy_method2.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_buy_method2.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_buy_method2.append(dataset_1h['diff 30 and 60'][i])
                list_result_buy_method2.append(1)

            elif dataset_1h['type trade'][i] == 'Sell from Below':
                list_balance_sell_below.append((1 + risk_trade) * list_balance_sell_below[len(list_balance_sell_below) - 1])
                list_time_sell_below.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                sell_below += 1
                sell_below_p += 1

                list_rsi_sell_method1.append(dataset_1h['RSI 14'][i])
                list_momentum_sell_method1.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_sell_method1.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_sell_method1.append(dataset_1h['diff 30 and 60'][i])
                list_result_sell_method1.append(1)

        elif dataset_1h['result trade'][i] == 'loss':
            num_loss += 1
            list_balance_total.append((1 - risk_trade) * list_balance_total[len(list_balance_total) - 1])
            list_time_total.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
            if dataset_1h['type trade'][i] == 'Buy from Top':
                list_balance_buy_top.append((1 - risk_trade) * list_balance_buy_top[len(list_balance_buy_top) - 1])
                list_time_buy_top.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                buy_top += 1
                buy_top_l += 1

                list_rsi_buy_method1.append(dataset_1h['RSI 14'][i])
                list_momentum_buy_method1.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_buy_method1.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_buy_method1.append(dataset_1h['diff 30 and 60'][i])
                list_result_buy_method1.append(0)

            elif dataset_1h['type trade'][i] == 'Sell from Top':
                list_balance_sell_top.append((1 - risk_trade) * list_balance_sell_top[len(list_balance_sell_top) - 1])
                list_time_sell_top.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                sell_top += 1
                sell_top_l += 1

                list_rsi_sell_method2.append(dataset_1h['RSI 14'][i])
                list_momentum_sell_method2.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_sell_method2.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_sell_method2.append(dataset_1h['diff 30 and 60'][i])
                list_result_sell_method2.append(0)

            elif dataset_1h['type trade'][i] == 'Buy from Below':
                list_balance_buy_below.append((1 - risk_trade) * list_balance_buy_below[len(list_balance_buy_below) - 1])
                list_time_buy_below.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                buy_below += 1
                buy_below_l += 1

                list_rsi_buy_method2.append(dataset_1h['RSI 14'][i])
                list_momentum_buy_method2.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_buy_method2.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_buy_method2.append(dataset_1h['diff 30 and 60'][i])
                list_result_buy_method2.append(0)

            elif dataset_1h['type trade'][i] == 'Sell from Below':
                list_balance_sell_below.append((1 - risk_trade) * list_balance_sell_below[len(list_balance_sell_below) - 1])
                list_time_sell_below.append(str(dataset_1h['Date'][i]) + ' ' + str(dataset_1h['Time'][i]))
                sell_below += 1
                sell_below_l += 1

                list_rsi_sell_method1.append(dataset_1h['RSI 14'][i])
                list_momentum_sell_method1.append(dataset_1h['Momentum 14'][i])
                list_diff15to30_sell_method1.append(dataset_1h['diff 15 and 30'][i])
                list_diff30to60_sell_method1.append(dataset_1h['diff 30 and 60'][i])
                list_result_sell_method1.append(0)

list_type_trade = ['Buy From Top', 'Buy From Below', 'Sell From Top', 'Sell From Below']
list_type_trade_numeric.append(buy_top)
list_type_trade_numeric.append(buy_below)
list_type_trade_numeric.append(sell_top)
list_type_trade_numeric.append(sell_below)

# DB with buy method 1
col_rsi_buy_method1 = pd.Series(list_rsi_buy_method1, name='rsi')
col_momentum_buy_method1 = pd.Series(list_momentum_buy_method1, name='momentum')
col_diff15to30_buy_method1 = pd.Series(list_diff15to30_buy_method1, name='diff15to30')
col_diff30to60_buy_method1 = pd.Series(list_diff30to60_buy_method1, name='diff30to60')
col_result_buy_method1 = pd.Series(list_result_buy_method1, name='result')
db_buy_method1 = pd.concat([col_rsi_buy_method1, col_momentum_buy_method1, col_diff15to30_buy_method1, col_diff30to60_buy_method1, col_result_buy_method1], axis=1)

# DB with buy method 2
col_rsi_buy_method2 = pd.Series(list_rsi_buy_method2, name='rsi')
col_momentum_buy_method2 = pd.Series(list_momentum_buy_method2, name='momentum')
col_diff15to30_buy_method2 = pd.Series(list_diff15to30_buy_method2, name='diff15to30')
col_diff30to60_buy_method2 = pd.Series(list_diff30to60_buy_method2, name='diff30to60')
col_result_buy_method2 = pd.Series(list_result_buy_method2, name='result')
db_buy_method2 = pd.concat([col_rsi_buy_method2, col_momentum_buy_method2, col_diff15to30_buy_method2, col_diff30to60_buy_method2, col_result_buy_method2], axis=1)

# DB with sell method 1
col_rsi_sell_method1 = pd.Series(list_rsi_sell_method1, name='rsi')
col_momentum_sell_method1 = pd.Series(list_momentum_sell_method1, name='momentum')
col_diff15to30_sell_method1 = pd.Series(list_diff15to30_sell_method1, name='diff15to30')
col_diff30to60_sell_method1 = pd.Series(list_diff30to60_sell_method1, name='diff30to60')
col_result_sell_method1 = pd.Series(list_result_sell_method1, name='result')
db_sell_method1 = pd.concat([col_rsi_sell_method1, col_momentum_sell_method1, col_diff15to30_sell_method1, col_diff30to60_sell_method1, col_result_sell_method1], axis=1)

# DB with sell method 2
col_rsi_sell_method2 = pd.Series(list_rsi_sell_method2, name='rsi')
col_momentum_sell_method2 = pd.Series(list_momentum_sell_method2, name='momentum')
col_diff15to30_sell_method2 = pd.Series(list_diff15to30_sell_method2, name='diff15to30')
col_diff30to60_sell_method2 = pd.Series(list_diff30to60_sell_method2, name='diff30to60')
col_result_sell_method2 = pd.Series(list_result_sell_method2, name='result')
db_sell_method2 = pd.concat([col_rsi_sell_method2, col_momentum_sell_method2, col_diff15to30_sell_method2, col_diff30to60_sell_method2, col_result_sell_method2], axis=1)

# click Distribution
if your_request == 'Distribution':
    import seaborn as sns
    # another tab inside tab5
    with tab5:
        # create tabs
        tab5_1, tab5_2, tab5_3 = tab5.tabs(["Total Distribution", "Buy Distribution", "Sell Distribution"])

        # tab 5 - 1: total distribution
        tab5_1.subheader('- Total Distribution:')
        fig_distribution, axes = plt.subplots(1, 2, figsize=(10, 5))
        # Distribution Trades pie chart
        axes[0].pie([buy_top, buy_below, sell_top, sell_below], labels=['Buy From Top', 'Buy From Below', 'Sell From Top', 'Sell From Below'], autopct='%1.1f%%', startangle=90)
        axes[0].axis('equal')
        axes[0].set_title('Distribution Trades')
        # Profit and Loss pie chart
        axes[1].pie([num_profit, num_loss], labels=['Total Profit', 'Total Loss'], autopct='%1.1f%%', startangle=90)
        axes[1].axis('equal')
        axes[1].set_title('Distribution Profit and Loss')
        # show chart
        plt.tight_layout()
        tab5_1.pyplot(fig_distribution)

        # tab 5 - 2: Buy Distribution
        tab5_2.subheader('- Buy Distribution:')
        fig_buy, axes = plt.subplots(1, 2, figsize=(12, 3))
        # Buy From Top pie chart
        axes[0].pie([buy_top_p, buy_top_l], labels=['Buy From Top Profit', 'Buy From Top Loss'], autopct='%1.1f%%', startangle=90)
        axes[0].axis('equal')
        axes[0].set_title('Distribution Buy From Top')
        # Buy From Below pie chart
        axes[1].pie([buy_below_p, buy_below_l], labels=['Buy From Below Profit', 'Buy From Below Loss'], autopct='%1.1f%%', startangle=90)
        axes[1].axis('equal')
        axes[1].set_title('Distribution Buy From Below')
        # show charts buy
        plt.tight_layout()
        tab5_2.pyplot(fig_buy)
        # Pairplot charts buy
        tab5_2.subheader('- Buy Method 1 Pairplot:')
        fig_buy_method1 = sns.pairplot(db_buy_method1, hue='result', height=5)
        tab5_2.pyplot(fig_buy_method1)
        tab5_2.subheader('- Buy Method 2 Pairplot:')
        fig_buy_method2 = sns.pairplot(db_buy_method2, hue='result', height=4)
        tab5_2.pyplot(fig_buy_method2)

        # tab 5 - 3: Sell Distribution
        tab5_3.subheader('- Sell Distribution:')
        fig_sell, axes = plt.subplots(1, 2, figsize=(12, 3))
        # Sell From Top pie chart
        axes[0].pie([sell_top_p, sell_top_l], labels=['Sell From Top Profit', 'Sell From Top Loss'], autopct='%1.1f%%', startangle=90)
        axes[0].axis('equal')
        axes[0].set_title('Distribution Sell From Top')
        # Sell From Below pie chart
        axes[1].pie([sell_below_p, sell_below_l], labels=['Sell From Below Profit', 'Sell From Below Loss'], autopct='%1.1f%%', startangle=90)
        axes[1].axis('equal')
        axes[1].set_title('Distribution Sell From Below')
        # show chart
        plt.tight_layout()
        tab5_3.pyplot(fig_sell)
        # Pairplot charts sell
        tab5_3.subheader('- Sell Method 1 Pairplot:')
        fig_sell_method1 = sns.pairplot(db_sell_method1, hue='result', height=3)
        tab5_3.pyplot(fig_sell_method1)
        tab5_3.subheader('- Sell Method 2 Pairplot:')
        fig_sell_method2 = sns.pairplot(db_sell_method2, hue='result', height=3)
        tab5_3.pyplot(fig_sell_method2)

# click Trade status
elif your_request == 'Trade status':

    # Show balance
    b_total = '{:.2f}'.format(list_balance_total[-1])
    b_buy_top = '{:.2f}'.format(list_balance_buy_top[-1])
    b_buy_below = '{:.2f}'.format(list_balance_buy_below[-1])
    b_sell_below = '{:.2f}'.format(list_balance_sell_below[-1])
    b_sell_top = '{:.2f}'.format(list_balance_sell_top[-1])
    tab5.error(f'Method Total: Balance at the beginning of {start_year} is equal to {your_balance} and at the end of {end_year} is equal to {b_total}')
    tab5.info(f'Method 1 - Buy from above: Balance at the beginning of {start_year} is equal to {your_balance} and at the end of {end_year} is equal to {b_buy_top}')
    tab5.info(f'Method 2 - Buy from below: Balance at the beginning of {start_year} is equal to {your_balance} and at the end of {end_year} is equal to {b_buy_below}')
    tab5.success(f'Method 1 - Sell from below: Balance at the beginning of {start_year} is equal to {your_balance} and at the end of {end_year} is equal to {b_sell_below}')
    tab5.success(f'Method 2 - Sell from above: Balance at the beginning of {start_year} is equal to {your_balance} and at the end of {end_year} is equal to {b_sell_top}')


    # plot for total trades
    fig_total_trades = plt.figure(figsize=(12, 4))
    plt.title('Balance during the Time')
    plt.xlabel('Years')
    plt.ylabel('Dollars')
    plt.xticks([])
    plt.plot(list_time_total, list_balance_total, label='Total Trade')
    plt.plot(list_time_buy_top, list_balance_buy_top, label='Buy Top')
    plt.plot(list_time_sell_top, list_balance_sell_top, label='Sell Top')
    plt.plot(list_time_buy_below, list_balance_buy_below, label='Buy Below')
    plt.plot(list_time_sell_below, list_balance_sell_below, label='Sell Below')
    plt.legend()
    tab5.pyplot(fig_total_trades)

# click Classification
elif your_request == 'Classification':
    # classification BUY method 1
    X_buy_1 = db_buy_method1[['rsi', 'momentum', 'diff15to30', 'diff30to60']]
    y_buy_1 = db_buy_method1['result']
    x_train_buy_1, x_test_buy_1, y_train_buy_1, y_test_buy_1 = train_test_split(X_buy_1, y_buy_1, test_size=0.2, random_state=0)
    logisticRegr_buy_1 = LogisticRegression()
    logisticRegr_buy_1.fit(x_train_buy_1, y_train_buy_1)
    predictions_buy_1 = logisticRegr_buy_1.predict(x_test_buy_1)
    score_buy_1 = logisticRegr_buy_1.score(x_test_buy_1, y_test_buy_1)
    buy_accuracy_1 = "{:.2f}".format(score_buy_1*100)
    tab5.subheader('-Method 1 Buy - Touch from above:')
    tab5.warning("accuracy: {:.2f}".format(score_buy_1))
    if score_buy_1 > prefer_estimate :
        tab5.success(f'Excellent! It has high accuracy. You can trust the offer with {buy_accuracy_1}% accuracy. It is better to trade with the highest possible risk.')
    else:
        tab5.error(f'There is no reliable level of accuracy in estimating the future. It is better to avoid the trade.')

    # classification BUY method 2
    X_buy_2 = db_buy_method2[['rsi', 'momentum', 'diff15to30', 'diff30to60']]
    y_buy_2 = db_buy_method2['result']
    x_train_buy_2, x_test_buy_2, y_train_buy_2, y_test_buy_2 = train_test_split(X_buy_2, y_buy_2, test_size=0.2, random_state=0)
    logisticRegr_buy_2 = LogisticRegression()
    logisticRegr_buy_2.fit(x_train_buy_2, y_train_buy_2)
    predictions_buy_2 = logisticRegr_buy_2.predict(x_test_buy_2)
    score_buy_2 = logisticRegr_buy_2.score(x_test_buy_2, y_test_buy_2)
    buy_accuracy_2 = "{:.2f}".format(score_buy_2 * 100)
    tab5.subheader('-Method 2 Buy - Touch from below:')
    tab5.warning("accuracy: {:.2f}".format(score_buy_2))
    if score_buy_2 > prefer_estimate:
        tab5.success(f'Excellent! It has high accuracy. You can trust the offer with {buy_accuracy_2}% accuracy. It is better to trade with the highest possible risk.')
    else:
        tab5.error(f'There is no reliable level of accuracy in estimating the future. It is better to avoid the trade.')

    # classification Sell method 1
    X_sell_1 = db_sell_method1[['rsi', 'momentum', 'diff15to30', 'diff30to60']]
    y_sell_1 = db_sell_method1['result']
    x_train_sell_1, x_test_sell_1, y_train_sell_1, y_test_sell_1 = train_test_split(X_sell_1, y_sell_1, test_size=0.2, random_state=0)
    logisticRegr_sell_1 = LogisticRegression()
    logisticRegr_sell_1.fit(x_train_sell_1, y_train_sell_1)
    predictions_sell_1 = logisticRegr_sell_1.predict(x_test_sell_1)
    score_sell_1 = logisticRegr_sell_1.score(x_test_sell_1, y_test_sell_1)
    sell_accuracy_1 = '{:.2f}'.format(score_sell_1 * 100)
    tab5.subheader('-Method 1 sell - Touch from below:')
    tab5.warning('accuracy: {:.2f}'.format(score_sell_1))
    if score_sell_1 > prefer_estimate:
        tab5.success(f'Excellent! It has high accuracy. You can trust the offer with {sell_accuracy_1}% accuracy. It is better to trade with the highest possible risk.')
    else:
        tab5.error(f'There is no reliable level of accuracy in estimating the future. It is better to avoid the trade.')

    # classification Sell method 2
    X_sell_2 = db_sell_method2[['rsi', 'momentum', 'diff15to30', 'diff30to60']]
    y_sell_2 = db_sell_method2['result']
    x_train_sell_2, x_test_sell_2, y_train_sell_2, y_test_sell_2 = train_test_split(X_sell_2, y_sell_2, test_size=0.2, random_state=0)
    logisticRegr_sell_2 = LogisticRegression()
    logisticRegr_sell_2.fit(x_train_sell_2, y_train_sell_2)
    predictions_sell_2 = logisticRegr_sell_2.predict(x_test_sell_2)
    score_sell_2 = logisticRegr_sell_2.score(x_test_sell_2, y_test_sell_2)
    sell_accuracy_2 = "{:.2f}".format(score_sell_2 * 100)
    tab5.subheader('-Method 2 sell - Touch from above:')
    tab5.warning("accuracy: {:.2f}".format(score_sell_2))
    if score_sell_2 > prefer_estimate:
        tab5.success(f'Excellent! It has high accuracy. You can trust the offer with {sell_accuracy_2}% accuracy. It is better to trade with the highest possible risk.')
    else:
        tab5.error(f'There is no reliable level of accuracy in estimating the future. It is better to avoid the trade.')

# Tab 2: suggestions
tab6.title('suggestions:')
tab6.write('1- It is suggested that other indicators should be examined in the future. As:')
tab6.write(' - MACD')
tab6.write(' - Ichimoku')
tab6.write(' - Stochastic')
tab6.write(' - Alligator')
tab6.write(' - ...')
tab6.write('2- In this project, only prediction accuracy was checked with the help of classification. But the issue of the success rate of the model should be investigated in more detail. In this way, we will be able to manage the risk of each trade based on its success rate in similar past market conditions.')
tab6.write('3- Due to the high capabilities of the forex market, it is suggested that this model be checked for other currency pairs as well.')
tab6.write('4- By generalizing the model through multi-time frame analysis and adding more conditions, we will probably see an increase in the estimation accuracy.')



