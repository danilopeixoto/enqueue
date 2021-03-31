import enqueue


app = enqueue.Enqueue()

app.add_queue('input', enqueue.Queue)
app.add_queue('output', enqueue.Queue)


@app.task()
def generate_values(context):
  '''Generate and enqueue constant values.'''

  input = context.queue('input')

  while not context.terminated():
    input.put(100)

@app.task()
def double_values(context):
  '''Double and enqueue values.'''

  input = context.queue('input')
  output = context.queue('output')

  while not context.terminated():
    if not input.empty():
      output.put(input.get() * 2)

@app.task()
def print_values(context):
  '''Print double values.'''

  output = context.queue('output')

  while not context.terminated():
    if not output.empty():
      print(output.get())

    abort = input('Continue task (Yes/No)? ').lower() == 'no'

    if abort:
      context.terminate()


if __name__ == '__main__':
  app.run()
