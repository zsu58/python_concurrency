import asyncio
import itertools as it
import os
import random
import time

async def makeitem(size: int = 5) -> str:
  return os.urandom(size).hex()

async def randsleep(caller=None) -> None:
  i = random.randint(0, 10)
  if caller:
    print(f"{caller} sleeping for {i} seconds.")
  await asyncio.sleep(i)

async def produce(name: int, q: asyncio.Queue) -> None:
  n = random.randint(0, 10)
  for _ in it.repeat(None, n):  # Synchronous loop for each single producer
    await randsleep(caller=f"Producer {name}")
    i = await makeitem()
    t = time.perf_counter()
    await q.put((i, t))
    print(f"Producer {name} added <{i}> to queue.")

async def consume(name: int, q: asyncio.Queue) -> None:
  while True:
    await randsleep(caller=f"Consumer {name}")
    i, t = await q.get()
    now = time.perf_counter()
    print(
        f"Consumer {name} got element <{i}>"
        f" in {now-t:0.5f} seconds."
    )
    q.task_done()

async def main(nprod: int, ncon: int):
  q = asyncio.Queue()
  producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
  consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
  await asyncio.gather(*producers)
  await q.join()  # Implicitly awaits consumers, too
  for c in consumers:
    c.cancel()

if __name__ == "__main__":
  import argparse
  random.seed(444)
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--nprod", type=int, default=5)
  parser.add_argument("-c", "--ncon", type=int, default=10)
  ns = parser.parse_args()
  start = time.perf_counter()
  asyncio.run(main(**ns.__dict__))
  elapsed = time.perf_counter() - start
  print(f"Program completed in {elapsed:0.5f} seconds.")
  # Producer 0 sleeping for 4 seconds.
  # Consumer 0 sleeping for 4 seconds.
  # Consumer 1 sleeping for 7 seconds.
  # Consumer 2 sleeping for 4 seconds.
  # Consumer 3 sleeping for 4 seconds.
  # Consumer 4 sleeping for 8 seconds.
  # Producer 0 added <440447c82f> to queue.
  # Producer 0 sleeping for 10 seconds.
  # Consumer 0 got element <440447c82f> in 0.00022 seconds.
  # Consumer 0 sleeping for 7 seconds.
  # Producer 0 added <82f04379d1> to queue.
  # Producer 0 sleeping for 8 seconds.
  # Consumer 2 got element <82f04379d1> in 0.00034 seconds.
  # Consumer 2 sleeping for 4 seconds.
  # Producer 0 added <a4568d2cb8> to queue.
  # Producer 0 sleeping for 7 seconds.
  # Consumer 3 got element <a4568d2cb8> in 0.00017 seconds.
  # Consumer 3 sleeping for 1 seconds.
  # Producer 0 added <6279dcdf5f> to queue.
  # Consumer 1 got element <6279dcdf5f> in 0.00024 seconds.
  # Consumer 1 sleeping for 6 seconds.
  # Program completed in 29.00951 seconds.
