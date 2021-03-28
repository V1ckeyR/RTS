import math
import matplotlib.pyplot as plt

from lab11.main import Signal


def w(pk, N):
    fi = 2 * math.pi / N * pk
    return complex(math.cos(fi), -math.sin(fi))


table = {}


def memoization(fun, arg1, arg2, arg3):
    params = (arg1 * arg2, arg3)
    if params not in table:
        table[params] = fun(arg1 * arg2, arg3)
    return table[params]


def f(p, N):
    res = 0
    for k in range(N):
        res += s.xt[k] * memoization(w, p, k, N)
    return res


def dft(N):
    sequence = range(N)
    spector = [f(freq, N) for freq in sequence]
    modules = list(map(lambda x: abs(x), spector))
    plt.xlabel('Частота')
    plt.ylabel('Амплітуда')
    plt.plot(sequence, modules)


s = Signal()
# dft(s.N)
# plt.show()

# for key, v in table.items():
#     print(f'p*k = {key[0]} -> w = {v}')

# print(w(9, 4))
