import concurrent.futures

# Each of the threads is accessing the same global variable counter and incrementing it
# However, counter is not protected in any way, so it is not thread-safe

# Because the operating system knows nothing about your code and can swap threads at any point in the execution, 
# it’s possible for this swap to happen after a thread has read the value but before it has had the chance to write it back
counter = 0


def increment_counter(fake_value):
  global counter
  for _ in range(100):
    counter += 1


if __name__ == "__main__":
  fake_data = [x for x in range(5000)]
  counter = 0
  with concurrent.futures.ThreadPoolExecutor(max_workers=5000) as executor:
    executor.map(increment_counter, fake_data)
  print(counter)