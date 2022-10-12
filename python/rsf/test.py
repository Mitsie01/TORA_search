import numpy as np
def main():
    random = np.array([])
    total = 0
    for _ in range(25):
        number = np.random.randint(0,100)
        np.append(random, number)
        total += number
    print(random)

















if __name__ == "__main__":
    main()