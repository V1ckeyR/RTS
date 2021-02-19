import math
import random
# import time

import matplotlib.pyplot as plt

n = 10        # Число гармонік в сигналі
w_max = 1500  # Гранична частота
N = 256       # Кількість дискретних відліків

w0 = w_max / N


def generate(harmonics):
    x = [0] * N
    for h in range(harmonics):
        w = w0 * (h + 1)
        a = random.random()
        phi = random.random()
        for t in range(N):
            x[t] += a * math.sin(w * t + phi)
    return x


xt = generate(n)

# o = range(1, 1000, 10)
# times = []

# for i in o:
#     start = time.time()
#     generate(i)
#     times.append(time.time() - start)

M = [sum(xt)/N] * N

d = 0
for j in range(N):
    d += ((xt[j] - M[0]) ** 2)
D = d/(N - 1)

print(M[0], D)
plt.xlabel("t")
plt.ylabel("x(t)")
plt.plot(range(N), M, 'r--', range(N), xt)
# plt.ylabel("O(n)")
# plt.plot(o, times)
plt.show()
