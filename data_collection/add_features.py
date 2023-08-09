import pandas as pd


def add_sma(df, num_rows):
    sma_5bar = [0] * 40
    sma_10bar = [0] * 40
    sma_40bar = [0] * 40

    for i in range(40, num_rows):
        val_5bar = 0
        val_10bar = 0
        val_40bar = 0

        for k in range(i - 5, i):
            val_5bar += df.iloc[k]['close']

        for k in range(i - 10, i):
            val_10bar += df.iloc[k]['close']

        for k in range(i - 40, i):
            val_40bar += df.iloc[k]['close']

        val_5bar /= 5
        val_10bar /= 10
        val_40bar /= 40

        sma_5bar.append(val_5bar)
        sma_10bar.append(val_10bar)
        sma_40bar.append(val_40bar)

    df['sma_5bar'] = sma_5bar
    df['sma_10bar'] = sma_10bar
    df['sma_40bar'] = sma_40bar


def add_ema(df, num_rows):
    ema_5bar = [0] * 40
    ema_10bar = [0] * 40
    ema_40bar = [0] * 40

    ema_5bar.append(df.iloc[40]['sma_5bar'])
    ema_10bar.append(df.iloc[40]['sma_10bar'])
    ema_40bar.append(df.iloc[40]['sma_40bar'])

    for i in range(41, num_rows):
        # smoothing constants
        sc5 = 2 / (5+1)
        sc10 = 2 / (10+1)
        sc40 = 2 / (40+1)

        close = df.iloc[i]['close']

        ema_5bar.append(((close - ema_5bar[i-1]) * sc5) + ema_5bar[i-1])
        ema_10bar.append(((close - ema_10bar[i-1]) * sc10) + ema_10bar[i-1])
        ema_40bar.append(((close - ema_40bar[i-1]) * sc40) + ema_40bar[i-1])

    df['ema_5bar'] = ema_5bar
    df['ema_10bar'] = ema_10bar
    df['ema_40bar'] = ema_40bar


def add_rsi(df, num_rows):
    rsi = [0] * 40

    for i in range(40, num_rows):
        gain_list = []
        loss_list = []
        gain_prev = 0
        loss_prev = 0

        for k in range((i-14), i):
            dif = df.iloc[k]['close'] - df.iloc[k-1]['close']
            if dif == 0:
                pass
            elif dif > 0:
                gain_list.append(dif)
            else:
                loss_list.append(abs(dif))

        if len(gain_list) != 0:
            for g in gain_list:
                gain_prev += g
            gain_prev /= len(gain_list)

        if len(loss_list) != 0:
            for l in loss_list:
                loss_prev += l
            loss_prev /= len(loss_list)

        dif_cur = df.iloc[i]['close'] - df.iloc[i-1]['close']

        gain_cur = 0
        loss_cur = 0

        if dif_cur > 0:
            gain_cur = dif_cur
        elif dif_cur < 0:
            loss_cur = abs(dif_cur)

        if (loss_prev == 0) and (loss_cur == 0):
            rsi.append(100)
        else:
            rsi.append(round(100 - (100 / (1 + (((gain_prev * 13) + gain_cur) / ((loss_prev * 13) + loss_cur)))), 3))

    df['rsi'] = rsi


def add_features(filename):
    df = pd.read_pickle(filename)
    
    num_rows = df.shape[0]

    add_sma(df, num_rows)
    add_ema(df, num_rows)
    add_rsi(df, num_rows)

    return(df.iloc[40:,:])


def main():
    df = add_features('./daily_log/combined.pkl')
    df.to_pickle('./daily_log/combined-ft.pkl')


if __name__ == "__main__":
    main()
