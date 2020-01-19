import pandas as pd
from matplotlib import pyplot as plt


def plot_time(df: pd.DataFrame):
    df_to_plot = df[df.time != -1]
    df_to_plot = pd.DataFrame(df_to_plot[['square_no', 'time']].groupby('square_no').mean())

    ax = plt.axes()

    ax.plot(df_to_plot.index.values, df_to_plot.time.values)
    plt.xticks(df_to_plot.index.values)
    plt.xlabel("No of squares")
    plt.ylabel("Seconds on average")

    plt.show()


def plot_error(df: pd.DataFrame):
    df_to_plot = df[df.time != -1]
    df_to_plot = df_to_plot.assign(error=df_to_plot.result - df_to_plot.optim)
    df_to_plot = pd.DataFrame(df_to_plot[['square_no', 'error']].groupby('square_no').mean())

    ax = plt.axes()

    ax.plot(df_to_plot.index.values, df_to_plot.error.values)
    plt.xticks(df_to_plot.index.values)
    plt.yticks(df_to_plot.error.values, fontsize=6)
    plt.xlabel("No of squares")
    plt.ylabel("Error on average")
    plt.tight_layout()

    plt.show()


def plot_time_exceeded(df: pd.DataFrame):
    exceeded_df = df.where(df.time == -1)

    exceeded_df = pd.DataFrame(exceeded_df[['square_no', 'time']].groupby('square_no').count())
    all_df = pd.DataFrame(df[['square_no', 'time']].groupby('square_no').count())

    df_to_plot = pd.DataFrame()
    df_to_plot = df_to_plot.assign(time=(exceeded_df.time / all_df.time) * 100)
    df_to_plot.fillna(0, inplace=True)

    ax = plt.axes()

    ax.plot(df_to_plot.index.values, df_to_plot.time.values)
    plt.xticks(df_to_plot.index.values)
    plt.yticks(df_to_plot.time.values)
    plt.xlabel("No of squares")
    plt.ylabel("No of instances")

    plt.show()


def plot_distribution(df: pd.DataFrame):
    df_to_plot = pd.DataFrame(df[['square_no', 'time']].groupby('square_no').count())

    ax = plt.axes()

    ax.bar(df_to_plot.index.values, height=df_to_plot.time.values)
    plt.xlabel("No of squares")
    plt.ylabel("Time exceeded percentage")

    plt.show()


if __name__ == "__main__":
    results = pd.read_csv("results_100.csv")
    # plot_time(results)
    # plot_error(results)
    # plot_time_exceeded(results)
    plot_distribution(results)
