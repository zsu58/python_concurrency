import concurrent.futures
import logging
import threading
import time


class FakeDatabase:
  def __init__(self):
    self.value = 0
    # Allow only one thread at a time into the read-modify-write section of your code
    # Most common way to do this is called Lock in Python(in some other languages this same idea is called a mutex)

    # Only one thread at a time can have the Lock
    # Any other thread that wants the Lock must wait until the owner of the Lock gives it up

    # A thread will call my_lock.acquire() to get the lock
    # If the lock is already held, the calling thread will wait until it is released 
      # Thus, if one thread gets the lock but never gives it back the program will be stuck
    self._lock = threading.Lock()

  def locked_update(self, name):
    logging.info("Thread %s: starting update", name)
    logging.debug("Thread %s about to lock", name)
    with self._lock:
      # when used as a context manager, it gets released automatically when the with block exits
      logging.debug("Thread %s has lock", name)
      local_copy = self.value
      local_copy += 1
      time.sleep(0.1)
      self.value = local_copy
      logging.debug("Thread %s about to release lock", name)
      # the locked_update method will keep the lock until all the process in the context manager(copy(assign), update, sleep, write to the database) is done
    logging.debug("Thread %s after release", name)
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
      executor.submit(database.locked_update, index)
  logging.info("Testing update. Ending value is %d.", database.value)
  # logging.INFO
  # 17:02:15: Testing update. Starting value is 0.
  # 17:02:15: Thread 0: starting update
  # 17:02:15: Thread 1: starting update
  # 17:02:15: Thread 0: finishing update
  # 17:02:15: Thread 1: finishing update
  # 17:02:15: Testing update. Ending value is 2.

  # logging.DEBUG
  # 18:07:29: Testing update. Starting value is 0.
  # 18:07:29: Thread 0: starting update
  # 18:07:29: Thread 0 about to lock
  # 18:07:29: Thread 0 has lock
  # 18:07:29: Thread 1: starting update
  # 18:07:29: Thread 1 about to lock
  # 18:07:29: Thread 0 about to release lock
  # 18:07:29: Thread 0 after release
  # 18:07:29: Thread 1 has lock
  # 18:07:29: Thread 0: finishing update
  # 18:07:29: Thread 1 about to release lock
  # 18:07:29: Thread 1 after release
  # 18:07:29: Thread 1: finishing update
  # 18:07:29: Testing update. Ending value is 2.

  # Deadlock
  # if the Lock has already been acquired, a second call to .acquire() will wait until the thread that is holding the Lock calls .release()
  # deadlock usually happen from one of two subtle things
    # 1) An implementation bug where a Lock is not released properly
      # Using a Lock as a context manager greatly reduces the probability
    # 2) A design issue where a utility function needs to be called by functions that might or might not already have the Lock
      # Python threading has a second object, called RLock
      # RLock allows a thread to .acquire() an RLock multiple times before it calls .release()
