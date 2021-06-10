from matplotlib import pyplot as plt
from numpy import arange

from scheduler.scheduler import Scheduler


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
        self.disciplines = {
            'fifo': lambda s: s.fifo(),
            'rm': lambda s: s.rm(),
            'edf': lambda s: s.edf()
        }
        self.colors = {
            'fifo': 'r',
            'rm': 'g',
            'edf': 'b'
        }

    def show_processors(self):
        s = Scheduler(self.size, self.lam, self.processors)
        processors = s.processors
        disciplines = list(self.disciplines.keys())
        amount = len(disciplines)
        collection = {}

        for n in range(amount):
            self.disciplines[disciplines[n]](s)
            for p in processors:
                collection[p.number] = p.completed

        plt.title('Завантаженість процесорів')
        plt.xlabel('Процесор')
        plt.ylabel('Виконано тасків')
        plt.bar(list(collection.keys()), collection.values())
        plt.show()

    def show_all(self):
        disciplines = list(self.disciplines.keys())
        amount = len(disciplines)

        fig, axs = plt.subplots(3)
        for n in range(amount):
            discipline = disciplines[n]
            self.bar('all', axs[0], self.disciplines[discipline], discipline)
            i, awt, awt_p, downtime, d, dp = self.intensity(self.disciplines[discipline])
            self.intensity_v_waiting_time(discipline, axs[1], i, awt, awt_p)
            self.percentage(discipline, axs[2], i, downtime, d, dp)

        plt.show()

    def show_protected(self):
        disciplines = list(self.disciplines.keys())
        amount = len(disciplines)

        for n in range(amount):
            fig, axs = plt.subplots(3)
            discipline = disciplines[n]
            self.bar('protected', axs[0], self.disciplines[discipline], discipline)
            i, awt, awt_p, downtime, d, dp = self.intensity(self.disciplines[discipline])
            self.intensity_v_waiting_time('protected', axs[1], i, awt, awt_p)
            self.percentage(discipline, axs[2], i, downtime, d, dp)

        plt.show()

    def waiting_time_v_task_amount(self, s, ax, title, color):
        if title in list(self.disciplines.keys()):
            wt = [c + p for c, p in zip(s.waiting_time['common'], s.waiting_time['protected'])]
        else:
            wt = s.waiting_time[title]
        wt.sort()

        collection = {}
        for i in wt:
            collection[i] = collection.get(i, 0) + 1

        ax.bar(list(collection.keys()), collection.values(), color=color, label=title)

    def bar(self, method, ax, discipline, title):
        s = Scheduler(self.size, self.lam, self.processors)
        discipline(s)

        if method == 'all':
            self.waiting_time_v_task_amount(s, ax, title, self.colors[title])
        else:
            self.waiting_time_v_task_amount(s, ax, 'common', 'b')
            self.waiting_time_v_task_amount(s, ax, 'protected', 'm')

        print(title.upper().center(60, '-'))
        print('Інтенсивність:', round(1 / self.lam, 2))
        s.show()

        if method == 'protected':
            ax.set_title(title.upper())

        ax.set_xlabel('Час очікування')
        ax.set_ylabel('Кількість заявок')
        ax.legend()

    def intensity(self, discipline):
        intensity = arange(0.01, 0.1, 0.003)
        downtime = []
        average_waiting_time = []
        average_waiting_time_protected = []
        deadline = []
        deadline_protected = []

        for i in intensity:
            s = Scheduler(self.size, 1 / i, self.processors)
            discipline(s)
            dt = s.downtime / s.size * 100
            awt = s.average_waiting_time['common']
            awt_p = s.average_waiting_time['protected']
            d = s.deadline_over['common'] / s.task_amount['common'] * 100
            dp = s.deadline_over['protected'] / s.task_amount['protected'] * 100

            downtime.append(dt)
            average_waiting_time.append(awt)
            average_waiting_time_protected.append(awt_p)
            deadline.append(d)
            deadline_protected.append(dp)

        return intensity, average_waiting_time, average_waiting_time_protected, downtime, deadline, deadline_protected

    def intensity_v_waiting_time(self, discipline, ax, i, awt, awt_p):
        ax.set_xlabel('Інтенсивність вхідного потоку заявок')
        ax.set_ylabel('Середній час очікування')
        if discipline in list(self.disciplines.keys()):
            ax.plot(i, [c + p for c, p in zip(awt, awt_p)], color=self.colors[discipline], label=discipline)
        else:
            ax.plot(i, awt, color='g', label='Звичайні')
            ax.plot(i, awt_p, color='m', label='Захищені')
        ax.legend()

    def percentage(self, discipline, ax, i, downtime, d, dp):
        ax.set_xlabel('Інтенсивність вхідного потоку заявок')
        if discipline in list(self.disciplines.keys()):
            ax.plot(i, downtime, color=self.colors[discipline], label="Процент простою")
            ax.plot(i, d, color=self.colors[discipline], label="Процент відкинутих")
        else:
            ax.plot(i, downtime, color='r', label="Процент простою")
            ax.plot(i, d, color='k', label="Процент відкинутих")
            ax.plot(i, dp, color='m', label="Процент відкинутих захищених")
            ax.legend()
