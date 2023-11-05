import concurrent.futures
import logging
import queue
import random
import threading
import time


def producer(pipeline, event):
  """Pretend we're getting a message from the network."""
  while not event.is_set():
    message = random.randint(1, 101)
    logging.info("Producer got message: %s", message)
    pipeline.set_message(message, "Producer")

  logging.info("Producer received EXIT event. Exiting")


def consumer(pipeline, event):
  """Pretend we're saving a number in the database."""
  while not event.is_set() or not pipeline.empty():
    message = pipeline.get_message("Consumer")
    logging.info(
        "Consumer storing message: %s  (queue size=%s)",
        message,
        pipeline.qsize(),
    )

  logging.info("Consumer received EXIT event. Exiting")


class Pipeline(queue.Queue):
  # Queue is thread-safe, therefore the locking happens inside the Queue itself
  def __init__(self):
    # The parameter maxsize will limit the queue to that number of elements,
    # causing .put() to block until there are fewer than maxsize elements
    
    # If maxsize is not set, then the queue will grow to the limits of the computer’s memory.
    super().__init__(maxsize=10)

  def get_message(self, name):
    logging.debug("%s:about to get from queue", name)
    value = self.get()
    logging.debug("%s:got %d from queue", name, value)
    return value

  def set_message(self, value, name):
    logging.debug("%s:about to add %d to queue", name, value)
    self.put(value)
    logging.debug("%s:added %d to queue", name, value)


if __name__ == "__main__":
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(
      format=format,
      level=logging.INFO,
      datefmt="%H:%M:%S"
  )
  # logging.getLogger().setLevel(logging.DEBUG)

  pipeline = Pipeline()
  # Queue can be used directly as a pipeline object
  # pipeline = queue.Queue(maxsize=10)
  event = threading.Event()
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(producer, pipeline, event)
    executor.submit(consumer, pipeline, event)

    time.sleep(0.1)
    logging.info("Main: about to set event")
    event.set()
