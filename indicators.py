def moving_func(period, dataset):
    """
    this function calculates moving average.
    :param period: period of moving average
    :param dataset: select dataset
    :return: return list of moving average
    """
    moving_list = []
    for i in range(len(dataset['Date'])):
        if i > period:
            moving_amount = dataset.loc[i - period:i, 'BC'].mean()
        else:
            moving_amount = 0
        moving_list.append(moving_amount)
    return moving_list


def momentum_func(period, dataset):
    """
    this function calculates momentum.
    :param period: period of momentum
    :param dataset: select dataset
    :return: return list of momentum
    """
    momentum_list = []
    for i in range(len(dataset['Date'])):
        if i > period:
            close_first = dataset['BC'][i-1]
            close_end = dataset['BC'][i-period]
            mom_amount = (close_first / close_end) * 100
        else:
            mom_amount = 0
        momentum_list.append(mom_amount)
    return momentum_list


def rsi_func(period, dataset):
    """
    this function calculates RSI.
    :param period: period of RSI
    :param dataset: select dataset
    :return: return RSI
    """
    rsi_list = []
    for i in range(len(dataset['Date'])):
        if i > period:
            sum_profit = 0
            sum_loss = 0
            for j in range(i - period, i):
                bch = dataset['BCh'][j]
                price_close = dataset['BC'][j]
                if bch > 0:
                    sum_profit = sum_profit + price_close
                else:
                    sum_loss = sum_loss + price_close
            average_sum_profit = sum_profit / period
            average_loss_profit = sum_loss / period
            if average_loss_profit == 0:
                rsi_amount = 0
            else:
                rsi_amount = 100 - (100 / (1 + (average_sum_profit/average_loss_profit)))
        else:
            rsi_amount = 0
        rsi_list.append(rsi_amount)
    return rsi_list


