import numpy as np
import matplotlib.pyplot as plt


def monte_carlo_pi(sample_sizes):
    convergence_array_pi = []
    errors = []

    for n in sample_sizes:
        samples = np.random.uniform(low=0, high=1, size=(n, 2))
        pi = 4 * np.mean(samples[:, 0] ** 2 + samples[:, 1] ** 2 <= 1)
        convergence_array_pi.append(pi)
        errors.append(np.abs(pi - np.pi))

    return convergence_array_pi, errors


def ex2(sample_sizes):
    convergence_array_ex2 = []
    errors = []

    for n in sample_sizes:
        samples = np.random.uniform(low=0, high=1, size=n)
        convergence_array_ex2.append(np.mean(samples**2))
        errors.append(np.abs(np.mean(samples**2) - (1 / 3)))
    return convergence_array_ex2, errors


def cdfx(n):
    x_val = np.random.uniform(0, 1, n)
    return np.mean(np.exp(-(x_val**2)))


def plot_convergence_and_error(
    sample_sizes, estimates, errors, true_value, name, ylim=None
):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(sample_sizes, estimates, marker="o", label=f"Estimated {name}")
    axes[0].axhline(y=true_value, color="r", linestyle="--", label=f"True {name}")
    axes[0].set_xscale("log")
    axes[0].set_title(f"{name} Estimation Convergence")
    axes[0].set_xlabel("Number of Samples (log scale)")
    axes[0].set_ylabel(f"Estimated {name} Value")
    if ylim:
        axes[0].set_ylim(ylim)
    axes[0].legend()

    axes[1].plot(
        sample_sizes, errors, marker="o", label=f"|Estimated {name} - True {name}|"
    )
    ref = errors[0] * np.sqrt(sample_sizes[0]) / np.sqrt(sample_sizes)
    axes[1].plot(sample_sizes, ref, "--", label="~ 1/√n")
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_title(f"{name} Error Scaling")
    axes[1].set_xlabel("Number of Samples (log scale)")
    axes[1].set_ylabel("Absolute Error (log scale)")
    axes[1].legend()

    plt.tight_layout()
    plt.show()
    plt.close()


def main():
    sample_sizes = np.logspace(2, 7, 40, dtype=int)
    pi_estimate_array, pi_errors = monte_carlo_pi(sample_sizes)
    print(pi_estimate_array[-1])
    ex2_estimate_array, ex2_errors = ex2(sample_sizes)
    cdfval = cdfx(n=10000)
    print(cdfval)

    plot_convergence_and_error(
        sample_sizes, pi_estimate_array, pi_errors, np.pi, "Pi", ylim=(3.0, 3.2)
    )
    plot_convergence_and_error(
        sample_sizes, ex2_estimate_array, ex2_errors, 1 / 3, "1/3", ylim=(0.3, 0.4)
    )


if __name__ == "__main__":
    main()
