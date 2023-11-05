## Speed Up Your Python Program With Concurrency

### What is Concurrency & Parallelism?

|Concurrency Type|Switching Decision|Number of Processors|
|----------------|------------------|--------------------|
|Threading(Pre-emptive multitasking)|The operating system decides when to switch tasks external to Python|1|
|Asyncio(Cooperative multitasking)|The tasks decide when to give up control|1|
|Multiprocessing|The processes all run at the same time on different processors|Many|

* In threading, the operating system actually knows about each thread and can interrupt it at any time to start running a different thread. This is called `pre-emptive multitasking` since the operating system can pre-empt your thread to make the switch
  * Pros: Pre-emptive multitasking is handy in that the code in the thread doesn’t need to do anything to make the switch. 
  * Cons: It can also be difficult because of that “at any time” phrase.
* Asyncio, on the other hand, uses cooperative multitasking. The tasks must cooperate by announcing when they are ready to be switched out.
  * Pros: The benefit of doing this extra work up front is that you always know where your task will be swapped out.
  * Cons: The code in the task has to change slightly to make the switching happen
* With multiprocessing, each of the process can run on a different core. Running on a different core means that they actually can run at the same time.

---

### When Is Concurrency Useful?
* Concurrency can make a big difference for either or `I/O-bound` or `CPU-bound` problems
  * `I/O-bound`: I/O-bound problems cause your program to slow down because it frequently must wait for input/output (I/O) from some external resources(e.g. printer, hard-drive, etc.), thus speeding it up  involves overlapping the times spent waiting for these devices
  * `CPU-bound`: CPU-bound programs, because the resource limiting the speed of your program is the CPU, not the network or the file system, thus speeding it up involves finding ways to do more computations in the same amount of time.

---

### How to Speed Up an I/O-Bound Program

#### Synchronous Version
* [🔗 Synchronous Code](https://github.com/zsu58/python_concurrency/tree/main/concurrency/IO-Bound-Program/io_synchronous.py)

#### Threading Version
* [🔗 Threading Code](https://github.com/zsu58/python_concurrency/tree/main/concurrency/IO-Bound-Program/io_threading.py)

#### Asyncio Version
* [🔗 Asyncio Code](https://github.com/zsu58/python_concurrency/tree/main/concurrency/IO-Bound-Program/io_asyncio.py)

#### Multiprocessing Version
* [🔗 Multiprocessing Code](https://github.com/zsu58/python_concurrency/tree/main/concurrency/IO-Bound-Program/io_multiprocessing.py)

---

### How to Speed Up a CPU-Bound Program

#### Synchronous Version
* [🔗 Synchronous Code](https://github.com/zsu58/python_concurrency/tree/main/concurrency/CPU-Bound-Program/cpu_synchronous.py)

#### Multiprocessing Version
* [🔗 Multiprocessing Code](https://github.com/zsu58/python_concurrency/tree/main/concurrency/CPU-Bound-Program/cpu_multiprocessing.py)

---

### When to Use Concurrency
* 1) Decide whether a concurrency module is needed
* 2) Figure out whether the program is I/O-bound or CPU-bound
  * I/O-bound: Use asyncio when possible, threading when required
    * critical libraries that have not been ported to take advantage of asyncio
    * when any task that doesn’t give up control to the event loop will block all of the other tasks
  * CPU-bound: use multiprocessing, threading and asyncio doesn't help

---

### Reference
* [🔗 Python Concurrency](https://realpython.com/python-concurrency/)

---
