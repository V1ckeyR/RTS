import math
import random
import time

import matplotlib.pyplot as plt

n = 10        # Число гармонік в сигналі
w_max = 1500  # Гранична частота
N = 256       # Кількість дискретних відліків

w0 = w_max / N


def generate(harmonics=n, rate=N):
    x = [0] * rate
    for h in range(harmonics):
        w = w0 * (h + 1)
        a = random.random()
        phi = random.random()
        for t in range(rate):
            x[t] += a * math.sin(w * t + phi)
    return x


class Signal:
    def __init__(self, gen=generate, harmonics=n, rate=N):
        self.n = harmonics
        self.N = rate
        self.generate = gen
        self.xt = gen(harmonics, rate)

    def set_rate(self, rate):
        self.N = rate
        self.xt = self.generate(self.n, rate)

    def set_harmonics(self, harmonics):
        self.n = harmonics
        self.xt = self.generate(harmonics, self.N)

    def get_m(self):
        return sum(self.xt)/self.N

    def get_d(self):
        res = 0
        expectation = self.get_m()
        for i in range(self.N):
            res += (self.xt[i] - expectation) ** 2
        return res / (self.N - 1)

    def show(self):
        mx = [self.get_m()] * self.N
        plt.xlabel("t")
        plt.ylabel("x(t)")
        plt.plot(range(self.N), mx, 'r--', range(self.N), self.xt)
        plt.show()

    def n_v_t(self):
        harmonics = range(1, 1000, 10)
        times = []

        for i in harmonics:
            start = time.time()
            self.generate(i)
            times.append(time.time() - start)

        plt.ylabel("O(n)")
        plt.plot(harmonics, times)
        plt.show()

    def N_v_M(self):
        rates = [4 * 4 ** i for i in range(7)]
        expectations = []

        for i in rates:
            self.set_rate(i)
            expectations.append(self.get_m())

        plt.xlabel("N")
        plt.ylabel("Mx")
        plt.plot(rates, expectations)
        plt.show()


signal = Signal()
xt = signal.xt
M = signal.get_m()
D = signal.get_d()
# print(M, D)
# signal.N_v_M()
