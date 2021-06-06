from numpy import arange
from numpy.random import poisson
import matplotlib.pyplot as plt


class Task:
    """
    Клас, в якому зберігаються параметри заявки
    :param time_of_arrival: час прибуття в систему планування
    :param time_of_execution: час виконання заяви
    :param k: коефіцієнт для розрахунку коректного дедлайна
    """
    def __init__(self, time_of_arrival, time_of_execution, k):
        self.tp = time_of_arrival
        self.to = time_of_execution
        self.td = time_of_arrival + time_of_execution * k
        self.progress = time_of_execution

    def __lt__(self, other):
        return self.tp < other.tp

    def __repr__(self):
        return f'[start: {self.tp}, ' \
               f'execution: {self.to}, ' \
               f'deadline: {self.td}]'


def generate_stream(size, lam, time_of_execution, deadline):
    """
    Функція, яка генерує потік тасків певного типу за допомогою потоку Пуассона
    :param size: орієнтовна кількість тактів
    :param lam: лямбда для потоку Пуассона
    :param time_of_execution: для налаштування тасків
    :param deadline: для налаштування тасків
    :return: масив тасків
    """
    time_to_arrive = 0
    stream = [Task(time_to_arrive, time_of_execution, deadline)]
    while True:
        time_to_arrive += poisson(lam)
        if time_to_arrive + time_of_execution > size:
            break
        stream.append(Task(time_to_arrive, time_of_execution, deadline))
    return stream


class Processor:
    """
    Клас, в якому зберігається стан процесора
    """
    def __init__(self):
        self.status = 1  # 0 - busy, 1 - free
        self.task = None

    def set_task(self, task):
        self.status = 0
        self.task = task

    def work(self):
        if self.task:
            self.task.progress -= 1
            if not self.task.progress:  # Finish work
                self.clear()

    def clear(self):
        self.status = 1
        self.task = None


class Scheduler:
    """
    Клас, що симулює алгоритми планування
    :param size: кількість тактів системи
    :param lam: лямбда, необхідна для генерації потоку заявок
    :param processors: кількість доступних процесорів
    """
    def __init__(self, size, lam, processors):
        t1 = generate_stream(size, lam=lam, time_of_execution=10, deadline=5)
        t2 = generate_stream(size, lam=2 * lam, time_of_execution=50, deadline=5)
        t3 = generate_stream(size, lam=10 * lam, time_of_execution=3, deadline=1)
        t = t1 + t2 + t3
        t.sort()

        self.size = size
        self.stream = t
        self.processors = tuple(Processor() for _ in range(processors))

        self.downtime = 0
        self.buffer_size = []
        self.waiting_time = []
        self.deadline_over = 0

    @staticmethod
    def check_stream(stream, buffer, tact, method):
        new_stream = []
        for task in stream:
            if task.tp == tact:
                buffer.append(task)  # Task ready to execute

                if method == 'rm':
                    buffer.sort(key=lambda t: t.to)

                if method == 'edf':
                    buffer.sort(key=lambda t: t.td)
            else:
                new_stream.append(task)

        return new_stream, buffer

    @staticmethod
    def check_downtime(buffer, processors):
        if not buffer:
            for processor in processors:
                if processor.status:
                    return 1
        return 0

    def clear_processors(self):
        for processor in self.processors:
            processor.clear()

    def scheduling(self, method=None):
        stream = self.stream
        buffer = []  # вхідна черга заявок

        downtime = 0
        buffer_size = []
        waiting_time = []
        deadline_over = 0

        for tact in range(self.size):
            stream, buffer = self.check_stream(stream, buffer, tact, method)

            for processor in self.processors:
                if processor.status:
                    while buffer:
                        task = buffer.pop(0)
                        waiting_time.append(tact - task.tp)
                        if tact + task.to <= task.td:
                            processor.set_task(task)
                            break
                        else:
                            deadline_over += 1  # Deadline is over
                processor.work()

            buffer_size.append(len(buffer))
            downtime += self.check_downtime(buffer, self.processors)

        self.clear_processors()
        self.downtime = downtime
        self.buffer_size = buffer_size
        self.waiting_time = waiting_time
        self.deadline_over = deadline_over

        return waiting_time, downtime / self.size * 100, deadline_over / len(self.stream) * 100

    def fifo(self):
        return self.scheduling()

    def rm(self):
        return self.scheduling('rm')

    def edf(self):
        return self.scheduling('edf')

    def show(self):
        average_waiting_time = sum(self.waiting_time)/len(self.waiting_time)
        print('Кількість процесорів:', len(self.processors))
        print('Середній розмір вхідної черги заявок:', sum(self.buffer_size) / len(self.buffer_size))
        print('Середній час очікування заявки в черзі:', round(average_waiting_time, 2))
        print('Кількість прострочених заявок:', self.deadline_over)
        print('Відношення кількості прострочених заявок до загальної кількості:',
              round(self.deadline_over / len(self.stream), 2))


class Graphics:
    """
    Клас для побудови графіків для усіх дисциплін
    :param size: кількість тактів системи планувальння
    :param intensity: інтенсивність потоку для першого графіку
    :param processors: кількість доступних процесорів для системи планування
    """
    def __init__(self, size, intensity, processors):
        self.size = size
        self.lam = 1/intensity
        self.processors = processors
        self.methods = {
            'fifo': lambda s: s.fifo(),
            'rm': lambda s: s.rm(),
            'edf': lambda s: s.edf()
        }

    def show(self):
        methods = list(self.methods.keys())
        columns = len(methods)

        fig, axs = plt.subplots(ncols=columns, nrows=3)

        for column in range(columns):
            method = methods[column]
            self.bar(axs[0, column], self.methods[method], method)
            self.plots(axs[1, column], axs[2, column], self.methods[method])

        fig.tight_layout()
        plt.show()

    def bar(self, ax, method, title):
        s = Scheduler(self.size, self.lam, self.processors)
        waiting_time_for_each_task, _, _ = method(s)
        waiting_time_for_each_task.sort()

        print(title.upper().center(60, '-'))
        print('Інтенсивність:', round(1 / self.lam, 2))
        s.show()

        collection = {}
        for i in waiting_time_for_each_task:
            collection[i] = collection.get(i, 0) + 1

        ax.set_title(title.upper())
        ax.set_xlabel('Час очікування')
        ax.set_ylabel('Кількість заявок')
        ax.bar(list(collection.keys()), collection.values(), color='b')

    def plots(self, ax1, ax2, method):
        intensity = arange(0.01, 0.2, 0.001)
        average_waiting_time = []
        downtime = []
        deadline = []

        for i in intensity:
            wt, dt, d = method(Scheduler(self.size, 1 / i, self.processors))
            average_waiting_time.append(sum(wt) / len(wt))
            downtime.append(dt)
            deadline.append(d)

        ax1.set_xlabel('Інтенсивність вхідного потоку заявок')
        ax1.set_ylabel('Середній час очікування')
        ax1.plot(intensity, average_waiting_time, color='g')

        ax2.set_xlabel('Інтенсивність вхідного потоку заявок')
        ax2.plot(intensity, downtime, color='r', label="Процент простою")
        ax2.plot(intensity, deadline, color='k', label="Процент відкинутих")
        ax2.legend()


if __name__ == '__main__':
    g = Graphics(size=1000, intensity=0.5, processors=4)
    g.show()
