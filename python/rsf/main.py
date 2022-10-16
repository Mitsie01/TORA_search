import numpy as np
import sys
from colorama import Fore

def main():
    global Z, delta, loops, tspan
    Z = 25
    delta = 0.01
    loops = 3
    tspan = int(Z/delta)

    global id, p_value, gamma
    field = np.genfromtxt("field.csv", delimiter=",")
    id = field[:,0]
    p_value = field[:,1]
    gamma = field[:,2]
    
    Opdracht_A()
    Opdracht_B()
    Opdracht_C()
    Opdracht_D()
    Opdracht_E()

def optimum_finder(init):
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
            print(f'''
Final score: {total_max}''')
            print(f'''
Final array:

{init}''')
            break
        else:
            total_max = cycle_max
            init[cycle_pos_min] = init[cycle_pos_min]-1
            init[cycle_pos_plus] = init[cycle_pos_plus]+1
    return total_max, init

def Opdracht_A():
  init = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100])
  print(f'''
-----------------------------------------------
[STARTING] 

Array:

{init}
''')
  optimum_finder(init)


def Opdracht_B():
    pass

def Opdracht_C():
    pass

def Opdracht_D():
    pass

def Opdracht_E():
    highest_max = 0
    for i in range(loops):

        p = np.full(
        shape=Z,
        fill_value=1/Z,
        dtype=np.float_
        )
        init = np.random.multinomial(int(Z/delta), p, 1).flatten()

        print(f'''
-------------------------------------------------------------''' + Fore.GREEN + '''
[STARTING]''' + Fore.RESET + f''' Cycle {i+1}/{loops}'''

+ Fore.CYAN +'''
[GENERATING]''' + Fore.RESET + f'''generated new random array:

{init}
''')
        total_max, init = optimum_finder(init)

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

{init}''')

if __name__ == "__main__":
    main()


