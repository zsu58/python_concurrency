import time

def count():
  print("One")
  time.sleep(1)
  print("Two")

def main():
  for _ in range(3):
    count()

if __name__ == "__main__":
  s = time.perf_counter()
  main()
  elapsed = time.perf_counter() - s
  print(f"{__file__} executed in {elapsed:0.2f} seconds.")
  # One
  # Two
  # One
  # Two
  # One
  # Two
  # /Users/zsupark/Documents/python_concurrency/asynchronous/countsync.py executed in 3.02 seconds.
