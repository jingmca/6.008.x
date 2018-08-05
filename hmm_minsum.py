import numpy as np

class HMM(object):
    
    def __init__(self, trans_prob, init_prob, observer_prob, observer_val):
        self.trans = trans_prob
        self.init = init_prob
        self.observer = observer_prob
        self.y = observer_val
        self.map_x = np.zeros(len(observer_val))
        self.trace_max = np.zeros((len(observer_val) - 1, len(init_prob)))

        self.minsum_table = np.zeros((len(observer_val) - 1, len(init_prob)))
        self.joint_dist = np.array(self.__compute_phi(), dtype = np.float)  

    def __compute_phi(self):
        phi_x = [self.observer[:,i] for i in self.y]
        phi_x[0] = self.init * phi_x[0]

        return phi_x

    def __trace_point(self, trans, vec, mode = 1):
        mat = np.multiply(trans, vec)
        if mode == 2:
            return np.max(mat, axis = 1)

        return np.argmax(mat, axis = 1)

    def forward_message(self, from_state, to_state):
        st = np.ones_like(self.init, dtype=np.float)

        if to_state > len(self.y) - 1:
            print("M%d->%d is over the upper bound"%(from_state, to_state))
            to_state = len(self.y) - 1
        if from_state < 0:
            from_state = 0
            
        if to_state - from_state != 1:
            print("M%d->%d is wrong toward"%(from_state, to_state))
        elif to_state == 1 and from_state == 0:
            st *= self.trans.dot(self.joint_dist[0])
            self.trace_max[0] = self.__trace_point(self.trans, self.joint_dist[0])
            
            print("M1->2 = ",st / np.sum(st))
        else:
            other = self.forward_message(from_state - 1, from_state)
            gamma = self.joint_dist[from_state] * other
            st = self.trans.dot(gamma)
            # in max-product algorithms, message func is a max-value func from last iter . its different from sum-product algo!
            other2 = self.__trace_point(self.trans, self.joint_dist[from_state - 1], mode = 2)
            self.trace_max[from_state] = self.__trace_point(self.trans, self.joint_dist[from_state] * other2)

            print("M%d->%d = "%(from_state+1, to_state+1),st / np.sum(st))
        return st / np.sum(st)
        
    def backward_message(self, from_state, to_state):
        backward_trans = self.trans.T
        st = np.ones_like(self.init)
        message_most_right_left = backward_trans.dot(self.joint_dist[len(self.y) - 1])
        
        if from_state - to_state != 1:
            print("B%d->%d is wrong tos"%(from_state, to_state))
        elif from_state == len(self.y) - 1 and to_state == from_state - 1:
            st *= message_most_right_left
        else:
            st = backward_trans.dot(self.joint_dist[from_state] * self.backward_message(from_state + 1, from_state))
        
        print("B%d->%d = "%(from_state+1, to_state+1), st/ np.sum(st))
        return st
        
    def computer_postior(self, state_indice):
        if state_indice == 0:
            prob = self.joint_dist[state_indice] * self.backward_message(1,0)
        elif state_indice == len(self.y) - 1:
            prob = self.joint_dist[state_indice] * self.forward_message(state_indice - 1, state_indice)
        else:
            prob = self.joint_dist[state_indice] * self.forward_message(state_indice - 1, state_indice) * self.backward_message(state_indice + 1, state_indice)
        print("state X%d max at [%d] postior distribution :"%(state_indice + 1, np.argmax(prob)), prob / np.sum([prob]))
        return prob
         
    def computer_max_prob(self):
        for k in range(len(self.y) - 1, -1, -1):
            self.map_x[k] = np.argmax(self.computer_postior(k))

    def minsum(self):
        _min_table = np.zeros_like(self.minsum_table, dtype=np.float)
        for node in range(len(self.y) - 1):
            if node == 0:
                self.minsum_table[node] =  np.argmin(-np.log2(self.trans) - np.log2(self.joint_dist[node]), axis = 1)
                _min_table[node] = np.min(-np.log2(self.trans) - np.log2(self.joint_dist[node]), axis = 1)
            else:
                self.minsum_table[node] = np.argmin(-np.log2(self.trans) - np.log2(self.joint_dist[node]) + _min_table[node - 1], axis = 1)
                _min_table[node] = np.min(-np.log2(self.trans) - np.log2(self.joint_dist[node]) + _min_table[node - 1], axis = 1)

        map_k = np.zeros(len(self.y))

        map_k[len(self.y) - 1] = np.argmin(_min_table[-1] - np.log2(self.joint_dist[len(self.y) - 1]))
        for k in range(len(_min_table) - 1 , -1, -1):
            # print(int(map_k[k+1]))
            map_k[k] = self.minsum_table[k, int(map_k[k+1])]

        return map_k

trans_prob = np.array([[.75, .25],
                       [.25, .75]])
x_prior_prob = np.array([.5, .5])
joint_observer = [{'H':.5,'T':.5}, {'H':.25,'T':.75}]
y = ['H','H','T','T','T']
print("joint observer is :", joint_observer)

joint_observer_prob = [zip(*i.items())[1] for i in joint_observer]
print(joint_observer_prob)

print(trans_prob,trans_prob.T)

def main():
    h = HMM(trans_prob, x_prior_prob, np.array(joint_observer_prob, dtype = np.float), [0,0,1,1,1])
    h.computer_max_prob()
    print("....")
    print("MAP ESMATE with 3 differnt algorithms:")
    print("ESMATE with max-product :", h.trace_max)
    print("ESMATE with max-marginal :", h.map_x)
    print("ESMATE with min-sum :", h.minsum())

"""
code for Week 6: Special Case - Marginalization in Hidden Markov Models
"""
def robot_loc():
    A = np.array([[0.25, .75, 0.1],
                [0.1, .25, .75],
                [0.1, 0.1, 1.0]])
    B = np.array([[1.,0.1],
                [0.1,1.],
                [1.,0.1]])
    C = np.array([1./3, 1./3, 1./3], dtype = np.float)

    r = HMM(A.T, C, B, [0,1,0])
    # r.forward_message(0,1)
    # r.forward_message(1,2)
    # r.backward_message(2,1)
    # r.backward_message(1,0)
    # r.computer_postior(1)

    r.computer_max_prob()
    print(r.map_x)
    print(r.minsum())
    
if __name__ == '__main__':
    main()
    #robot_loc()
