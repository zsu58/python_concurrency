import concurrent.futures
import logging
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

  # An easier way to start up a group of threads is utilizing ThreadPoolExecutor
  # The easiest way to create it is as a context manager, using the with statement to manage the creation and destruction of the pool
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # ThreadPoolExecutor is created as a context manager, telling it how many worker threads it wants in the pool
    # It then uses .map() to step through an iterable of things, passing each one to a thread in the pool
    executor.map(thread_function, range(3))
    # The end of the with block causes the ThreadPoolExecutor to do a join() on each of the threads in the pool
    # It is strongly recommended that ThreadPoolExecutor is used as a context manager, since using the .join() method is automatically applied

  # 16:30:14: Thread 0: starting
  # 16:30:14: Thread 1: starting
  # 16:30:14: Thread 2: starting
  # 16:30:16: Thread 2: finishing
  # 16:30:16: Thread 0: finishing
  # 16:30:16: Thread 1: finishing
  # Note that Thread 2 finished ealier then Thread 0,
  # meaning that the scheduling of threads is done by the operating system and does not follow a plan that’s easy to figure out.
  # Cf. Using a ThreadPoolExecutor can cause some confusing errors, since ThreadPoolExecutor hides exception, and the program terminates with no output.
  # For example, if a function that takes no parameters, gets passed in .map(), the thread will throw an exception
