import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pdb
pd.options.mode.chained_assignment = None

# get the S&P 500 symbol from wikipedia page
tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = tickers.Symbol.to_list()
tickers = [i.replace('.','-') for i in tickers] # BRK.B -> BRK-B

def RSIcalc(asset):
    df = yf.download(asset,start='2011-01-01')
    df['MA200'] = df['Adj Close'].rolling(window=200).mean() # mean of the last 200 days

    # relative return
    df['price change'] = df['Adj Close'].pct_change() # get the daily return
    df['Upmove'] = df['price change'].apply(lambda x: x if x>0 else 0)
    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)

    # 移动平均线(MA:Moving Average): 将一定时期内的证券价格（指数）加以平均
    # 并把不同时间的平均值连接起来，形成一根MA，用以观察证券价格变动趋势的一种技术指标。
    # Exponential moving average
    df['avg Up'] = df['Upmove'].ewm(span=19).mean()  # ewm, exponential moving average
    df['avg Down'] = df['Downmove'].ewm(span=19).mean()

    df = df.dropna()

    df['RS'] = df['avg Up'] / df['avg Down']
    df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))

    if not df.empty:
        # make decision
        df.loc[(df['Adj Close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
        df.loc[(df['Adj Close'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = 'No'
    return df

def getSignals(df):
    Buying_dates = []
    Selling_dates = []

    for i in range(len(df)-11):
        if i >= df.shape[0]:
            print('in')
            df = df.reindex(index=list(df.index) + [i])
        if "Yes" in df['Buy'].iloc[i]:
            Buying_dates.append(df.iloc[i+1].name)
            for j in range(1,11):
                if df['RSI'].iloc[i+j] > 30:
                    Selling_dates.append(df.iloc[i+j+1].name)
                    break
                elif j == 10:
                    Selling_dates.append(df.iloc[i+j+1].name)
    return Buying_dates, Selling_dates

# main part
matrixsignals = []
matrixprofits = []

for i in range(len(tickers)):
    # print(f'stock {tickers[i]}')
    frame = RSIcalc(tickers[i])
    buy, sell = getSignals(frame)
    Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
    matrixsignals.append(buy)
    matrixprofits.append(Profits)

# len(matrixprofits)

allprofit = []
for i in matrixprofits:
    for e in i:
        allprofit.append(e)

wins = [i for i in allprofit if i > 0]
win_rate = len(wins)/len(allprofit)  # calc win rate
print('win rate: ', win_rate)