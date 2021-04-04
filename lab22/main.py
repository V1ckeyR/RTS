import matplotlib.pyplot as plt

from lab11.main import Signal
from lab21.main import w


def fft(x, N):
    if N % 2 > 0:
        raise ValueError("N must be a power of 2")
    elif N == 2:
        return [w(0, N) * (x[0] + x[1]), w(0, N) * (x[0] - x[1])]
    else:
        x_even = fft(x[::2], N/2)
        x_odd = fft(x[1::2], N/2)
        x_res = [0] * int(N)
        for p in range(int(N/2)):
            x_res[p] = x_even[p] + x_odd[p] * w(p, N)
            x_res[int(N/2) + p] = x_even[p] - x_odd[p] * w(p, N)
        return x_res


s = Signal()
plt.xlabel('Частота')
plt.ylabel('Амплітуда')
# plt.plot(range(s.N), list(map(lambda i: abs(i), fft(s.xt, s.N))))
# plt.show()


def fft_time():
    def timer(name, stmt):
        # The output will be a list of the execution times
        # of all code runs repeated a specified no. of times.
        from timeit import repeat
        times = repeat(setup=setup,
                       stmt=stmt,
                       repeat=3,
                       number=10000)
        print(f'{name} execution time: {min(times)}')

    setup = '''
from lab21.main import f
from lab11.main import Signal
        '''

    my_dft = '''
def dft(N):
    return [f(freq, N) for freq in range(N)]
s = Signal()
dft(s.N)
        '''

    timer("My DFT", my_dft)

    setup = '''
from lab11.main import Signal
from lab21.main import w
    '''

    my_fft = '''
def fft(x, N):
    if N % 2 > 0:
        raise ValueError("N must be a power of 2")
    elif N == 2:
        return [w(0, N) * (x[0] + x[1]), w(0, N) * (x[0] - x[1])]
    else:
        x_even = fft(x[::2], N/2)
        x_odd = fft(x[1::2], N/2)
        x_res = [0] * int(N)
        for p in range(int(N/2)):
            x_res[p] = x_even[p] + x_odd[p] * w(p, N)
            x_res[int(N/2) + p] = x_even[p] - x_odd[p] * w(p, N)
        return x_res


s = Signal()
list(map(lambda i: abs(i), fft(s.xt, s.N)))
    '''

    timer("My FFT", my_fft)

    setup = '''
from numpy.fft import fft
from lab11.main import Signal
    '''

    numpy_fft = '''
s = Signal()
fft(s.xt, s.N)
    '''
    timer("Numpy FFT", numpy_fft)


# fft_time()

def additional_task():
    def timer(my_setup, my_code, rate):
        # The output is the execution time of number times
        # iteration of the code snippet, not the single iteration.
        from timeit import timeit
        number = 100
        return timeit(setup=my_setup, stmt=my_code.format(rate), number=number) / number

    my_fft_setup = '''
from lab11.main import Signal
from lab21.main import w
        '''

    my_fft_code = '''
def fft(x, N):
    if N % 2 > 0:
        raise ValueError("N must be a power of 2")
    elif N == 2:
        return [w(0, N) * (x[0] + x[1]), w(0, N) * (x[0] - x[1])]
    else:
        x_even = fft(x[::2], N/2)
        x_odd = fft(x[1::2], N/2)
        x_res = [0] * int(N)
        for p in range(int(N/2)):
            x_res[p] = x_even[p] + x_odd[p] * w(p, N)
            x_res[int(N/2) + p] = x_even[p] - x_odd[p] * w(p, N)
        return x_res


s = Signal(rate={})
list(map(lambda i: abs(i), fft(s.xt, s.N)))
        '''

    np_fft_setup = '''
from numpy.fft import fft
from lab11.main import Signal
        '''

    np_fft_code = '''
s = Signal(rate={})
fft(s.xt, s.N)
        '''

    rates = [4 * 4 ** i for i in range(7)]
    my_fft_time = []
    np_fft_time = []
    for item in rates:
        my_fft_time.append(timer(my_fft_setup, my_fft_code, item))
        np_fft_time.append(timer(np_fft_setup, np_fft_code, item))

    print(rates, my_fft_time)
    plt.xlabel("Rate")
    plt.ylabel("Time")
    plt.plot(rates, my_fft_time, rates, np_fft_time)
    plt.show()


additional_task()
