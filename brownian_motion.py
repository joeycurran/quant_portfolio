import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=42)


def gbm_path(s_0, sigma, r, T, n_steps):
    dt = T / n_steps
    dW = rng.normal(0, np.sqrt(dt), n_steps)
    W = np.cumsum(dW)

    t = np.linspace(0, T, n_steps)
    S = s_0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)
    return t, S, W


def plot_gbm(s_0, sigma, r, T, n_steps):
    t, S, W = gbm_path(s_0, sigma, r, T, n_steps)

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(np.linspace(0, T, n_steps), W)
    plt.title("Brownian Motion $W_t$")
    plt.xlabel("time")
    plt.ylabel("W_t")

    plt.subplot(1, 2, 2)
    plt.plot(t, S)
    plt.title("Simulated GBM Path $S_t$")
    plt.xlabel("time")
    plt.ylabel("S_t")

    plt.tight_layout()
    plt.show()
    return t, S, W


def main():
    n, r, T, s_0, sigma = 1000, 0.05, 1, 40, 0.08
    t, S, W = plot_gbm(s_0, sigma, r, T, n)
    print(t, S, W)


if __name__ == "__main__":
    main()
