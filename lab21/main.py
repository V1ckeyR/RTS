import math
import matplotlib.pyplot as plt

from lab11.main import Signal


def w(pk, N):
    fi = 2 * math.pi / N * pk
    return complex(math.cos(fi), -math.sin(fi))


def f(p, N):
    res = 0
    for k in range(N):
        res += s.xt[k] * w(p * k, N)
    return res


def dpf(N):
    sequence = range(N)
    spector = [f(freq, N) for freq in sequence]
    modules = list(map(lambda x: abs(x), spector))
    plt.xlabel('Частота')
    plt.ylabel('Амплітуда')
    plt.plot(sequence, modules)


s = Signal()
dpf(s.N)
plt.show()
