class Processor:
    """
    Клас, в якому зберігається стан процесора
    """
    def __init__(self, number):
        self.number = number
        self.status = 1  # 0 - busy, 1 - free
        self.task = None
        self.completed = 0

    def set_task(self, task):
        self.status = 0
        self.task = task

    def work(self):
        if self.task:
            self.task.progress -= 1
            if not self.task.progress:  # Finish work
                self.task.progress = self.task.to  # Return task progress to initial status
                self.status = 1
                self.task = None
                self.completed += 1

    def clear(self):
        self.status = 1
        self.task = None
        self.completed = 0

    def __lt__(self, other):
        return self.completed < other.completed

    def __repr__(self):
        return f"Processor {self.number} completed {self.completed} tasks"
