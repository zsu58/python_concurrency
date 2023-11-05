import concurrent.futures
import logging
import time


class FakeDatabase:
  def __init__(self):
    self.value = 0

  def update(self, name):
    logging.info("Thread %s: starting update", name)
    local_copy = self.value # local_copy variable is thread-safe
    local_copy += 1 
    time.sleep(0.1) # cause the current thread to pause and allows other threads to run
    self.value = local_copy
    logging.info("Thread %s: finishing update", name)


if __name__ == "__main__":
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(
      format=format,
      level=logging.INFO,
      datefmt="%H:%M:%S"
  )

  database = FakeDatabase()
  logging.info("Testing update. Starting value is %d.", database.value)
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    for index in range(2):
      # .submit() has a signature that allows both positional and named arguments to be passed to the function running in the thread:
      # .submit(function, *args, **kwargs)
      executor.submit(database.update, index)
  logging.info("Testing update. Ending value is %d.", database.value)
  # 16:45:16: Testing update. Starting value is 0.
  # 16:45:16: Thread 0: starting update
  # 16:45:16: Thread 1: starting update
  # 16:45:16: Thread 0: finishing update
  # 16:45:16: Thread 1: finishing update
  # 16:45:16: Testing update. Ending value is 1.