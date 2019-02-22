import sys
import pandas_datareader.data as web
import datetime
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
import backtrader as bt


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

def data_read():
    data = pd.read_csv('data/iris.csv')
    return data

# Get GS Data from Yahoo
# gs = web.DataReader("066570.KS", "yahoo", "2016-01-01", "2019-02-01")
gs = web.DataReader("066570.KS", "yahoo")
new_gs = gs[gs['Volume']!=0]

# Moving average
ma5 = new_gs['Adj Close'].rolling(window=5).mean()
ma20 = new_gs['Adj Close'].rolling(window=20).mean()
ma60 = new_gs['Adj Close'].rolling(window=60).mean()
ma120 = new_gs['Adj Close'].rolling(window=120).mean()

# Insert columns
new_gs.insert(len(new_gs.columns), "MA5", ma5)
new_gs.insert(len(new_gs.columns), "MA20", ma20)
new_gs.insert(len(new_gs.columns), "MA60", ma60)
new_gs.insert(len(new_gs.columns), "MA120", ma120)


# Plot
# plt.plot(new_gs.index, new_gs['Adj Close'], label='Adj Close')
# plt.plot(new_gs.index, new_gs['MA5'], label='MA5')
# plt.plot(new_gs.index, new_gs['MA20'], label='MA20')
# plt.plot(new_gs.index, new_gs['MA120'], label='MA120')

# plt.legend(loc="best")
# plt.grid()
# plt.show()



# cerebro = bt.Cerebro()
# cerebro.addstrategy(SmaCross)

# data0 = bt.feeds.YahooFinance(dataname='066570.KS', fromdate=datetime(2016, 1, 1), todate=datetime(2019, 2, 1))
# data0 = bt.feeds.YahooFinance(dataname='066570.KS', fromdate=datetime(2016, 1, 1))
# cerebro.adddata(data0)

# cerebro.run()
# cerebro.plot()

# print(new_gs.info)
# print(new_gs.head(10))
# print(new_gs.tail(5))
# print(type(new_gs))
# print(new_gs['Close'])
# print(type(new_gs['Close']))

# print(new_gs.columns) # columns 네임 보여주기
# print(new_gs.index)   # index 출력

# 행렬크기 보기
# print(new_gs.shape)

# 2개 이상을 보기위해서는 대괄호가 2개 필요하다.
# print(new_gs[['Open', 'Close']])

# 특정행을 숫자 index로 보고 싶을 때 iloc
# print(new_gs.iloc[10, :])

# 특정행을 name으로 보고 싶을 때 loc
# print(new_gs.loc['2010-01-18', :])

# print(new_gs.iloc[5:10]['Close'])
# print(new_gs.iloc[::2]['Close'])

data = data_read()
print(data.head(5))

# 컬럼 순서 바꾸기
data = data.reindex(columns = ['sepal_length', 'sepal_width', 'species', 'petal_length', 'petal_width'])
print(data.head(5))

# 컬럼 조건 True, False 추가하기
data['Large'] = data['sepal_length'] > 5
print(data.head(5))

