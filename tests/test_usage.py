import enqueue


def test_usage(app):
  '''Test basic usage.'''

  app.add_queue('input', enqueue.Queue)
  app.add_queue('output', enqueue.Queue)

  @app.task()
  def generate_values(context):
    input = context.queue('input')
    input.put(100)

  @app.task()
  def double_values(context):
    input = context.queue('input')
    output = context.queue('output')

    while not context.terminated():
      if not input.empty():
        output.put(input.get() * 2)
        context.terminate()

  app.run()

  output = app.queue('output')

  assert output.get(timeout = 5) == 200
  assert output.empty()
