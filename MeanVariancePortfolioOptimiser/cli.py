import argparse

# MSFT, AAPL, GOOG


def parse_args():
    """Parse command line arguments for running benchmarks."""
    parser = argparse.ArgumentParser(description="Run Monte Carlo Simulation.")
    parser.add_argument(
        "--stock-tickers",
        help="comma-separated list of stock tickers",
        nargs="+",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--start-date",
        help="start date for historical data (YYYY-MM-DD)",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--end-date",
        help="end date for historical data (YYYY-MM-DD)",
        type=str,
        required=True,
    )

    return parser.parse_args()
