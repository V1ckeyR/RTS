from lab11.main import Signal
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
taus = range(200)
cors = [rx(s1, t) for t in taus]
# cors = [rxy(s1, s2, t) for t in taus]
plt.xlabel("tau")
plt.ylabel("correlation")
plt.plot(taus, cors)
plt.show()
