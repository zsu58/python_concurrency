import multiprocessing
import time


def cpu_bound(number):
  return sum(i * i for i in range(number))


def find_sums(numbers):
  with multiprocessing.Pool() as pool:
    # create a multiprocessing.Pool object and use its map() method to send individual numbers to worker-processes as they become free
    # By default, the number of pools will be determined by the number of CPUs in the machine, createing a process for each one
    pool.map(cpu_bound, numbers)


if __name__ == "__main__":
  numbers = [5_000_000 + x for x in range(20)]

  start_time = time.time()
  find_sums(numbers)
  duration = time.time() - start_time
  print(f"Duration {duration} seconds")
  # Duration 2.626873016357422 seconds