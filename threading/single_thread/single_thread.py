import logging
import threading
import time

def thread_function(name):
  logging.info("Thread %s: starting", name)
  time.sleep(2)
  logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(
      format=format, 
      level=logging.INFO,
      datefmt="%H:%M:%S"
  )

  logging.info("Main    : before creating thread")
  x = threading.Thread(target=thread_function, args=(1,))
  logging.info("Main    : before running thread")
  x.start()
  logging.info("Main    : wait for the thread to finish")
  # x.join()
  logging.info("Main    : all done")
  # 16:00:52: Main    : before creating thread
  # 16:00:52: Main    : before running thread
  # 16:00:52: Thread 1: starting
  # 16:00:52: Main    : wait for the thread to finish
  # 16:00:52: Main    : all done
  # 16:00:54: Thread 1: finishing
