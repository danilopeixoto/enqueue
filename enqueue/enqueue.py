from threading import Thread

from .task import Task


class Enqueue:
  '''Enqueue application.'''

  def __init__(self):
    '''Initialize application.'''

    self.__terminated = False
    self.__queues = {}
    self.__tasks = []

  def terminate(self):
    '''Set application to terminate tasks.'''

    self.__terminated = True

  def terminated(self):
    '''Return true if the application is terminated, false otherwise.'''

    return self.__terminated

  def add_queue(self, name, queue_type, *args, **kwargs):
    '''Add queue by name.'''

    self.__queues[name] = queue_type(*args, **kwargs)

  def remove_queue(self, name):
    '''Remove queue by name'''

    self.__queues.pop(name)

  def has_queue(self, name):
    '''Return true if the queue exists, false otherwise.'''

    return name in self.__queues.keys()

  def queue(self, name):
    '''Return queue by name.'''

    return self.__queues.get(name)

  def queues(self):
    '''Return queue map.'''

    return self.__queues

  def add_task(self, task_type, *args, **kwargs):
    '''Add task and return the object reference.'''

    task = task_type(*args, **kwargs)
    self.__tasks.append(task)

    return task

  def remove_task(self, task):
    '''Remove task.'''

    self.__tasks.remove(task)

  def has_task(self, task):
    '''Return true if task exists, false otherwise.'''

    return task in self.__tasks

  def task(self, daemon = False):
    '''Task decorator.'''

    def decorator(function):
      self.add_task(Task, function, daemon)

      return function

    return decorator

  def tasks(self):
    '''Return task list.'''

    return self.__tasks

  def run(self):
    '''Run tasks.'''

    threads = map(
      lambda task: Thread(
        target = task.run,
        args = (self,),
        daemon = task.is_daemon()),
      self.__tasks)

    for thread in threads:
      thread.start()

    for thread in threads:
      if not thread.isDaemon():
        thread.join()
