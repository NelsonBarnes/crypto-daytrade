import requests
import pandas as pd
from datetime import date


def minute_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    return df

def main():
    # 1980 min = 1 day 9 hr
    df = minute_price_historical('ETH', 'USD', 1980, 1)
    df.drop(df.tail(1).index,inplace=True)
    df.drop('volumefrom', axis=1, inplace=True)
    df.drop('conversionType', axis=1, inplace=True)
    df.drop('conversionSymbol', axis=1, inplace=True)
    df.rename(columns={'volumeto': 'volume'}, inplace=True)

    today = date.today()
    mdy = today.strftime("%m-%d-%y")

    df.to_pickle('./daily_log/eth-' + mdy + '.pkl')

if __name__ == "__main__":
    main()
