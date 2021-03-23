import cv2
import mediapipe as mp

from utils import Framerate, VideoStream


def main():
  '''Read video stream, detect faces and draw detections.'''

  face_mesh = mp.solutions.face_mesh
  drawing_utils = mp.solutions.drawing_utils
  drawing_spec = drawing_utils.DrawingSpec(thickness = 1, circle_radius = 1)

  framerate = Framerate()
  video_stream = VideoStream(source = 0, buffer_size = 100)

  with face_mesh.FaceMesh(
      max_num_faces = 5,
      min_detection_confidence = 0.5,
      min_tracking_confidence = 0.5) as face_mesh_model:
    framerate.reset()
    video_stream.start()

    while video_stream.is_playing():
      frame = video_stream.get_frame()

      frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
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

      cv2.imshow('Face Mesh', frame)

      framerate.update()

      if cv2.waitKey(5) & 0xFF == 27:
        video_stream.stop()
        cv2.destroyAllWindows()

        break


if __name__ == '__main__':
  main()
