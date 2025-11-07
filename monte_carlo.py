import numpy as np


def monte_carlo_pi(n):
    samples = np.random.uniform(low=0, high=1, size=(n, 2))
    pi = 4 * np.mean(samples[:, 0] ** 2 + samples[:, 1] ** 2 <= 1)
    return pi


def ex2(n):
    samples = np.random.uniform(low=0, high=1, size=n)
    return np.mean(samples**2)


def cdfx(n):
    x_val = np.random.uniform(0, 1, n)
    return np.mean(np.exp(-(x_val**2)))


def main():
    n = 100000
    pi_estimate = monte_carlo_pi(n)
    print(pi_estimate)

    size = 10
    while True:
        ex2_estimate = ex2(n)
        print(ex2_estimate)
        size *= 10
        if (ex2_estimate - (1 / 3)) < 1e-10:
            print("Converged")
            break
    cdfval = cdfx(n)
    print(cdfval)


if __name__ == "__main__":
    main()
