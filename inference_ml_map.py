#-*-encoding:utf8-*-
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import NullFormatter
from scipy.special import logsumexp
from flip_coin import sample_from_finite_probability_space

theta = np.linspace(0.00001, 0.99999, num=10000)


def gen_observeration_data(prob, num=50):
    return [sample_from_finite_probability_space({'heads': prob, 'tails': 1 - prob}) for i in range(num)]


def computer_max_likelihood(param_space, observer_list):
    jointlogsum = np.vectorize(lambda p: np.sum(
        [np.log(p) if i == 'heads' else np.log(1-p) for i in observer_list]))
    max_id = np.argmax(jointlogsum(param_space))
    return (max_id, param_space[max_id], jointlogsum(param_space))

def prior_distribution(prob, heade_order = 1, tail_order = 1):
    # _formula = "θ^%d * (1 - θ)^%d"%(heade_order, tail_order)
    _func = np.vectorize(lambda prob :heade_order * np.log(prob) + tail_order * np.log(11-  prob))
    return _func(prob)


def main():
    prob_r = np.random.rand()
    data = gen_observeration_data(prob_r)
    _, peak, log_dist = computer_max_likelihood(theta, data)
    dist = log_dist - logsumexp(log_dist)

    log_dist_map_h1t1 = (dist + prior_distribution(theta)) -  logsumexp(dist + prior_distribution(theta))
    dist_h1t1 = np.exp(log_dist_map_h1t1)
    peak_h1t1 = theta[np.argmax(dist_h1t1)]

    log_dist_map_h10t30 = (dist + prior_distribution(theta, 10, 30)) -  logsumexp(dist + prior_distribution(theta, 10, 30))
    dist_h10t30 = np.exp(log_dist_map_h10t30)
    peak_h10t30 = theta[np.argmax(log_dist_map_h10t30)]

    plt.plot(theta, np.exp(dist), 'c--', label="inference")
    plt.plot(theta, dist_h1t1, 'b--')
    plt.plot(theta, dist_h10t30, 'y--')

    plt.plot([prob_r], [max(np.exp(dist))], 'ro', label="inference")
    plt.plot([peak], [max(np.exp(dist))], 'cx', label="inference")
    plt.plot([peak_h1t1], [max(dist_h1t1)], 'bx', label="inference")
    plt.plot([peak_h10t30], [max(dist_h10t30)], 'yx', label="inference")

    plt.legend(('max likelihood',u"map1 θ*(1-θ)",u"map2 θ^10*(1-θ)^30", u"θtrue:%f" % prob_r, u"θml:%f" % peak, u"θmap1:%f"%peak_h1t1, u"θmap2:%f"%peak_h10t30),
               loc='best')
    plt.title("max likelihood inference")
    plt.xscale('linear')
    plt.grid(True)
    plt.yscale('symlog', linthreshy=0.000001)
    plt.show()


if __name__ == '__main__':
    main()
