import pandas as pd


def combine_data(filename1, filename2):
    df1 = pd.read_pickle(filename1)
    df2 = pd.read_pickle(filename2)
    
    return(pd.concat([df1, df2], axis=0))


def main():
    df1 = combine_data('./daily_log/eth-01-20-23.pkl', './daily_log/eth-01-21-23.pkl')
    df2 = combine_data('./daily_log/eth-01-22-23.pkl', './daily_log/eth-01-23-23.pkl')
    df3 = combine_data('./daily_log/eth-01-24-23.pkl', './daily_log/eth-01-25-23.pkl')
    df4 = combine_data('./daily_log/eth-01-26-23.pkl', './daily_log/eth-01-27-23.pkl')

    df5 = pd.concat([df1, df2], axis=0)
    df6 = pd.concat([df3, df4], axis=0)

    df = pd.concat([df5, df6], axis=0)

    df.to_pickle('./daily_log/combined.pkl')


if __name__ == "__main__":
    main()