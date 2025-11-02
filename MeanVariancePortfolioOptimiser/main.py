from cli import parse_args
from get_data import get_data
import calculations as cal
import numpy as np


def main():
    args = parse_args()
    stock_tickers = args.stock_tickers
    start_date = args.start_date
    end_date = args.end_date

    print("\n--- Portfolio Inputs ---")
    print(f"Stock Tickers: {stock_tickers}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    stock_data = get_data(stock_tickers, start_date, end_date)

    if stock_data is not None:
        print("\n--- Retrieved Stock Data ---")
        print(stock_data.head())
    else:
        print("Failed to retrieve stock data.")

    log_returns = cal.calculate_log_returns(stock_data)
    mean_returns = cal.calculate_annualized_mean_returns(log_returns)
    covariance_matrix = cal.calculate_annualized_covariance(log_returns)
    optimal_weights = cal.optimize_portfolio(covariance_matrix)

    print("\n--- Annualized Mean Returns ---")
    print(mean_returns)
    print("\n--- Annualized Covariance Matrix ---")
    print(covariance_matrix)
    print("\n--- Portfolio Optimization Results ---")
    print("Optimal Weights:")
    for ticker, weight in zip(stock_tickers, optimal_weights):
        print(f"{ticker}: {weight:.4f}")
    print("\n--- Portfolio Performance ---")
    print(
        f"Expected Annual Return: {cal.calculate_portfolio_return(optimal_weights, mean_returns):.4f}"
    )
    print(
        f"Expected Annual Volatility: {cal.calculate_portfolio_volatility(optimal_weights, covariance_matrix):.4f}"
    )


if __name__ == "__main__":
    main()
