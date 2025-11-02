from cli import parse_args
from model import EuropeanOptionPricerModel


def main():
    print("Welcome to the European Option Pricer!")
    args = parse_args()

    # Unpack arguments
    S0 = args.stock_price
    K = args.strike_price
    T = args.time_to_maturity
    r = args.risk_free_rate
    sigma = args.volatility
    num_simulations = args.num_simulations
    option_type = args.option_type

    print("\n--- Option Inputs ---")
    print(f"Stock Price (S): {args.stock_price:.2f}")
    print(f"Strike Price (K): {args.strike_price:.2f}")
    print(f"Time to Maturity (T): {args.time_to_maturity} years")
    print(
        f"Risk-Free Rate (r): {args.risk_free_rate:.4f} ({(args.risk_free_rate * 100):.2f}%)"
    )
    print(f"Volatility (sigma): {args.volatility:.4f} ({(args.volatility * 100):.2f}%)")
    print(f"MC Simulations: {args.num_simulations:,}")  # {:,} adds commas

    # Monte Carlo Simulation
    model = EuropeanOptionPricerModel(
        spot_price=S0,
        strike_price=K,
        time_to_maturity=T,
        risk_free_rate=r,
        volatility=sigma,
    )

    print("\nCalculating...")

    bsm_price_call = None
    mc_price_call = None
    bsm_price_put = None
    mc_price_put = None

    if option_type in ("call", "all"):
        bsm_price_call = model.bsm_call_price()
        mc_price_call = model.monte_carlo_call_price(num_simulations)

    if option_type in ("put", "all"):
        bsm_price_put = model.bsm_put_price()
        mc_price_put = model.monte_carlo_put_price(num_simulations)

    print("\n--- Results ---")
    if bsm_price_call is not None:
        print(f"Black-Scholes Call Price: {bsm_price_call:.5f}")

    if mc_price_call is not None:
        print(f"Monte Carlo Call Price: {mc_price_call:.5f}")

    if bsm_price_put is not None:
        print(f"Black-Scholes Put Price: {bsm_price_put:.5f}")

    if mc_price_put is not None:
        print(f"Monte Carlo Put Price: {mc_price_put:.5f}")


if __name__ == "__main__":
    main()
