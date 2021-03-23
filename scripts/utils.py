from datetime import datetime
from queue import Queue
from threading import Thread

import cv2


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


class VideoStream:
  def __init__(self, source, buffer_size):
    self.__source = source
    self.__buffer_size = buffer_size

    self.__playing = False
    self.__stream = cv2.VideoCapture(self.__source)
    self.__buffer = Queue(maxsize = self.__buffer_size)

  def __update(self):
    while self.__playing:
      if not self.__buffer.full():
        success, frame = self.__stream.read()

        if success:
          self.__buffer.put(frame)
        else:
          self.__playing = False

  def source(self):
    return self.__source

  def buffer_size(self):
    return self.__buffer_size

  def is_playing(self):
    return self.__playing

  def start(self):
    self.__playing = True

    thread = Thread(target = self.__update, daemon = True)
    thread.start()

  def stop(self):
    self.__playing = False

  def get_frame(self):
    return self.__buffer.get()
