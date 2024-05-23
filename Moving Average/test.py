import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

stock = 'AAPL'
start = '2015-01-01'
stop = '2024-05-16'


def getData(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    #print(data.columns) # --> ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    data.dropna(inplace=True)  
    return data

def calc50DayMovingAverage(df):
    # I think I need to normalize this
    df["50DayMovingAverage"] = df.Close.rolling(window=50).mean()
    return df

def calcFuturePriceChange(df, interval):
    # worried this is wrong #df["FuturePriceChange"] = (df.Close / df.Close.shift(-interval)) - 1
    df["FuturePriceChange"] = (df.Close.shift(-interval) / df.Close) - 1
    return df

def calcCorrelation(df):
    correlation = df[["50DayMovingAverage", "FuturePriceChange"]].corr().iloc[0, 1]
    return correlation

def visualizeData(df, interval):
    fig, axs = plt.subplots(2,1, figsize=(10, 7.5))

    axs[0].plot(df.index, df["50DayMovingAverage"], label='50 DMA', color='black')
    axs[0].set_title("50 Day Moving Average")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("50 DMA")
    axs[0].legend()

    axs[1].plot(df.index, df["FuturePriceChange"], label='Price Change', color = 'blue')
    axs[1].set_title(f"Percent Change Over Next {interval} Days")
    axs[1].set_xlabel("Date")
    axs[1].set_ylabel("Percent Change In Price")
    axs[1].legend()

    plt.tight_layout()
    plt.show()


def main():
    interval = 365
    data = getData(stock, start, stop)
    data = calc50DayMovingAverage(data)
    data = calcFuturePriceChange(data, interval)
    correlation = calcCorrelation(data)
    print(f"Stock: {stock} \nCorrelation of 50-Day Moving Average and change in stock price over {interval} days is: {correlation}")
    visualizeData(data, interval)

if __name__ == "__main__":
    main()
