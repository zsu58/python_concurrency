import asyncio
import time


async def count():
  print("One")
  # the benefit of awaiting something, including asyncio.sleep(), 
  # is that the surrounding function can temporarily cede control to another function that’s more readily able to do something immediately

  # In contrast, time.sleep() or any other blocking call is incompatible with asynchronous Python code, 
  # because it will stop everything in its tracks for the duration of the sleep time
  await asyncio.sleep(1)
  print("Two")


async def main():
  # The order of this output is the heart of async IO
  # A single event loop(or coordinator) talks to each of the calls to count(),
  # When each task reaches await asyncio.sleep(1), the function yells up to the event loop and gives control back to it, saying
  # “I’m going to be sleeping for 1 second. Go ahead and let something else meaningful be done in the meantime.”
  await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
  s = time.perf_counter()
  asyncio.run(main())
  elapsed = time.perf_counter() - s
  print(f"{__file__} executed in {elapsed:0.2f} seconds.")
  # One
  # One
  # One
  # Two
  # Two
  # Two
  # /Users/zsupark/Documents/python_concurrency/asynchronous/countasync.py executed in 1.00 seconds.