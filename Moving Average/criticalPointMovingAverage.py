import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

stock = 'IBM'
start = '2015-01-01'
stop = '2024-05-16'

def loadData(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.dropna(inplace=True)
    return df

def calc50DMA(df):
    df["50DMA"] = df.Close.rolling(window=50).mean()
    return df

def calc200DMA(df):
    df["200DMA"] = df.Close.rolling(window=200).mean()
    return df

def norm50DMA(df):
    df["Norm50DMA"] = df["50DMA"] / df["200DMA"]
    return df

def findCriticalPoints(df):
    df["50Over200"] = df["50DMA"] > df["200DMA"]
    df["Crossover"] = df["50Over200"].diff() == 1
    
    crossover_dates = df.index[df["Crossover"]].tolist()
    return df, crossover_dates

def visualizeData(df, crossovers):
    fig, axs = plt.subplots(1,1, figsize=(10, 7.5))

    axs.plot(df.index, df.Close, label="Stock Price", color="red", zorder=1)
    axs.scatter(crossovers, df.loc[crossovers, "Close"], label="Golden Cross", color="black", zorder=2)
    axs.set_title("Stock Price Over Time")
    axs.set_xlabel("Date")
    axs.set_ylabel("Price")
    axs.legend()
    fig.suptitle(f"Stock: {stock}, Golden Crosses")
    plt.show()



def main():
    data = loadData(stock, start, stop)
    data = calc200DMA(data)
    data = calc50DMA(data)
    data = norm50DMA(data)
    dates = findCriticalPoints(data)[1]
    visualizeData(data, dates)

if __name__ == "__main__":
    main()