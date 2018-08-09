import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import NullFormatter

from flip_coin import sample_from_finite_probability_space

theta = np.linspace(0.001, 0.999, num=200)


def gen_observeration_data(prob, num=20):
    return [sample_from_finite_probability_space({'heads': prob, 'tails': 1 - prob}) for i in range(num)]


def computer_max_likelihood(param_space, observer_list):
    jointlogsum = np.vectorize(lambda p: np.sum(
        [np.log(p) if i == 'heads' else np.log(1-p) for i in observer_list]))
    max_id = np.argmax(jointlogsum(param_space))
    return (max_id, param_space[max_id], jointlogsum(param_space))


def main():
    prob_r = np.random.rand()
    data = gen_observeration_data(prob_r)
    _, peak, dist = computer_max_likelihood(theta, data)

    plt.plot(theta, np.exp(dist), 'c--', label="inference")
    plt.plot([prob_r], [max(np.exp(dist))], 'ro', label="inference")
    plt.plot([peak], [max(np.exp(dist))], 'kx', label="inference")

    plt.legend(('prob', "Origin:%f" % prob_r, "ML:%f" % peak),
               loc='best')
    plt.title("max likelihood inference with %d observed object" % len(theta))
    plt.xscale('linear')
    plt.grid(True)
    plt.yscale('symlog', linthreshy=0.000001)
    plt.show()


if __name__ == '__main__':
    main()
