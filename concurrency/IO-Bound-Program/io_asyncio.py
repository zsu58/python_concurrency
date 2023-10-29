import asyncio
import time
import aiohttp


async def download_site(session, url):
  async with session.get(url) as response:
    print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sites(sites):
  # unlike threading, session is created as a context manager and shared in all the tasks
  # There is no way one task could interrupt another while the session is in a bad state
  async with aiohttp.ClientSession() as session:
    tasks = []
    for url in sites:
      # creates a list of tasks using asyncio.ensure_future(), which also takes care of starting them
      task = asyncio.ensure_future(download_site(session, url))
      tasks.append(task)
    # await is the magic that allows the task to hand control back to the event loop
    # When the code awaits a function call, it’s a signal that the call is likely to be something that takes a while and that the task should give up control
    # Once all the tasks are created, asyncio.gather() is used to keep the session context alive until all of the tasks have completed.
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
  # The general concept of asyncio is that a single Python object, called the event loop, controls how and when each task gets run. 
  # The event loop is aware of each task and knows what state it’s in.
  # In reality, there are many states that tasks could be in, but for now let’s imagine a simplified event loop that just has two states
  
  # The ready state will indicate that a task has work to do and is ready to be run, 
  # and the waiting state means that the task is waiting for some external thing to finish, such as a network operation.

  # The simplified event loop maintains two lists of tasks, one for each of these states. 
  # It selects one of the ready tasks and starts it back to running. 
  # That task is in complete control until it cooperatively hands the control back to the event loop.

  # When the running task gives control back to the event loop, the event loop places that task into either the ready or waiting list 
  # and then goes through each of the tasks in the waiting list to see if it has become ready by an I/O operation completing. 
  # It knows that the tasks in the ready list are still ready because it knows they haven’t run yet.

  # Once all of the tasks have been sorted into the right list again, 
  # the event loop picks the next task to run, and the process repeats.
  # The simplified event loop picks the task that has been waiting the longest and runs that.
  # This process repeats until the event loop is finished.

  # An important point of asyncio is that the tasks never give up control without intentionally doing so.
  # They never get interrupted in the middle of an operation.
  # This allows us to share resources a bit more easily in asyncio than in threading.
  # No needs to worry about making the4 code thread-safe.
  sites = [
      "https://www.jython.org",
      "http://olympus.realpython.org/dice",
  ] * 80
  start_time = time.time()
  # needs to start up the event loop and tell it which tasks to run
  # after python3.7, asyncio.run() is the counterpart
  asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
  # asyncio.run(download_all_sites(sites)) # same as above
  duration = time.time() - start_time
  print(f"Downloaded {len(sites)} sites in {duration} seconds")
  # Downloaded 160 sites in 0.913593053817749 seconds
