import cv2
import mediapipe as mp
import enqueue

from utils import Framerate


app = enqueue.Enqueue()

app.add_queue('input', enqueue.LifoQueue, maxsize = 10)
app.add_queue('output', enqueue.LifoQueue, maxsize = 10)

framerate = Framerate()


@app.task()
def read_video(context):
  '''Read video stream.'''

  input = context.queue('input')
  capture = cv2.VideoCapture(0)

  while capture.isOpened() and not context.terminated():
    success, frame = capture.read()

    if success:
      input.put(frame)

def detect_faces(context):
  '''Detect faces.'''

  face_mesh = mp.solutions.face_mesh
  drawing_utils = mp.solutions.drawing_utils
  drawing_spec = drawing_utils.DrawingSpec(thickness = 1, circle_radius = 1)

  input = context.queue('input')
  output = context.queue('output')

  with face_mesh.FaceMesh(
      max_num_faces = 5,
      min_detection_confidence = 0.5,
      min_tracking_confidence = 0.5) as face_mesh_model:
    while not context.terminated():
      if input.empty():
        continue

      frame = cv2.cvtColor(cv2.flip(input.get(), 1), cv2.COLOR_BGR2RGB)
      frame.flags.writeable = False

      results = face_mesh_model.process(frame)

      frame.flags.writeable = True
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
          drawing_utils.draw_landmarks(
            image = frame,
            landmark_list = face_landmarks,
            connections = face_mesh.FACE_CONNECTIONS,
            landmark_drawing_spec = drawing_spec,
            connection_drawing_spec = drawing_spec)

      cv2.putText(
          frame,
          '{:.0f} fps'.format(framerate.get()),
          (10, 450),
          cv2.FONT_HERSHEY_SIMPLEX,
          1.0,
          (255, 255, 255))

      output.put(frame)

@app.task()
def detection_worker_one(context):
  '''Detection worker one.'''

  detect_faces(context)

@app.task()
def detection_worker_two(context):
  '''Detection worker two.'''

  detect_faces(context)

@app.task()
def draw_detections(context):
  '''Draw detections.'''

  output = context.queue('output')

  framerate.reset()

  while not context.terminated():
    if not output.empty():
      cv2.imshow('Face Mesh', output.get())
      framerate.update()

    if cv2.waitKey(5) & 0xFF == 27:
      context.terminate()


if __name__ == '__main__':
  app.run()
