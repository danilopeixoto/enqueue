import pytest


def test_initialization(task):
  '''Test initialization.'''

  assert task.function() == None
  assert task.is_daemon() == False

def test_running(task):
  '''Test running.'''

  with pytest.raises(NotImplementedError):
    task.run(None)
