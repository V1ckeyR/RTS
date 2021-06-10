from scheduler.generator import generate_stream
from scheduler.processor import Processor


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
        self.processors = tuple(Processor(n) for n in range(processors))

        self.downtime = 0
        self.buffer_size = {}
        self.waiting_time = {}
        self.average_waiting_time = {}
        self.deadline_over = {}
        self.task_amount = {}

    def scheduling(self, method=None):
        self.clear_processors()
        stream = self.stream
        buffer = []  # вхідна черга заявок
        buffer_protected = []  # вхідна черга захищених заявок

        downtime = 0
        buffer_size = []
        bs_protected = []
        waiting_time = []
        wt_protected = []
        deadline_over = 0
        d_protected = 0

        for tact in range(self.size):
            stream = self.check_stream(stream, buffer, buffer_protected, tact, method)

            for processor in sorted(self.processors):
                if processor.status:
                    if buffer_protected:
                        d_protected = self.check_buffer(buffer_protected, tact, processor, wt_protected, d_protected)
                    if not buffer_protected:
                        deadline_over = self.check_buffer(buffer, tact, processor, waiting_time, deadline_over)
                processor.work()

            buffer_size.append(len(buffer))
            bs_protected.append(len(buffer_protected))
            downtime += self.check_downtime(buffer, self.processors)

        self.set_variables(downtime, buffer_size, bs_protected, waiting_time, wt_protected, deadline_over, d_protected)

    def fifo(self):
        return self.scheduling()

    def rm(self):
        return self.scheduling('rm')

    def edf(self):
        return self.scheduling('edf')

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

    def set_variables(self, downtime, bs, bsp, wt, wtp, d, dp):
        self.count_tasks()
        self.downtime = downtime
        self.buffer_size = {
            'common': bs,
            'protected': bsp
        }
        self.waiting_time = {
            'common': wt,
            'protected': wtp
        }
        self.average_waiting_time = {
            'common': sum(wt) / len(wt) if wt else 0,
            'protected': sum(wtp) / len(wtp) if wtp else 0
        }
        self.deadline_over = {
            'common': d,
            'protected': dp
        }

    def show(self):
        if not self.waiting_time:
            print('Please, run algorithm before')

        awt = self.average_waiting_time['common']
        awt_p = self.average_waiting_time['protected']
        abz = sum(self.buffer_size['common']) / len(self.buffer_size['common'])
        abz_p = sum(self.buffer_size['protected']) / len(self.buffer_size['protected'])
        d = self.deadline_over['common']
        d_p = self.deadline_over['protected']
        t = self.task_amount['common']
        t_p = self.task_amount['protected']

        print('Кількість процесорів:', len(self.processors))
        print('Загальна кількість заявок:', len(self.stream), f'(звичайних: {t},  захищених: {t_p})')
        print('Середній розмір вхідної черги заявок:', abz)
        print('Середній розмір вхідної черги захищених заявок:', abz_p)
        print('Середній час очікування заявки в черзі:', round(awt, 2))
        print('Середній час очікування захищеної заявки в черзі:', round(awt_p, 2))
        print('Кількість прострочених заявок:', d)
        print('Кількість прострочених захищених заявок:', d_p)
        print('Відношення кількості прострочених заявок до загальної кількості:', round(d / t, 2))
        print('Відношення кількості прострочених захищених заявок до загальної кількості:', round(d_p / t_p, 2))
