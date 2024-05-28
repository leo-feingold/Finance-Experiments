import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stock = 'QQQ'
start = '2020-01-01'
stop = '2024-05-27'

def loadData(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.dropna(inplace=True)
    return df

def calc50DMA(df):
    df["50DMA"] = df["Close"].rolling(window=50).mean()
    return df

def calc200DMA(df):
    df["200DMA"] = df["Close"].rolling(window=200).mean()
    return df

def interestingPoint(df):
    df["PriceOver50DMA"] = df["Close"] > df["50DMA"]
    df["Crossover"] = (df["PriceOver50DMA"] == True) & (df["PriceOver50DMA"].shift(1) == False)
    df["CrossoverOther"] = (df["PriceOver50DMA"] == False) & (df["PriceOver50DMA"].shift(1) == True)

    crossover_dates = df.index[df["Crossover"]].tolist()
    crossover_other_dates = df.index[df["CrossoverOther"]].tolist()
    print(crossover_dates,'\n',crossover_other_dates)
    return df, crossover_dates, crossover_other_dates

def visualizeData(df, crossovers, crossover_others):
    fig, axs = plt.subplots(1,1, figsize=(10, 7.5))
    axs.scatter(crossovers, df.loc[crossovers, "Close"], label='Price Passes 50 DMA', color = 'green', zorder = 4)
    axs.scatter(crossover_others, df.loc[crossover_others, "Close"], label='Price Falls Under 50 DMA', color='red', zorder=5)
    axs.plot(df.index, df.Close, label='Stock Price', color='black', zorder=1)
    axs.plot(df.index, df["50DMA"], label='50 DMA', color='blue', linestyle='--', zorder=2)

    axs.set_xlabel("Date")
    axs.set_ylabel("Price")
    axs.set_title("Stock Price Over Time")
    fig.suptitle(f"Stock: {stock}")
    axs.legend()
    plt.tight_layout()
    plt.show()



def main():
    data = loadData(stock, start, stop)
    data = calc200DMA(data)
    data = calc50DMA(data)
    data, crossover_dates, crossover_other_dates = interestingPoint(data)
    visualizeData(data, crossover_dates, crossover_other_dates)

if __name__ == "__main__":
    main()