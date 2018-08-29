import numpy as np
import matplotlib.pyplot as plt

data = np.array([[0,0,0],
        [0,0,1],
        [0,1,1],
        [1,1,1]])

alphabet = (0,1)

def node_empirical(d):
    nodes = np.zeros((3,2))
    for i in xrange(len(alphabet)):
        v = alphabet[i]
        for j in xrange(d.shape[1]):
            nodes[j,i] = np.sum(data[:,j] == v)

    return nodes

def pairwise_empirical(d, q = 0.5, leader = 0, leader_space = {0:0.5,1:0.5}):

    likelihood = np.empty_like(d,dtype = np.float)
    for i in xrange(d.shape[1]):
        if i == leader:
            likelihood[:,i] = map(lambda x:leader_space[x], d[:,i])
        else:
            likelihood[:, i] = map(lambda x: q if x else 1 - q, d[:, i] == d[:, leader])

    log_likelihood = np.sum(np.log(likelihood))
    return log_likelihood


def main():
    log_ratio = []
    for i in xrange(data.shape[1]):
        log_ratio.append(pairwise_empirical(data, leader = i, q = 0.8))
    print("ration is:")
    print(log_ratio)
    print("max estimation leader is %d"%np.argmax(log_ratio))

    fig, ax = plt.subplots()

    q_axis = np.linspace(0,1,100)
    y0_axis = [pairwise_empirical(data, q=x, leader = 0) for x in q_axis]
    y1_axis = [pairwise_empirical(data, q=x, leader = 1) for x in q_axis]
    y2_axis = [pairwise_empirical(data, q=x, leader = 2) for x in q_axis]
    ax.plot(q_axis, y0_axis, 'r+', label='red')
    ax.plot(q_axis, y1_axis, 'g--', label='green')
    ax.plot(q_axis, y2_axis, 'b--', label='blue')
    ax.annotate('q = %.3f'%q_axis[np.argmax(y0_axis)], xy=(q_axis[np.argmax(y0_axis)], np.max(y0_axis)), xytext=(0.5, -11),
            arrowprops=dict(facecolor='black', shrink=0.001),
            horizontalalignment='right',
            verticalalignment='bottom',
            )
    ax.annotate('q = %.3f'%q_axis[np.argmax(y1_axis)], xy=(q_axis[np.argmax(y1_axis)], np.max(y1_axis)), xytext=(1, -5),
            arrowprops=dict(facecolor='black', shrink=0.001),
            horizontalalignment='right',
            verticalalignment='top',
            )
    # ax.axvline(x=q_axis[np.argmax(y0_axis)],color='#d62728',alpha = 0.5)
    # ax.axvline(x=q_axis[np.argmax(y1_axis)],color='#2ca02c',alpha = 0.5)
    ax.axvspan(0.5, 1, facecolor='0.5', alpha=0.3)


    ax.set_ylim(-30, -5)

    plt.show()

    

if __name__ == '__main__':
    main()