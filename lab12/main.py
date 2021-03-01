from lab11.main import Signal
from time import time
import matplotlib.pyplot as plt


def rx(x, tau=0):
    res = 0
    m = x.get_m()
    for t in range(x.N - tau):
        res += (x.xt[t] - m) * (x.xt[t + tau] - m)
    return res/(x.N - 1)


def rxy(x, y, tau=0):
    res = 0
    mx = x.get_m()
    my = y.get_m()
    for t in range(x.N - tau):
        res += (x.xt[t] - mx) * (y.xt[t + tau] - my)
    return res/(x.N - 1)


# Графік залежності кореляції від тау
s1 = Signal()
s2 = Signal()
s1.set_rate(10000)
s2.set_rate(10000)
taus = range(10000)

start = time()
auto_cors = [rx(s1, t) for t in taus]
time_auto = round(time() - start, 3)

start = time()
cors = [rxy(s1, s2, t) for t in taus]
time_cors = round(time() - start, 3)

logical = '<' if time_auto < time_cors else '>'
logical = '=' if time_auto == time_cors else logical

print(f'Час побудови автокореляції: {time_auto}\nЧас побудови кореляції: {time_cors}')
print(f'Час побудови автокореляції {logical} Час побудови кореляції')

plt.xlabel("tau")
plt.ylabel("correlation")
plt.plot(taus, cors)
# plt.show()
