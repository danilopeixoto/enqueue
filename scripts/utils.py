from datetime import datetime


class Framerate:
  '''Framerate estimation.'''

  def __init__(self):
    '''Initialize metrics.'''

    self.reset()

  def reset(self):
    '''Reset metrics.'''

    self.__start_time = datetime.now()
    self.__count = 0

  def update(self):
    '''Increment count metric.'''

    self.__count += 1

  def get(self):
    '''Return framerate estimation.'''

    elapsed_time = (datetime.now() - self.__start_time).total_seconds()

    return self.__count / elapsed_time if elapsed_time > 0 else 0
