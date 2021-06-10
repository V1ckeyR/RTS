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
               f'deadline: {self.td}, ' \
               f'progress = {self.progress}, ' \
               f'protected = {self.protected}]'
