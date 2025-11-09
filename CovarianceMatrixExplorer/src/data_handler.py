import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data


def log_returns(data):
    log_returns = pd.DataFrame(index=data.index)
    for col in data.columns:
        log_returns[col] = np.log(data[col] / data[col].shift(1))

    return log_returns.dropna()


def covariance_correlation(data):
    covar = pd.DataFrame(
        np.cov(data, rowvar=False), index=data.columns, columns=data.columns
    )  # becasue out columns are the independent data
    corr = data.corr()
    print("Correlation Matrix:\n", corr)
    return covar, corr


def plot_heatmaps(cov, corr, tickers):
    fig, axes = plt.subplots(1, 1, figsize=(14, 6))

    sns.heatmap(
        corr,
        ax=axes,
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        xticklabels=tickers,
        yticklabels=tickers,
    )
    axes.set_title("Correlation Matrix")

    axes.set_xlabel("Assets")
    axes.set_ylabel("Assets")

    plt.tight_layout()
    plt.show()
    plt.close()


def plot_pca_scree(eigvals):
    total_var = np.sum(eigvals)
    explained_var_ratio = eigvals / total_var
    cum_var = np.cumsum(explained_var_ratio)

    plt.figure(figsize=(8, 5))
    plt.bar(
        range(1, len(eigvals) + 1),
        explained_var_ratio,
        label="Individual Explained Variance",
    )
    x = np.arange(1, len(eigvals) + 1)
    plt.plot(
        x,
        cum_var,
        color="black",
        marker="o",
        linewidth=2,
        label="Cumulative Explained Variance curve",
    )
    plt.step(
        range(1, len(eigvals) + 1),
        cum_var,
        where="mid",
        label="Cumulative Explained Variance",
        color="red",
    )
    plt.xlabel("Principal Component")
    plt.ylabel("Proportion of Variance Explained")
    plt.title("Scree Plot (PCA)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
    plt.close()


def eigen_pca(corr, k=3):
    corr_eig = np.linalg.eig(corr)
    indices = np.argsort(corr_eig[0])[::-1]
    corr_eig = (corr_eig[0][indices], corr_eig[1][:, indices])

    print(corr_eig)
    return corr_eig[0][:k], corr_eig[1][:, :k]
