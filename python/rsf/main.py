import numpy as np

Z = 25
delta = 0.01

tspan = int(Z/delta)

field = np.genfromtxt("field.csv", delimiter=",")

id = field[:,0]
p_value = field[:,1]
gamma = field[:,2]

init = np.array([50, 25, 25, 75, 125, 50, 100, 150, 125, 250, 125, 250, 100, 125, 175, 50, 125, 50, 50, 25, 50, 100, 100, 100, 100])
scores = np.array([])

init_score = np.sum(p_value*(1-np.exp(-gamma*(init*delta))))

print(init_score)

for n in range(init.size-1):
    if init[n] != 0:
        init[n] = init[n]-1
        for i in range(init.size-1):
            if i != n:
                init[i] = init[i]+1
                score = np.sum(p_value*(1-np.exp(-gamma*(init*delta))))
                scores = np.append(scores, score)
                init[i] = init[i]-1
    
        init[n] = init[n]+1

print(np.max(scores))