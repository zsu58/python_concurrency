import asyncio
import random

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def makerandom(idx: int, threshold: int = 6) -> int:
  # coroutine
  print(c[idx + 1] + f"Initiated makerandom({idx}).")
  i = random.randint(0, 10)
  while i <= threshold:
    print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
    await asyncio.sleep(idx + 1) # randint is CPU-bound, but with asyncio.sleep, it becomes an IO-Boundi(sh) Program
    i = random.randint(0, 10)
  print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
  return i

async def main():
  # runs the coroutine makerandom() concurrently across 3 different inputs

  # most pograms contain small, modular coroutines(i.e. makerandom()) and one wrapper function(i.e. main) to chain the coroutines together
  res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
  return res

if __name__ == "__main__":
  random.seed(444)
  r1, r2, r3 = asyncio.run(main())
  print()
  print(f"r1: {r1}, r2: {r2}, r3: {r3}")
