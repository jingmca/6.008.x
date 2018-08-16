import numpy as np
from scipy.stats import entropy

sample_dist = {'s1':0.3,'s2':0.15,'s3':0.3}
sample_prob = np.array(sample_dist.values())
sample_prob /= np.sum(sample_prob)

sample_entropy = -np.dot(np.log(sample_prob), sample_prob)

infer_prob = np.array([0.85,0.1,0.6])
infer_prob /= np.sum(infer_prob)
# print(infer_prob)

cross_entropy = -np.dot(np.log(infer_prob), sample_prob)
relative_entropy = np.dot(np.log(sample_prob / infer_prob), sample_prob)

eq = np.abs(sample_entropy + relative_entropy - cross_entropy) < 1e-15
print("1.sample entropy :%f, KL_divergence :%f, cross entropy: %f, eq is %d\n"%(sample_entropy, relative_entropy, cross_entropy, eq))
print("2.sample entropy :%f, KL_divergence :%f, cross entropy: %f, eq is %d"%(entropy(sample_prob), entropy(sample_prob, infer_prob), sample_entropy + relative_entropy, eq))
