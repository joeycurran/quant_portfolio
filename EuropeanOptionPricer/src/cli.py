import argparse


def parse_args():
    """Parse command line arguments for running benchmarks."""
    parser = argparse.ArgumentParser(description="Run Monte Carlo Simulation.")
    parser.add_argument(
        "--stock-price", help="current stock price", type=float, required=True
    )
    parser.add_argument(
        "--strike-price", help="strike price", type=float, required=True
    )
    parser.add_argument(
        "--time-to-maturity",
        help="time to maturity in years",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--risk-free-rate",
        help="annual risk-free interest rate (as a decimal)",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--volatility",
        help="annual volatility (as a decimal)",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--num-simulations",
        help="number of Monte Carlo simulations to run",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--option-type",
        help="call or put option",
        type=str,
        required=True,
        choices=["call", "put", "all"],
    )

    return parser.parse_args()
