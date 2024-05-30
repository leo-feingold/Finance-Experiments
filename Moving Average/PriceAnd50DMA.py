import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stock = 'SPY'
start = '2015-01-01'
stop = '2024-05-29'

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
    #data = pd.DataFrame(crossover_other_dates)
    # looks about right #print(data)
    return df, crossover_dates, crossover_other_dates

def visualizeData(df, crossovers, crossover_others):
    fig, axs = plt.subplots(1,1, figsize=(10, 7.5))
    axs.scatter(crossovers, df.loc[crossovers, "Close"], label='Price Passes 50 DMA', color = 'green', zorder = 4)
    axs.scatter(crossover_others, df.loc[crossover_others, "Close"], label='Price Falls Under 50 DMA', color='red', zorder=5)
    axs.plot(df.index, df.Close, label='Stock Price', color='black', zorder=1)
    #axs.plot(df.index, df["50DMA"], label='50 DMA', color='blue', linestyle='--', zorder=2)

    axs.set_xlabel("Date")
    axs.set_ylabel("Price")
    axs.set_title("Stock Price Over Time")
    fig.suptitle(f"Stock: {stock}")
    axs.legend()
    plt.tight_layout()
    plt.show()

def findNextSellDay(df, buy_date, crossover_others):
    future_crossover_others = [date for date in crossover_others if date > buy_date]
    if not future_crossover_others:
        return df.index[-1]
    return min(future_crossover_others)


def buySell(df, crossovers, crossover_others):
    performanceTable = {
            "buy_date": [],
            "buy_price": [],
            "sell_date": [],
            "sell_price": [],
            "return_%": []
    }

    for date in crossovers:
        sell_date = findNextSellDay(df, date, crossover_others)
        sell_price = df.loc[sell_date, "Close"]
        buy_price = df.loc[date, "Close"]
        performanceTable["buy_date"].append(date)
        performanceTable["buy_price"].append(buy_price)
        performanceTable["sell_date"].append(sell_date)
        performanceTable["sell_price"].append(sell_price)
        performanceTable["return_%"].append(((sell_price - buy_price)/buy_price) * 100)

    df = pd.DataFrame(performanceTable)
    # looks about right #print(df["sell_date"])
    df.to_csv("PriceAnd50DMA.csv", index=False)
    return df



def main():
    data = loadData(stock, start, stop)
    data = calc200DMA(data)
    data = calc50DMA(data)
    data, crossover_dates, crossover_other_dates = interestingPoint(data)
    visualizeData(data, crossover_dates, crossover_other_dates)
    buySell(data, crossover_dates, crossover_other_dates)

if __name__ == "__main__":
    main()