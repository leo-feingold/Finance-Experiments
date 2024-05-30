import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

show_moving_averages = False
timeElapsed = 25
stock = 'QQQ'
start = '2000-01-01'
stop = '2024-05-27'

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

def find_nearest_date(df, target_date):
    time_diff = np.abs(df.index - target_date)
    closest_index = time_diff.argmin()
    closest_date = df.index[closest_index]
    return closest_date


def findCriticalPoints(df):
    df["50Over200"] = df["50DMA"] > df["200DMA"]
    df["Crossover"] = (df["50Over200"] == True) & (df["50Over200"].shift(1) == False)
    df["CrossoverOther"] = (df["50Over200"] == False) & (df["50Over200"].shift(1) == True)
    
    crossover_dates = df.index[df["Crossover"]].tolist()
    crossover_other_dates = df.index[df["CrossoverOther"]].tolist()
    return df, crossover_dates, crossover_other_dates

def findNextSellDay(df, buy_date, crossover_others):
    future_crossover_others = [date for date in crossover_others if date > buy_date]
    if not future_crossover_others:
        return df.index[-1]
    return min(future_crossover_others)


def getPerformance(df, crossovers, crossover_others):
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
    df.to_csv(f"{stock}_buyGoldSellDeath.csv", index=False)
    return df

def visualizeData(df, crossovers, crossover_others):
    fig, axs = plt.subplots(1,1, figsize=(10, 7.5))

    axs.plot(df.index, df.Close, label="Stock Price", color="black", zorder=1)

    if show_moving_averages:
        axs.plot(df.index, df["50DMA"], label="50DMA", color="blue", linestyle='--', zorder=2)
        axs.plot(df.index, df["200DMA"], label="200DMA", color="green", linestyle='--', zorder=3)
        fig.suptitle(f"Stock: {stock}, Golden and Death Crosses. Include Moving Averages Mode: On")

    else: fig.suptitle(f"Stock: {stock}, Golden and Death Crosses. Include Moving Averages Mode: Off")
    axs.scatter(crossovers, df.loc[crossovers, "Close"], label="Golden Cross", color="gold", zorder=4)
    axs.scatter(crossover_others, df.loc[crossover_others, "Close"], label="Death Cross", color='red', zorder=5)
    axs.set_title("Stock Price Over Time")
    axs.set_xlabel("Date")
    axs.set_ylabel("Price")
    axs.legend()
    plt.show()

def main():
    data = loadData(stock, start, stop)
    data = calc200DMA(data)
    data = calc50DMA(data)
    data, dates, dates_other = findCriticalPoints(data)
    visualizeData(data, dates, dates_other)
    table = getPerformance(data, dates, dates_other)


if __name__ == "__main__":
    main()