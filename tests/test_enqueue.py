import enqueue


def test_initialization(app):
  '''Test initialization.'''

  assert app.terminated() == False
  assert app.queues() == {}
  assert app.tasks() == set()

def test_termination(app):
  '''Test termination.'''

  app.terminate()

  assert app.terminated() == True

def test_queues(app):
  '''Test queues.'''

  app.add_queue('queue', enqueue.Queue)
  assert app.has_queue('queue')

  queue = app.queue('queue')
  assert type(queue) == enqueue.Queue

  app.remove_queue('queue')
  assert app.has_queue('queue') == False

def test_tasks(app):
  '''Test tasks.'''

  task = app.add_task(enqueue.Task)
  assert app.has_task(task)

  app.remove_task(task)
  assert app.has_task(task) == False

def test_task_execution(app):
  '''Test task execution.'''

  app.add_queue('queue', enqueue.Queue)

  @app.task()
  def generate_values(context):
    input = context.queue('queue')
    input.put(100)

  app.run()

  queue = app.queue('queue')

  assert queue.get(timeout = 5) == 100
  assert queue.empty()
