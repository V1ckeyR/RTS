from numpy.random import poisson

from scheduler.task import Task


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
