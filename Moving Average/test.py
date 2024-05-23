import yfinance as yf
import pandas as pd
import numpy as np

stock = 'AMZN'
start = '2015-01-01'
stop = '2024-05-16'


def getData(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    #print(data.columns) # --> ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    data.dropna(inplace=True)  
    return data

def calc50DayMovingAverage(df):
    df["50DayMovingAverage"] = df.Close.rolling(window=50).mean()
    return df

def calcFuturePriceChange(df, interval):
    df["FuturePriceChange"] = (df.Close / df.Close.shift(-interval)) - 1
    return df

def calcCorrelation(df):
    correlation = df[["50DayMovingAverage", "FuturePriceChange"]].corr().iloc[0, 1]
    return correlation

def main():
    interval = 365
    data = getData(stock, start, stop)
    data = calc50DayMovingAverage(data)
    data = calcFuturePriceChange(data, interval)
    correlation = calcCorrelation(data)
    print(f"Stock: {stock} \nCorrelation of 50-Day Moving Average and % change in stock price over {interval} days is: {correlation}")

if __name__ == "__main__":
    main()
