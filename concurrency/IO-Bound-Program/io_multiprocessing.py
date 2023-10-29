import requests
import multiprocessing
import time

session = None


def set_global_session():
  # session for each process
  global session
  if not session:
    session = requests.Session()


def download_site(url):
  with session.get(url) as response:
    name = multiprocessing.current_process().name
    print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sites(sites):
  # By default, multiprocessing.Pool() will determine the number of CPUs in your computer and match that
  with multiprocessing.Pool(initializer=set_global_session) as pool:
    # The pool creates a number of separate Python interpreter processes,
    # and has each one run the specified function on some of the items in the iterable
    # The communication between the main process and the other processes is handled by the multiprocessing module

    # Since the processes doesn't share the same memory, initializer=set_global_session part creates a session for each processes
    pool.map(download_site, sites)


if __name__ == "__main__":
  # Because of the current design of CPython, and the existence of GIL(Global Interpreter Lock), the synchronous, threading, and asyncio versions of this example all run on a single CPU
  # multiprocessing in the standard library was designed to break down that barrier and run your code across multiple CPUs
  # It does this by creating a new instance of the Python interpreter to run on each CPU and then farming out part of your program to run on it
  
  # Bringing up a separate Python interpreter is not as fast as starting a new thread in the current Python interpreter
  #  It’s a heavyweight operation and comes with some restrictions and difficulties, but for the correct problem, it can make a huge difference
  sites = [
      "https://www.jython.org",
      "http://olympus.realpython.org/dice",
  ] * 80
  start_time = time.time()
  download_all_sites(sites)
  duration = time.time() - start_time
  print(f"Downloaded {len(sites)} in {duration} seconds")
  # Downloaded 160 in 4.036267042160034 seconds
