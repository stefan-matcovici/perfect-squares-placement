import pandas as pd
from matplotlib import pyplot as plt


def plot_time(df: pd.DataFrame):
    df_to_plot = pd.DataFrame(df[['square_no', 'time']].groupby('square_no').mean())

    fig = plt.figure(1)
    ax = plt.axes()

    ax.plot(df_to_plot.index.values, df_to_plot.time.values)
    plt.xticks(df_to_plot.index.values)
    plt.xlabel("No of squares")
    plt.ylabel("Seconds on average")

    plt.show()


def plot_error(df: pd.DataFrame):
    df_to_plot = df.copy()
    df_to_plot['error'] = df.result - df.optim
    df_to_plot = pd.DataFrame(df_to_plot[['square_no', 'error']].groupby('square_no').mean())

    fig = plt.figure(2)
    ax = plt.axes()

    ax.plot(df_to_plot.index.values, df_to_plot.error.values)
    plt.xticks(df_to_plot.index.values)
    plt.yticks(df_to_plot.error.values)
    plt.xlabel("No of squares")
    plt.ylabel("Error on average")

    plt.show()


if __name__ == "__main__":
    results = pd.read_csv("results.csv")
    plot_time(results)
    plot_error(results)
