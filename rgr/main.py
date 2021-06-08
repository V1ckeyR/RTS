from numpy import arange
from numpy.random import poisson
import matplotlib.pyplot as plt


class Task:
    """
    Клас, в якому зберігаються параметри заявки
    :param time_of_arrival: час прибуття в систему планування
    :param time_of_execution: час виконання заяви
    :param k: коефіцієнт для розрахунку коректного дедлайна
    :param protected: True якщо таск захищений
    """
    def __init__(self, time_of_arrival, time_of_execution, k, protected):
        self.tp = time_of_arrival
        self.to = time_of_execution
        self.td = time_of_arrival + time_of_execution * k
        self.progress = time_of_execution
        self.protected = protected

    def __lt__(self, other):
        return self.tp < other.tp

    def __repr__(self):
        return f'[start: {self.tp}, ' \
               f'execution: {self.to}, ' \
               f'deadline: {self.td}]'


def generate_stream(size, lam, time_of_execution, deadline, protected):
    """
    Функція, яка генерує потік тасків певного типу за допомогою потоку Пуассона
    :param size: орієнтовна кількість тактів
    :param lam: лямбда для потоку Пуассона
    :param time_of_execution: для налаштування тасків
    :param deadline: для налаштування тасків
    :param protected: визначає чи таски будуть захищеними
    :return: масив тасків
    """
    time_to_arrive = 0
    stream = [Task(time_to_arrive, time_of_execution, deadline, protected)]
    while True:
        time_to_arrive += poisson(lam)
        if time_to_arrive + time_of_execution > size:
            break
        stream.append(Task(time_to_arrive, time_of_execution, deadline, protected))
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
        t1 = generate_stream(size, lam=2 * lam, time_of_execution=5, deadline=3, protected=True)
        t2 = generate_stream(size, lam=5 * lam, time_of_execution=10, deadline=6, protected=True)
        t3 = generate_stream(size, lam=0.5 * lam, time_of_execution=5, deadline=3, protected=False)
        t4 = generate_stream(size, lam=lam, time_of_execution=50, deadline=6, protected=False)
        t5 = generate_stream(size, lam=2 * lam, time_of_execution=2, deadline=10, protected=False)

        t = t1 + t2 + t3 + t4 + t5
        t.sort()

        self.size = size
        self.stream = t
        self.processors = tuple(Processor() for _ in range(processors))

        self.downtime = 0
        self.buffer_size = {}
        self.waiting_time = {}
        self.deadline_over = {}
        self.task_amount = {}

    @staticmethod
    def check_stream(stream, buffer, buffer_protected, tact, method):
        new_stream = []
        for task in stream:
            if task.tp == tact:  # Task ready to execute
                if task.protected:
                    buffer_protected.append(task)

                    if method == 'rm':
                        buffer_protected.sort(key=lambda t: t.to)

                    if method == 'edf':
                        buffer_protected.sort(key=lambda t: t.td)
                else:
                    buffer.append(task)

                    if method == 'rm':
                        buffer.sort(key=lambda t: t.to)

                    if method == 'edf':
                        buffer.sort(key=lambda t: t.td)
            else:
                new_stream.append(task)

        return new_stream

    @staticmethod
    def check_buffer(buffer, tact, processor, waiting_time, deadline_over):
        while buffer:
            task = buffer.pop(0)
            waiting_time.append(tact - task.tp)
            if tact + task.to <= task.td:
                processor.set_task(task)
                break
            else:
                deadline_over += 1  # Deadline is over
        return deadline_over

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

    def count_tasks(self):
        common = 0
        protected = 0

        for task in self.stream:
            if task.protected:
                protected += 1
            else:
                common += 1

        self.task_amount = {
            'common': common,
            'protected': protected
        }

    def scheduling(self, method=None):
        stream = self.stream
        buffer = []  # вхідна черга заявок
        buffer_protected = []  # вхідна черга захищених заявок

        downtime = 0

        buffer_size = []
        waiting_time = []
        deadline_over = 0

        buffer_size_protected = []
        wt_protected = []
        d_protected = 0

        for tact in range(self.size):
            stream = self.check_stream(stream, buffer, buffer_protected, tact, method)

            for processor in self.processors:
                if processor.status:
                    if buffer_protected:
                        d_protected = self.check_buffer(buffer_protected, tact, processor, wt_protected, d_protected)
                    if not buffer_protected:
                        deadline_over = self.check_buffer(buffer, tact, processor, waiting_time, deadline_over)
                processor.work()

            buffer_size.append(len(buffer))
            buffer_size_protected.append(len(buffer_protected))
            downtime += self.check_downtime(buffer, self.processors)

        self.clear_processors()
        self.count_tasks()

        self.downtime = downtime
        self.buffer_size = {
            'common': buffer_size,
            'protected': buffer_size_protected
        }
        self.waiting_time = {
            'common': waiting_time,
            'protected': wt_protected
        }
        self.deadline_over = {
            'common': deadline_over,
            'protected': d_protected
        }

    def fifo(self):
        return self.scheduling()

    def rm(self):
        return self.scheduling('rm')

    def edf(self):
        return self.scheduling('edf')

    def show(self):
        if not self.waiting_time:
            print('Please, run algorithm before')

        average_waiting_time = sum(self.waiting_time['common'])/len(self.waiting_time['common'])
        average_waiting_time_protected = sum(self.waiting_time['protected'])/len(self.waiting_time['protected'])
        average_buffer_size = sum(self.buffer_size['common']) / len(self.buffer_size['common'])
        average_buffer_size_protected = sum(self.buffer_size['protected']) / len(self.buffer_size['protected'])

        print('Кількість процесорів:', len(self.processors))
        print('Середній розмір вхідної черги заявок:', average_buffer_size)
        print('Середній розмір вхідної черги захищених заявок:', average_buffer_size_protected)
        print('Середній час очікування заявки в черзі:', round(average_waiting_time, 2))
        print('Середній час очікування захищеної заявки в черзі:', round(average_waiting_time_protected, 2))
        print('Кількість прострочених заявок:', self.deadline_over['common'])
        print('Кількість прострочених захищених заявок:', self.deadline_over['protected'])
        print('Відношення кількості прострочених заявок до загальної кількості:',
              round(self.deadline_over['common'] / self.task_amount['common'], 2))
        print('Відношення кількості прострочених захищених заявок до загальної кількості:',
              round(self.deadline_over['protected'] / self.task_amount['protected'], 2))


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
        amount = len(methods)

        for n in range(amount):
            fig, axs = plt.subplots(3)
            method = methods[n]
            self.bar(axs[0], self.methods[method], method)
            self.plots(axs[1], axs[2], self.methods[method])

        plt.show()

    def bar(self, ax, method, title):
        s = Scheduler(self.size, self.lam, self.processors)
        method(s)
        wt = s.waiting_time['common']
        wt.sort()
        wtp = s.waiting_time['protected']
        wtp.sort()

        print(title.upper().center(60, '-'))
        print('Інтенсивність:', round(1 / self.lam, 2))
        s.show()

        collection = {}
        for i in wt:
            collection[i] = collection.get(i, 0) + 1

        collection_protected = {}
        for i in wtp:
            collection_protected[i] = collection_protected.get(i, 0) + 1

        ax.set_title(title.upper())
        ax.set_xlabel('Час очікування')
        ax.set_ylabel('Кількість заявок')
        ax.bar(list(collection.keys()), collection.values(), color='b', label='Звичайні')
        ax.bar(list(collection_protected.keys()), collection_protected.values(), color='m', label='Захищені')
        ax.legend()

    def plots(self, ax1, ax2, method):
        intensity = arange(0.01, 0.1, 0.003)
        downtime = []
        average_waiting_time = []
        average_waiting_time_protected = []
        deadline = []
        deadline_protected = []

        for i in intensity:
            s = Scheduler(self.size, 1 / i, self.processors)
            method(s)
            dt = s.downtime / s.size * 100
            wt = s.waiting_time['common']
            wtp = s.waiting_time['protected']
            d = s.deadline_over['common'] / s.task_amount['common'] * 100
            dp = s.deadline_over['protected'] / s.task_amount['protected'] * 100

            downtime.append(dt)
            average_waiting_time.append(sum(wt) / len(wt))
            average_waiting_time_protected.append(sum(wtp) / len(wtp))
            deadline.append(d)
            deadline_protected.append(dp)

        ax1.set_xlabel('Інтенсивність вхідного потоку заявок')
        ax1.set_ylabel('Середній час очікування')
        ax1.plot(intensity, average_waiting_time, color='g', label='Звичайні')
        ax1.plot(intensity, average_waiting_time_protected, color='m', label='Захищені')
        ax1.legend()

        ax2.set_xlabel('Інтенсивність вхідного потоку заявок')
        ax2.plot(intensity, downtime, color='r', label="Процент простою")
        ax2.plot(intensity, deadline, color='k', label="Процент відкинутих")
        ax2.plot(intensity, deadline_protected, color='m', label="Процент відкинутих захищених")
        ax2.legend()


if __name__ == '__main__':
    g = Graphics(size=1000, intensity=0.5, processors=2)
    g.show()
