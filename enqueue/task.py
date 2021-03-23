class Task:
  '''Task metadata.'''

  def __init__(self, function = None, daemon = False):
    '''Initialize task metadata.'''

    self.__function = function
    self.__daemon = daemon

  def function(self):
    '''Return function.'''

    return self.__function

  def is_daemon(self):
    '''Return true if task is daemon, false otherwise.'''

    return self.__daemon

  def run(self, context):
    '''Run function if it exists or raise not implemented error.'''

    if self.__function is None:
      raise NotImplementedError
    else:
      self.__function(context)
