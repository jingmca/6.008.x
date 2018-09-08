# 6.008.1x
('joint observer is :', [{'H': 0.5, 'T': 0.5}, {'H': 0.25, 'T': 0.75}])  

[(0.5, 0.5), (0.25, 0.75)]  

(array([[0.75, 0.25],  
       [0.25, 0.75]]), array([[0.75, 0.25],  
       [0.25, 0.75]]))  

('M1->2 = ', array([0.58333333, 0.41666667]))  
('M2->3 = ', array([0.61842105, 0.38157895]))  
('M3->4 = ', array([0.50966851, 0.49033149]))  
('M4->5 = ', array([0.4546589, 0.5453411]))  
('state X5 max at [1] postior distribution :', array([0.35724792, 0.64275208]))  

('M1->2 = ', array([0.58333333, 0.41666667]))  
('M2->3 = ', array([0.61842105, 0.38157895]))  
('M3->4 = ', array([0.50966851, 0.49033149]))  
('B5->4 = ', array([0.45, 0.55]))  
('state X4 max at [1] postior distribution :', array([0.36182383, 0.63817617]))  

('M1->2 = ', array([0.58333333, 0.41666667]))  
('M2->3 = ', array([0.61842105, 0.38157895]))  
('B5->4 = ', array([0.45, 0.55]))  
('B4->3 = ', array([0.42647059, 0.57352941]))  
('state X3 max at [1] postior distribution :', array([0.44549763, 0.55450237]))  

('M1->2 = ', array([0.58333333, 0.41666667]))  
('B5->4 = ', array([0.45, 0.55]))  
('B4->3 = ', array([0.42647059, 0.57352941]))  
('B3->2 = ', array([0.41571429, 0.58428571]))  
('state X2 max at [0] postior distribution :', array([0.66579506, 0.33420494]))  

('B5->4 = ', array([0.45, 0.55]))  
('B4->3 = ', array([0.42647059, 0.57352941]))  
('B3->2 = ', array([0.41571429, 0.58428571]))  
('B2->1 = ', array([0.54364279, 0.45635721]))  
('state X1 max at [0] postior distribution :', array([0.70436346, 0.29563654]))  

.... 

MAP ESMATE with 3 differnt algorithms:  

('ESMATE with max-product :', array([[0., 1.],
       [0., 0.],
       [0., 1.],
       [0., 1.]]))  

('ESMATE with max-marginal :', array([0., 0., 1., 1., 1.]))  

('ESMATE with min-sum :', array([0., 0., 1., 1., 1.]))  

连续扔两枚硬币,一枚均匀,一枚反面重
emission_prob: {'biased': {'head': 0.25, 'tail': 0.75}, 'fair': {'head': 0.5, 'tail': 0.5}}
states: ('fair', 'biased')
start: {'biased': 0.5, 'fair': 0.5}
transition_prob: {'biased': {'biased': 0.75, 'fair': 0.25}, 'fair': {'biased': 0.25, 'fair': 0.75}}
output: <listreverseiterator object at 0x10fec04d0>
observ: ('head', 'head', 'tail', 'tail', 'tail')
MAP Estination:
fair->fair->biased->biased->biased
===========================================
医生连续三天给一个人看病,根据现象判断三天的病情
emission_prob: {'Healthy': {'cold': 0.4, 'dizzy': 0.1, 'normal': 0.5}, 'Fever': {'cold': 0.3, 'dizzy': 0.6, 'normal': 0.1}}
states: ('Healthy', 'Fever')
start: {'Healthy': 0.6, 'Fever': 0.4}
transition_prob: {'Healthy': {'Healthy': 0.7, 'Fever': 0.25}, 'Fever': {'Healthy': 0.4, 'Fever': 0.6}}
output: <listreverseiterator object at 0x10f37cf90>
observ: ('normal', 'cold', 'dizzy')
MAP Estination:
Healthy->Healthy->Fever
