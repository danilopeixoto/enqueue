import enqueue
import pytest


@pytest.fixture
def app():
  '''Return application.'''

  return enqueue.Enqueue()

@pytest.fixture
def task():
  '''Return task.'''

  return enqueue.Task()
