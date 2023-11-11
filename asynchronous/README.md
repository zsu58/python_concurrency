## Async IO in Python: A Complete Walkthrough

### The 10,000-Foot View of Async IO
* `Parallelism`
  * Performing multiple operations at the same time
  * Multiprocessing is a means to effect parallelism(a form of parallelism), and it entails spreading tasks over a computer’s CPU
  * A specific type(subset) of concurrency
* `Concurrency`
  * A slightly broader term than parallelism, it suggests that multiple tasks have the ability to run in an overlapping manner
  * (There’s a saying that concurrency does not imply parallelism)
  * Encompasses both multiprocessing (ideal for CPU-bound tasks) and threading (suited for IO-bound tasks)
* `Threading`
  * A concurrent execution model whereby multiple threads take turns executing tasks
* `Asynchronous IO`
  * Built in `CPython`, enabled through the standard library’s asyncio package and the new async and await language keywords
  * Has existed or is being built into other languages and runtime environments, such as Go, C#, or Scala
  * A library to write concurrent code, but is not threading, nor is it multiprocessing(and not built on top of either of these)
  * A single-threaded, single-process design, using cooperative multitasking, but it is not parallelism.
  * More closely aligned with threading than with multiprocessing but is very much distinct from both of these and is a standalone member in concurrency’s bag of tricks
  * Coroutines (a central feature of async IO) can be scheduled concurrently, but they are not inherently concurrent
  * Asynchronous routines are able to `pause` while waiting on their ultimate result and let other routines run in the meantime
  * Asynchronous code, through the mechanism above, facilitates concurrent execution(i.e. asynchronous code gives the look and feel of concurrency)

---

### The asyncio Package and async/await
* `coroutine`
  * A specialized version of a Python generator function
  * A function that can suspend its execution before reaching return, and it can indirectly pass control to another coroutine for some time

```bash
python3 countasync.py

python3 countsync.py
```

---

### The Rules of Async IO
* `async`: a native coroutine or an asynchronous generator
  * `async with`, `async for` are also valid
* `await`: passes function control back to the event loop(It suspends the execution of the surrounding coroutine)
  * If python encounter an `await f()` expression in the scope of `g()`, `await` tells the event loop, "Suspend execution of `g()` until the result of `f()` is returned. Until then run something else"
  * In code it is roughly as below

```python
async def g():
  print("start of g()")
  r = await f() # Pause here and come back to g() when f() is done
  return r
```

#### Rules
* A function with `async def` is a coroutine, which may use `await`, `return`, `yield`, or `pass`
* Using `await` and/or `return` creates a coroutine function
  * To call a coroutine function, `await` should be used to get its results
* It it less common(only recently legal in Pyton) to use `yield` in an `async def` block.
  * This creates an asynchronous generator, iterated over with `async for`
* `async def` can not use `yield from`
* `await` can be used only insde a `async def` coroutine
* When using `await f()`, f() should be an `awaitable` object
  * awaitable object is either `another coroutine` or an object defining an `.__await__()` method returning an iterator
* Marking a functino as a coroutine can be done in two ways, decorating a normal function with `@asyncio.coroutine`(generator-based coroutine) or using `async def`(native coroutine)
  * These are essentially equivalent, but it is recommended to use native coroutine(generator-based coroutine will be removed from Python3.10)

```python
async def f(x):
  # ok, since `await` and `return ` is allowed in coroutines
  y = await z(x)
  return y

async def g(x):
  # ok, an async generator
  yield x

async def m(x):
  # no, SyntaxError
  yield from gen(x)

def m(x):
  # no, `await` should be inside `async def` block
  y = await(z)
  return y
```

```bash
python3 rand.py
```

---

### Async IO Design Patterns
#### Chaining Coroutines
* A key feature of coroutines is that they can be chained together, allowing break programs into smaller, manageable, recyclable coroutines

```bash
python3 chain.py
```

#### Using a Queue
* Using a queue class provided in `asyncio package`
* In this structure a number of producers which are not associated with each other, can add multiple items to the queue at random, unannounced times
* Consumers pull items from the queue as they show up, greedily and without waiting for any other signal
* There is no chaining of any individual consumer to a producer, meaning that consumers don’t know the number of producers, or even the cumulative number of items that will be added to the queue, in advance.
* It takes an individual producer or consumer a variable amount of time to put and extract items from the queue, respectively. 
* The queue serves as a throughput that can communicate with the producers and consumers without them talking to each other directly.

```bash
python3 queue.py -p 2 -c 5
```


### Reference
* [🔗 Python Async-IO](https://realpython.com/async-io-python/)

---
