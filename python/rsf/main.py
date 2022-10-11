import numpy as np

Z = 25
delta = 0.01
iterations = 3000

tspan = int(Z/delta)

field = np.genfromtxt("field.csv", delimiter=",")

id = field[:,0]
p_value = field[:,1]
gamma = field[:,2]

#init = np.array([50, 20, 20, 75, 125, 50, 100, 150, 125, 250, 125, 250, 100, 125, 175, 50, 125, 50, 50, 25, 50, 100, 100, 100, 100])
init = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100])
scores = np.array([])
n_max = None
i_max = None
c_max = 0

init_score = np.sum(p_value*(1-np.exp(-gamma*(init*delta))))
print(f'Initial score: {init_score}')

for c in range(iterations):
    for n in range(init.size-1):
        if init[n] != 0:
            init[n] = init[n]-1
            for i in range(init.size-1):
                if i != n:
                    init[i] = init[i]+1
                    score = np.sum(p_value*(1-np.exp(-gamma*(init*delta))))
                    scores = np.append(scores, score)
                    if score == np.max(scores):
                        n_max = n
                        i_max = i
                    init[i] = init[i]-1
        
            init[n] = init[n]+1

    if c_max >= np.max(scores):
        print(f"[BREAKING] Optimum reached after {c} iterations")
        break
    else:
        c_max = np.max(scores)
        scores = np.array([])
        init[n_max] = init[n_max]-1
        init[i_max] = init[i_max]+1

print(f'''
Final score: {c_max}''')
print(f'''
Final array:

{init}''')