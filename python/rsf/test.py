import numpy as np

n = 25

p = np.full(
  shape=n,
  fill_value=1/n,
  dtype=np.float_
)

print(p)
x = np.random.multinomial(2500, p, 1)

print(np.sum(x))
print(x)