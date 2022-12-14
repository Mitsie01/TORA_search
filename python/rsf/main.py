import numpy as np
import sys
from colorama import Fore

def main():
    global Z, delta
    Z = 25
    delta = 0.01

    global id, p_value, gamma
    field = np.genfromtxt("field.csv", delimiter=",")
    id = field[:,0]
    p_value = field[:,1]
    gamma = field[:,2]
    
    input("Voer opdracht A uit?")
    Opdracht_A()
    input("Voer opdracht B uit?")
    Opdracht_B()
    input("Voer opdracht D uit?")
    Opdracht_D(Z)
    input("Voer opdracht E uit?")
    Opdracht_E()

def optimum_finder(init, delta):
    total_max = 0
    cycle_max = 0
    iterations = 3000
    init_score = np.sum(p_value*(1-np.exp(-gamma*(init*delta))))
    print(f'Initial score: {init_score}')

    print(Fore.GREEN + f'''
[STARTING]''' + Fore.RESET + f" Starting iteration process of max {iterations} iterations.")

    for cycle in range(iterations):   
        print(Fore.CYAN + f'[ITERATING]' + Fore.RESET + f'{int((cycle/iterations)*100)}%', end='\r')
        sys.stdout.write("\033[K")
        for pos_min in range(init.size):
            if init[pos_min] > 0:
                init[pos_min] = init[pos_min]-1
                for pos_plus in range(init.size):
                    if pos_plus != pos_min:
                        init[pos_plus] = init[pos_plus]+1
                        # Calculate score
                        score = np.sum(p_value*(1-np.exp(-gamma*(init*delta))))
                        if score > cycle_max:
                            cycle_max = score
                            cycle_pos_min = pos_min
                            cycle_pos_plus = pos_plus
                        init[pos_plus] = init[pos_plus]-1
                init[pos_min] = init[pos_min]+1

        if total_max >= cycle_max:
            print(Fore.RED + f"[BREAKING]" + Fore.RESET + f" Optimum reached after {cycle} iterations")
            try:    
                print(f'''
Final array:

{init.reshape(5,5)}''')
                print(f'''
Final score: {total_max}''')
            except:
                pass
            break
        else:
            total_max = cycle_max
            init[cycle_pos_min] = init[cycle_pos_min]-1
            init[cycle_pos_plus] = init[cycle_pos_plus]+1
    return total_max, init


def array_generator(Z, delta):
    print(f'''
{Fore.CYAN}[GENERATING]{Fore.RESET} Generating random array.''')
    p = np.full(shape=Z,fill_value=1/Z,dtype=np.float_)
    random_array = np.random.multinomial(int(Z/delta), p, 1).flatten()
    print(f'''{Fore.GREEN}[FINISHED]{Fore.RESET} Random array generated:

{random_array.reshape(5,5)}
''')
    return random_array


def Opdracht_A():
    init = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100])
    print(f'''
-------------------------------------------------------------''' + Fore.GREEN + '''
[STARTING]''' + Fore.RESET + f'''

{init.reshape(5,5)}
''')
    optimum_p, optimum_array = optimum_finder(init, delta)
    return optimum_p, optimum_array


def Opdracht_B():
    global p_value, gamma
    p_0 = p_value
    gamma_0 = gamma
    
    init = np.array([625,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1875])
    init_left = init.reshape(5,5)[:, np.r_[0:4]].reshape(20)
    init_right = init.reshape(5,5)[:, 4]
    
    p_value = p_0.reshape(5,5)[:, 4]
    gamma = gamma_0.reshape(5,5)[:, 4]
    total_right, init_right = optimum_finder(init_right, delta)
    
    p_value = p_0.reshape(5,5)[:, np.r_[0:4]].reshape(20)
    gamma = gamma_0.reshape(5,5)[:, np.r_[0:4]].reshape(20)
    total_left, init_left = optimum_finder(init_left, delta)

    init.reshape(5,5)[:, 4] = init_right
    init.reshape(5,5)[:, np.r_[0:4]] = init_left.reshape(5,4)
    total_max = total_left + total_right
    print(f'''
Final array:

{init.reshape(5,5)}''')
    print(f'''
Final score: {total_max}''')
    p_value = p_0
    gamma = gamma_0

def Opdracht_D(Z):
    # for 3 different delta values: 0.1, 0.06, 0.02
    delta = 0.1
    p_values = []
    for i in range(3):
        delta = 0.1
        array = array_generator(Z, delta)
        max, array = optimum_finder(array, delta)
        p_values.append(float(max))
        delta -= 0.4
        print(p_values)
    print(f'''
==============================================================
Probability scores:

delta = 0.1: {p_values[0]}
delta = 0.06: {p_values[1]}
delta = 0.02: {p_values[2]}

Difference between delta values: {(np.max(p_values)-np.min(p_values))/((np.max(p_values)+np.min(p_values))/2)*100} %
''')


def Opdracht_E():
    highest_max = 0
    loops = 3
    for i in range(loops):
        print(f'''
-------------------------------------------------------------{Fore.GREEN}
[STARTING]{Fore.RESET} Cycle {i+1}/{loops}''')

        init = array_generator(Z, delta)

        total_max, init = optimum_finder(init, delta)

        if total_max > highest_max:
            highest_max = total_max
            highest_array = init
            print(f'''
New maximum found: {total_max}''')

    print(f'''
=================================================

Final maximum score: {total_max}''')
    print(f'''
Final array:

{highest_array.reshape(5,5)}''')

if __name__ == "__main__":
    main()


