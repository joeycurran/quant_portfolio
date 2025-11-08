import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()


def gbm_paths(s_0, sigma, r, T, n_steps, n_paths):
    dt = T / n_steps
    dW = rng.normal(0, np.sqrt(dt), size=(n_paths, n_steps))
    W = np.cumsum(dW, axis=1)
    t = np.linspace(0, T, n_steps)
    S = s_0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)
    return t, S  # shape (paths, steps)


def euro_call_price(stock_data, K, r, T):
    # want the data for today so must apply disc factor
    S_T = stock_data[:, -1]  # grab last price from every path at t=T
    payoffs = np.maximum(S_T - K, 0)
    discounted_payoffs = np.exp(-r * T) * payoffs  # discount back to t=0
    price = np.mean(discounted_payoffs)  # Monte Carlo expected value
    return price


def plot_mean_vs_analytical(T, S, s0, r, n_show=20):
    n_paths, n_steps = S.shape
    t = np.linspace(0, T, n_steps)

    mean_path = S.mean(axis=0)
    std_path = S.std(axis=0)
    analytical_st = s0 * np.exp(r * t)

    # Error between analytical and Monte Carlo mean
    errors = analytical_st - mean_path

    fig, axes = plt.subplots(
        3, 1, figsize=(10, 10), sharex=True, gridspec_kw={"height_ratios": [2, 1, 0.8]}
    )

    for i in range(min(n_show, n_paths)):
        axes[0].plot(t, S[i], lw=0.8, alpha=0.6)
    axes[0].set_title(f"{n_show} Random GBM Paths")
    axes[0].set_ylabel("Stock Price $S_t$")
    axes[0].grid(alpha=0.3)

    axes[1].plot(t, mean_path, color="black", lw=2, label="Monte Carlo Mean Path")
    axes[1].plot(t, analytical_st, "r--", lw=2, label="Analytical $E[S_t]=S_0 e^{rt}$")

    axes[1].set_title("Monte Carlo Mean vs Analytical Expectation")
    axes[1].set_ylabel("Stock Price $S_t$")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].plot(
        t, errors, color="red", lw=2, label="Error = Analytical - Monte Carlo mean"
    )
    axes[2].axhline(0, color="black", linestyle="--", lw=1)
    axes[2].set_xlabel("Time (years)")
    axes[2].set_ylabel("Error ($)")
    axes[2].plot(t, np.mean(errors) * np.ones_like(t), "g--", lw=1, label="Mean Error")
    axes[2].set_title("Average Monte Carlo Error vs Analytical Expectation")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
    plt.close()


def main():
    n_steps, n_paths = 10000, 10000
    r, T, s0, sigma, K = 0.05, 1, 105, 0.2, 100
    t, S = gbm_paths(s0, sigma, r, T, n_steps, n_paths)
    plot_mean_vs_analytical(T, S, s0, r)

    mean_path = S.mean(axis=0)

    call_price = euro_call_price(S, K, r, T)
    print("Monte Carlo Call Price =", call_price)
    print(
        "Analytical vs Monte Carlo Stock Price:", mean_path[-1], s0 * np.exp(r * T)
    )  # should be close to s0*exp(r*T)
    S_T = S[:, -1]
    mc_E_X2 = np.mean(S_T**2)
    theory_E_X2 = s0**2 * np.exp(2 * r * T + sigma**2 * T)
    print("Monte Carlo E[X^2] =", mc_E_X2)
    print("Analytical E[X^2]  =", theory_E_X2)
    variance = mc_E_X2 - mean_path[-1] ** 2
    print("Monte Carlo Variance =", variance)
    print("Analytical Variance  =", theory_E_X2 - (s0 * np.exp(r * T)) ** 2)
    plot_error(T, S, s0, r, mean_path=mean_path)
    return


if __name__ == "__main__":
    main()
