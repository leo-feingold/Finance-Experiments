import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

show_moving_averages = False
timeElapsed = 25
stock = 'SPY'
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

def findCriticalPoints(df):
    df["50Over200"] = df["50DMA"] > df["200DMA"]
    df["Crossover"] = (df["50Over200"] == True) & (df["50Over200"].shift(1) == False)
    df["CrossoverOther"] = (df["50Over200"] == False) & (df["50Over200"].shift(1) == True)
    
    crossover_dates = df.index[df["Crossover"]].tolist()
    crossover_other_dates = df.index[df["CrossoverOther"]].tolist()
    return df, crossover_dates, crossover_other_dates

def visualizeData(df, crossovers, crossover_others, summary):
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

    summary_text = (
        f"Time Interval: {timeElapsed} Days\n"
        f"Golden Cross Avg Return: {summary['golden_cross_avg_return']:.2%}\n"
        f"Golden Cross Median Return: {summary['golden_cross_median_return']:.2%}\n"
        f"Death Cross Avg Return: {summary['death_cross_avg_return']:.2%}\n"
        f"Death Cross Median Return: {summary['death_cross_median_return']:.2%}"
    )
    axs.text(0.015, 0.85, summary_text, transform=axs.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

    axs.legend()
    plt.show()

def determinePerformance(df, crossovers, crossover_others, interval):
    performance = {
        "golden_cross": [],
        "death_cross": []
    }

    for date in crossovers:
        if date + pd.DateOffset(days=interval) in df.index:
            start_price = df.loc[date, "Close"]
            end_price = df.loc[date + pd.DateOffset(days=interval), "Close"]
            performance["golden_cross"].append((end_price - start_price) / start_price)

    for date in crossover_others:
        if date + pd.DateOffset(days=interval) in df.index:
            start_price = df.loc[date, "Close"]
            end_price = df.loc[date + pd.DateOffset(days=interval), "Close"]
            performance["death_cross"].append((end_price - start_price) / start_price)
    
    summary = {
        "golden_cross_avg_return": np.mean(performance["golden_cross"]),
        "golden_cross_median_return": np.median(performance["golden_cross"]),
        "death_cross_avg_return": np.mean(performance["death_cross"]),
        "death_cross_median_return": np.median(performance["death_cross"])
    }

    return summary


def main():
    data = loadData(stock, start, stop)
    data = calc200DMA(data)
    data = calc50DMA(data)
    data, dates, dates_other = findCriticalPoints(data)
    summary = determinePerformance(data, dates, dates_other, timeElapsed)
    visualizeData(data, dates, dates_other, summary)

if __name__ == "__main__":
    main()