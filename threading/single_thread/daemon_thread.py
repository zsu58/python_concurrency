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
  # In computer science, a daemon is a process that runs in the background
  # In Python threading, A daemon thread will shut down immediately when the program exits

  # If a program is running Threads that are not daemons, then the program will wait for those threads to complete before it terminates
  # Threads that are daemons, however, are just killed wherever they are when the program is exiting

  # When Python program ends, part of the shutdown process is to clean up the threading routine,
  # and when the threads are non-daemonic Pythonn will wait the threads to complete
    # https://github.com/python/cpython/blob/df5cdc11123a35065bbf1636251447d0bfe789a5/Lib/threading.py#L1263
    # Threading._shutdown() walks through all of the running threads and calls .join() on every one that does not have the daemon flag set

  # unlike the sinlge_thread program, thread_function() did not get a chance to complete, since it was a daemon thread killed when the program exited
  x = threading.Thread(target=thread_function, args=(1,), daemon=True)
  logging.info("Main    : before running thread")
  x.start()
  logging.info("Main    : wait for the thread to finish")
  # x.join() # when uncommented, the main thread waits for the x thread
  logging.info("Main    : all done")
  # 16:01:15: Main    : before creating thread
  # 16:01:15: Main    : before running thread
  # 16:01:15: Thread 1: starting
  # 16:01:15: Main    : wait for the thread to finish
  # 16:01:15: Main    : all done
