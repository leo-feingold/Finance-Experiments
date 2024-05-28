import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

stock = 'IBM'
start = '2015-01-01'
stop = '2024-05-16'


def getData(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    #print(data.columns) # --> ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    data.dropna(inplace=True)  
    return data

def calc200DayMovingAverage(df):
    df["200DayMovingAverage"] = df.Close.rolling(window=200).mean()
    return df

def calc50DayMovingAverage(df):
    df["50DayMovingAverage"] = df.Close.rolling(window=50).mean()
    return df

def normalize50DayMovingAverage(df):
    df["Normalized_50DayMovingAverage"] = df["50DayMovingAverage"]/df["200DayMovingAverage"]
    return df

def calcFuturePriceChange(df, interval):
    df["FuturePriceChange"] = (df.Close.shift(-interval) / df.Close) - 1
    return df

def calcCorrelation(df):
    correlation = df[["Normalized_50DayMovingAverage", "FuturePriceChange"]].corr().iloc[0, 1]
    return correlation

def visualizeData(df, interval, corr):
    fig, axs = plt.subplots(3,1, figsize=(10, 7.5))

    axs[0].plot(df.index, df["Normalized_50DayMovingAverage"], label='50 DMA', color='black')
    axs[0].set_title(f"Normalized 50 Day Moving Average")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("Normalized 50 DMA")
    axs[0].legend()

    axs[1].plot(df.index, df["FuturePriceChange"], label='Price Change', color = 'blue')
    axs[1].set_title(f"Percent Change Over Next {interval} Days")
    axs[1].set_xlabel("Date")
    axs[1].set_ylabel("Percent Change")
    axs[1].legend()

    axs[2].scatter(df["FuturePriceChange"], df["Normalized_50DayMovingAverage"], label='50 DMA vs Price Change', color = 'green')
    axs[2].set_title(f"Normalized 50 DMA vs Percent Change Over Next {interval} Days")
    axs[2].set_xlabel("Percent Change")
    axs[2].set_ylabel("Normalized 50 DMA")
    axs[2].legend()

    fig.suptitle(f"Stock: {stock}, Correlation: {corr:.2f}, r^2: {corr**2:.2f}", fontsize=16)
    plt.tight_layout()
    plt.show()


def main():
    interval = 30
    data = getData(stock, start, stop)
    data = calc200DayMovingAverage(data)
    data = calc50DayMovingAverage(data)
    data = normalize50DayMovingAverage(data)
    data = calcFuturePriceChange(data, interval)
    correlation = calcCorrelation(data)
    print(f"Stock: {stock} \nCorrelation of normalized 50-day moving average and change in stock price over {interval} days is: {correlation}")
    visualizeData(data, interval, correlation)

if __name__ == "__main__":
    main()
