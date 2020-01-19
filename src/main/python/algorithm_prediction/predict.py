import os
from operator import itemgetter

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import skew, kurtosis
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

from datasets import datasets


def get_sizes(x):
    return [dataset.square_sizes for dataset in itemgetter(*x.instance_no.values.tolist())(datasets)]


def wrap(accum, f, *arg):
    return lambda x: [f(result, arg) if len(arg) >= 1 else f(result) for result in accum(x)]


def rmse_cv(model, x, y):
    rmse = np.sqrt(-cross_val_score(model, x, y, scoring="neg_mean_squared_error", cv=5))
    return (rmse)


if __name__ == "__main__":
    results = pd.read_csv(os.path.join(os.pardir, "results_100.csv"))
    results.instance_no = results.instance_no.astype(int)

    results = results.assign(avg=wrap(get_sizes, np.mean))
    results = results.assign(median=wrap(get_sizes, np.median))
    results = results.assign(std=wrap(get_sizes, np.std))
    results = results.assign(p80=wrap(get_sizes, np.percentile, 80))
    results = results.assign(p90=wrap(get_sizes, np.percentile, 90))
    results = results.assign(p95=wrap(get_sizes, np.percentile, 95))
    results = results.assign(skew=wrap(get_sizes, skew))
    results = results.assign(kurt=wrap(get_sizes, kurtosis))
    results = results.assign(min=wrap(get_sizes, min))
    results = results.assign(max=wrap(get_sizes, max))
    results = results.assign(len=wrap(get_sizes, len))

    results.drop(columns=["instance_no", "square_no"], inplace=True)
    results.replace(to_replace=-1, value=np.max(results['time']), inplace=True)
    print(results.head())

    time_data = results.drop(columns=["result"])

    y = time_data['time']
    X = time_data.drop(columns=['time'])

    alphas = [0.05, 0.1, 0.3, 1, 3, 5, 10, 15, 30, 50, 75]
    cv_ridge = [rmse_cv(Ridge(alpha=alpha), X, y).mean()
                for alpha in alphas]

    # cv_ridge = pd.Series(cv_ridge, index=alphas)
    # cv_ridge.plot(title="Validation")
    # plt.xlabel("alpha")
    # plt.ylabel("rmse")

    # plt.show()

    # print(cv_ridge.min())

    import xgboost as xgb
    from sklearn.model_selection import train_test_split

    X_tr, X_val, y_tr, y_val = train_test_split(X, y, random_state=3)
    X_tr.p80 = X_tr.p80.astype(float)
    X_tr.p90 = X_tr.p90.astype(float)
    X_tr.p95 = X_tr.p95.astype(float)
    dtrain = xgb.DMatrix(X_tr, label=y)

    params = {"learning_rate": 0.1,
              "n_estimators": 1000,
              "max_depth": 3,
              "subsample": 0.8,
              "colsample_bytree": 1,
              "gamma": 1,
              "eta": 0.1
              }
    model = xgb.cv(params, dtrain, num_boost_round=10, early_stopping_rounds=100, nfold=5)

    model.loc[:, ["test-rmse-mean", "train-rmse-mean"]].plot()
    plt.show()
