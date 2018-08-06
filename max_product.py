import numpy as np
from graphviz import Digraph

x4 = [1,0]
x5 = [1,2]
x3 = [1,1]

x2 = [1,1]
x1 = [1,1]
x6 = x7 = [1,1]

joint_blue_green_prob = np.array([[0.5,0.5],
                                    [0.25,0.75]])

def trace_back(x_val = [], y_val = None, other = [], Name = '', mode = 1):
    if other != []:
        x_val *= other
        print(x_val)
    tb = np.multiply(joint_blue_green_prob, x_val)
    print("---",Name)
    print("trace matrix:",tb)
    print("---")

    if mode == 2:
        return np.max(tb, axis = 1)

    if y_val != None:
        return np.argmax(tb[y_val])
    else:
        return np.argmax(tb, axis = 1)
  

m42 = joint_blue_green_prob.dot(x4)
tr_table24 = trace_back(x4,Name='x4')

m52 = joint_blue_green_prob.dot(x5)
tr_table25 = trace_back(x5)

m63 = joint_blue_green_prob.dot(x6)
tr_table36 = trace_back(x6,Name='x6')
m73 = joint_blue_green_prob.dot(x7)
tr_table37 = trace_back(x7,Name='x7')

m31 = joint_blue_green_prob.dot(x3 * m63 * m73)
print("M3->1 is :",m31)

# m31_bar = np.diag(joint_blue_green_prob @ x6) @ np.diag(joint_blue_green_prob @ x7) @ x3
# print("M3->1 bar is :",m31_bar)

tr_table13 = trace_back(x3,other =  trace_back(x6, mode=2) * trace_back(x7, mode= 2), Name='x3')

m21 = joint_blue_green_prob.dot(x2 * m42 * m52)
tr_table12 = trace_back(x2,Name='x2', other=trace_back(x4, mode = 2) * trace_back(x5, mode = 2))

prob_x1 = x1 * m21 * m31
max_x1 = np.argmax(prob_x1)
print("x1 prob is",prob_x1,"max prob val: %d"%max_x1)

tri24 = -np.log(x4) - np.log(joint_blue_green_prob)
tri25 = -np.log(x5) - np.log(joint_blue_green_prob)
tri12 = -np.log(x2) - np.log(joint_blue_green_prob) + np.min(tri24, axis=1) + np.min(tri25, axis=1)

max_x2 = np.argmin(tri12[max_x1])
print("x2 ",max_x2,tr_table12[max_x1])
max_x4 = np.argmin(tri24[max_x2])
print("x4 ",max_x4,tr_table24[max_x2])
max_x5 = np.argmin(tri25[max_x2])
print("x5 ",max_x5,tr_table25[max_x2])

tri36 = -np.log(x6) - np.log(joint_blue_green_prob)
tri37 = -np.log(x7) - np.log(joint_blue_green_prob)
tri13 = -np.log(x3) - np.log(joint_blue_green_prob) + np.min(tri36, axis=1) + np.min(tri37, axis=1)

max_x3 = np.argmin(tri13[max_x1])
print("x3 ",max_x3,tr_table13[max_x1])
max_x6 = np.argmin(tri36[max_x3])
print("x6 ",max_x6,tr_table36[max_x3])
max_x7 = np.argmin(tri37[max_x3])
print("x7 ",max_x7,tr_table37[max_x3])


c = lambda x:'wizard' if x == 0 else 'muggle'

dot_after = Digraph(comment='The Round Table')
dot_after.node('1',"X1:"+c(max_x1))
dot_after.node('2',"X2:"+c(max_x2))
dot_after.node('3',"X3:"+c(max_x3))
dot_after.node('4',"X4:"+c(max_x4))
dot_after.node('5',"X5:"+c(max_x5))
dot_after.node('6',"X6:"+c(max_x5))
dot_after.node('7',"X7:"+c(max_x5))

dot_after.edges(['12','13','24','25','36','37'])
dot_after.render('round-table2.jpg', view=True)