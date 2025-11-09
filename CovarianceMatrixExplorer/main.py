from src.data_handler import (
    load_data,
    covariance_correlation,
    eigen_pca,
    plot_heatmaps,
    plot_pca_scree,
)


def main():
    file_path = "data/tech_prices.csv"
    data = load_data(file_path)
    covar, corr = covariance_correlation(data)
    sorted_eigenvalues, sorted_eigenvectors = eigen_pca(corr, 7)
    plot_heatmaps(covar, corr, data.columns)
    plot_pca_scree(sorted_eigenvalues)


if __name__ == "__main__":
    main()
