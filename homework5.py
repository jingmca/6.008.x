import numpy as np
import sympy as sym
joint_table = np.array([[0.,1.],
                        [1.,0.]])

p = 0.8

m42 = joint_table.dot(np.array([p, 1-p]))
m42_blue = m42[0]

m52_blue = m42_blue

m31_blue = m42_blue
m31 = np.array([0.4,0.6])

m12 = joint_table.dot([1,1] * m31)

print(m42,m52_blue,m31,m12)

p2 = m42*m42*m12*[1,1]
print(p2 / sum(p2))