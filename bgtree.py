import numpy as np

joint_blue_green_prob = np.array([[0.2,0.8],
                                  [0.8,0.2]])
                                  
#define phi struct with [blue,green]
phi4 = [1,0]
phi3 = phi5 = [0,1]
phi1 = phi2 = [1,1]

m42 = joint_blue_green_prob.dot(phi4)
print("M4->2 message :", m42, "blue = ", m42[0])
m31 = joint_blue_green_prob.dot(phi3)
print("M3->1 message :", m31, "blue = ", m31[0])

class Phi (object):
    
    def __init__(self,prob, parent = [], child = []):
        self.phi = prob
        self.parent = parent
        self.child = child
        

x4 = Phi(phi4)
x3 = Phi(phi3)
x5 = Phi(phi5)
x2 = Phi(phi2, child = [x4, x5])
x1 = Phi(phi1, child = [x2, x3])
x3.parent = x1
x2.parent = x1
x4.parent = x2
x5.parent = x2

print(x1,x2,x3)        
    
m52 = joint_blue_green_prob.dot(phi5)
print("M5->2 message:", m52, "blue = ", m52[0])
m12 = joint_blue_green_prob.dot(phi1 * m31)
print("M2->1 message:", m12, "blue =", m12[0])

unormalized_x2 = phi2 * m12 * m42 * m52
print("unormalize x2 prob is :", unormalized_x2, "blue = ", unormalized_x2[0] / sum(unormalized_x2))

def compute_message(froma, tob):
    belife = np.array([1.0,1.0])
    
    if froma is None:
        return belife
        
    if tob == froma.parent:
        print("parent")
        for c in froma.child:
            belife *= compute_message(c, froma)
    
    elif tob in froma.child:
        print("child")
        belife *= compute_message(froma.parent, froma)
        for c in froma.child:
            if to != c:
                belife *= compute_message(c, froma)
    print("aa,",froma.phi)
    
    aa = froma.phi
    
    belife *= aa
    belife = joint_blue_green_prob.dot(belife)
        
    return belife
    
print(compute_message(x4,x2))
