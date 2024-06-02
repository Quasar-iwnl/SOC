import json
import numpy as np
import matplotlib.pyplot as plt
import scipy

def inv_transform(distribution: str, num_samples: int, **kwargs) -> list:
    """ populate the 'samples' list from the desired distribution """

    samples = []

    # TODO: first generate random numbers from the uniform distribution
    uniform = np.random.uniform(0, 1, num_samples)
    # END TODO
    if distribution == 'cauchy':
        peak_x = kwargs.get('peak_x', 0)
        gamma = kwargs.get('gamma', 1)
        print(gamma, peak_x)
        samples = inverse_cauchy(uniform, peak_x, gamma)
        samples = np.around(samples, decimals=4)

    elif distribution == 'exponential':
        l = kwargs.get('lambda', 1)
        samples = inverse_exp(uniform, l)
        samples = np.around(samples, decimals=4)

    samples = list(samples)
    return samples

def inverse_exp(p, l):
    return -np.log(1 - p) / l

def inverse_cauchy(p, peak_x, gamma):
    return peak_x + gamma*np.tan(np.pi*(p-0.5))


if __name__ == "__main__":
    np.random.seed(42)

    for distribution in ["cauchy", "exponential"]:
        file_name = "q1_" + distribution + ".json"
        args = json.load(open(file_name, "r"))
        samples = inv_transform(**args)
        with open("q1_output_" + distribution + ".json", "w") as file:
            json.dump(samples, file)

        # TODO: plot and save the histogram to "q1_" + distribution + ".png"
        plt.hist(samples, bins=50, density=True, alpha=0.6, color='b')
        plt.savefig("q1_" + distribution + ".png")
        plt.close()
        # END TODO
