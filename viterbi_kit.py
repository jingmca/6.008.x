#encoding:utf-8
import numpy as np


class Viterbi(object):

    def __init__(self, state_space, transition_prob, emission_prob, start_prob):
        self.states = state_space
        self.transition_prob = transition_prob
        self.emission_prob = emission_prob
        self.start = start_prob
        self.output = None
        self.observ = None

    def __str__(self):
        return "\n".join(([i + ": " + str(self.__dict__[i]) for i in self.__dict__]))

    def estimate(self, observations):
        self.observ = observations
        _trans = self.__compute_pairwise_table()
        transition = []
        messages = []

        for i in xrange(len(self.observ)):
            _step = self.__compute_potential_step(i)
            if i == 0:
                _message = _step + _trans
            else:
                _message = _step + _trans + messages[i - 1]
            messages.append(np.min(_message, axis=1))
            _path = np.argmin(_message, axis=1)

            if i < len(self.observ) - 1:
                _link = dict([(self.states[post],  self.states[pri]) for post, pri in enumerate(_path)])
                transition.append(_link)

        end_state = self.states[np.argmin(messages[-1])]
        self.output = [end_state]
        # print("Finally State Estimation is: '%s'" % end_state)

        for path in reversed(transition):
            end_state = path[end_state]
            self.output.append(end_state)

        self.output = reversed(self.output)
        return self.output

    def __compute_potential_step(self, step):
        if step == 0:
            return -np.log2([self.start[i] * self.emission_prob[i][self.observ[0]] for i in self.states])
        return -np.log2([self.emission_prob[i][self.observ[step]] for i in self.states])

    def __compute_pairwise_table(self):
        _trans = np.zeros((len(self.states), len(self.states)))
        for j, v in self.transition_prob.items():
            colu = self.states.index(j)
            for i, p in v.items():
                row = self.states.index(i)
                _trans[row, colu] = p
        return -np.log2(_trans)


def problem_coin():
    states = ('fair', 'biased')
    trans = {'fair': {'fair': .75, 'biased': .25}, 'biased': {'fair': .25, 'biased': .75}}
    emiss = {'fair': {'head': .5, 'tail': .5}, 'biased': {'head': .25, 'tail': .75}}
    start = {'fair': 0.5, 'biased': 0.5}

    v = Viterbi(states, trans, emiss, start)
    output = v.estimate(("head", "head", "tail", "tail", "tail"))
    print(v)
    print("MAP Estination:")
    print("->".join(output))

def problem_health():
    states = ('Healthy', 'Fever')
    trans = {'Healthy': {'Healthy': .7, 'Fever': .25}, 'Fever': {'Healthy': .4, 'Fever': .6}}
    emiss = {'Healthy': {'normal': .5, 'cold': .4, 'dizzy':.1}, 'Fever': {'normal': .1, 'cold': .3, 'dizzy':.6}}
    start = {'Healthy': 0.6, 'Fever': 0.4}

    v = Viterbi(states, trans, emiss, start)
    output = v.estimate(("normal", "cold", "dizzy"))
    print(v)
    print("MAP Estination:")
    print("->".join(output))


if __name__ == '__main__':
    print("连续扔两枚硬币,一枚均匀,一枚反面重")
    problem_coin()
    print("===========================================")
    print("医生连续三天给一个人看病,根据现象判断三天的病情")
    problem_health()
