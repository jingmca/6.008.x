from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
from scipy.special import comb, perm

def calc_entropy(prob):
    pairs = list(prob.items())
    outcomes, outcomes_prob = zip(*pairs)
    return -np.dot(outcomes_prob,np.log2(outcomes_prob))

print(calc_entropy({1:999999/1000000, 2:1/1000000}))

joint_prob_XY = np.array([[0.10, 0.09, 0.11], [0.08, 0.07, 0.07], [0.18, 0.13, 0.17]])
prob_X = joint_prob_XY.sum(axis=1)
prob_Y = joint_prob_XY.sum(axis=0)
joint_prob_XY_indep = np.outer(prob_X, prob_Y)

print(np.sum(np.log2(joint_prob_XY / joint_prob_XY_indep) * joint_prob_XY))

base = (sum([comb(x,1)*0.2*((0.8)**(x-1)) for x in range(1,5)]))
upper = [x * comb(x,1)*0.2*(0.8 ** (x - 1)) / (base) for x in range(1,5)]
print(sum(upper))