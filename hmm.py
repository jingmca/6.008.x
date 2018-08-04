import numpy as np
# this is an example of matrix vector multiplication, shown first in pure python with dictionaries
# and shown second with the matrix vector multiplication equivalent

# The structure is of a markov chain.  The way to think about this is, Today it is sunny for sure (see line 19).  
# Per line 13, we know on a day that is sunny, there is a 20% chance the next day is sunny, 
# a 25% chance the next day is cloudy, and 55% chance the next day is rainy
# we have similar information for next day expectation if today were to be cloudy, and also if today was rainy
# each day there is new weather.  And we learn new information and update our beliefs every morning at sunrise.  

total_days_in_future_to_estimate = 4 # this can be changed to any natural number
destination_weather = ['sunny', 'cloudy', 'rainy']
master_mini_tree_state_to_traverse = {'cloudy': [0.4, 0.1, 0.5], 'sunny' :[0.2, 0.25, 0.55], 'rainy': [0.7, 0.1, 0.2]}
# note the above VALUES in the mini_tree dict are all ordered like in destination_weather: ['sunny', 'cloudy', 'rainy']
# For the avoidance of doubt, we could state instead use
# master_mini_tree_state_to_traverse = {'sunny' :[0.2, 0.25, 0.55], 'cloudy': [0.4, 0.1, 0.5], 'rainy': [0.7, 0.1, 0.2]}
# However, the KEYS in Python dictionaries are unordered, so line 16 and line 13 are in fact identical 

original_prior_distribution = {'sunny': 1, 'cloudy': 0, 'rainy': 0}

prior_distribution = original_prior_distribution.copy() 

# repeated matrix vector multiplication shown below
for _ in range(total_days_in_future_to_estimate):
    post_distribution = {'sunny': 0, 'cloudy': 0, 'rainy': 0} # post is short for posterior
    for weather_key in prior_distribution:
        for marginal_prob, destination in zip(master_mini_tree_state_to_traverse.get(weather_key), destination_weather):
            post_distribution[destination] += marginal_prob * prior_distribution.get(weather_key) 
            # notice the use of += 
            # this is where the 'recombining' of the tree occurs
    prior_distribution = post_distribution
# the above process has a very nice picture interpretation.  It is worth drawing it out for 4 iterations.

print("now printing weather probabilities, calculated using recombining trees")    

for item in destination_weather:
    print(item + ":", post_distribution.get(item))

print("\nOnward to the matrix vector equivalent")

# the matrix vector equivalent is below

print("by convention I tend to use the form of Ax = b")
print("Note each column sums to == 1 -- because each has a valid probability distribution")

A = np.zeros((3,3))
x = np.zeros(3)

for j, dest in enumerate(destination_weather):
    x[j] = original_prior_distribution.get(dest) # this grabs a prior probability equal to one for sunny
    for i, probability in enumerate(master_mini_tree_state_to_traverse.get(dest)):
        A[i,j] = probability

print("this is our prior distribution, x (which is a column vector in Linear Algebra terms -- though numpy doesn't care)")
print( x, "\n")
print("this is our transition matrix, which has taken info from the master_mini_tree_state_to_traverse and placed it in a matrix ")
print(A)

# matrix vector produc, shown below
for _ in range(total_days_in_future_to_estimate):
    b = np.dot(A, x)
    x = b
    print(b)

print(" ")
print("posterior distribution:")
print(b)

# the above for loop is equivalent to writing A @ A @ ... A @ x, where we show A n times, and n = total_days_in_future_to_estimate

print("\n#####################################################################" )
print("notice how the probabilities are identical (setting aside floating point nuances) in vector b ")
print("with what we originally printed at the top \n")
print("the only key difference between this and an HMM is we update it HMM with likelihood functions")
print("between daily state transitions --- AND")

print("we also run it forward and backward to make use of available information and avoid having inconsistent beliefs")


print("\nThe thing to notice is how on line 28 with post_distribution[destination]")
print("we explicitly did the recombining of the tree")
print("but with matrix vector multiplication, that -- roughly speaking-- happens automatically")
print("the easiest way to understand the viterbi alrogithm is that it doesn't let the recombination happen")
print("instead it just grabs the 'best' branches at each stage")