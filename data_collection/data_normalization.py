import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import sys


plt.style.use('fivethirtyeight')


def main():
    df = pd.read_pickle('./daily_log/eth-02-11-23-ft.pkl')
    df = df.iloc[:, 1:]
    training_data_len = math.ceil(df.shape[0] * .8)
    scaler = MinMaxScaler(feature_range=(0, 1))
    feature_names = ['high', 'low', 'open', 'close', 'volume', 'sma_5bar', 'sma_10bar', 'sma_40bar', 'ema_5bar', 'ema_10bar', 'ema_40bar', 'rsi']
    features, training_data, x_train, y_train = [], [], [], []

    for name in feature_names:
        features.append(scaler.fit_transform(df.filter([name]).values))

    for i in range(0, training_data_len):
        training_data.append([])
        for k in range(0, len(features)):
            training_data[i].append(features[k][i][0])

    for i in range(60, training_data_len):
        x_train.append(training_data[i-60:i][:])
        y_train.append(training_data[i][:])

    x_train, y_train = np.array(x_train), np.array(y_train)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

if __name__ == "__main__":
    main()
