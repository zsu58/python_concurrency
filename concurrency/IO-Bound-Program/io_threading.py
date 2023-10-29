import concurrent.futures
import requests
import threading
import time

# you only want to create one of these objects, not one for each thread. 
# The object itself takes care of separating accesses from different threads to different data.
thread_local = threading.local()


def get_session():
  # For each thread, a separate Session is needed,
  # because the operating system is in control of when the task gets interrupted and another task starts, 
  # any data that is shared between the threads needs to be protected, or thread-safe

  # There are several strategies for making data accesses thread-safe depending on what the data is and how you’re using it. 
  # One of them is to use thread-safe data structures like Queue from Python’s queue module.
  # These objects use low-level primitives like threading.Lock to ensure that only one thread can access a block of code or a bit of memory at the same time
  # This code is using this strategy indirectly by way of the ThreadPoolExecutor object.

  # Another strategy to use here is something called thread local storage. 
  # threading.local() creates an object that looks like a global but is specific to each individual thread

  # If the programmer has not sufficiently protected data accesses to prevent threads from interfering with each other,
  # it can lead to subtle bugs called "race conditions"
  if not hasattr(thread_local, "session"):
    thread_local.session = requests.Session()
  return thread_local.session


def download_site(url):
  session = get_session()
  with session.get(url) as response:
    print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
  # Thread: 
  # Pool: This object is going to create a pool of threads, each of which can run concurrently
  # Executor: the Executor is the part that’s going to control how and when each of the threads in the pool will run
  # An executor is a higher-level abstraction, that manage many of the details when fine-grained details aren't needed
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_site, sites)


if __name__ == "__main__":
  sites = [
      "https://www.jython.org",
      "http://olympus.realpython.org/dice",
  ] * 80
  start_time = time.time()
  download_all_sites(sites)
  duration = time.time() - start_time
  print(f"Downloaded {len(sites)} in {duration} seconds")
  # Downloaded 160 in 3.974519729614258 seconds
