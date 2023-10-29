from multiprocessing import Process
import os

def foo() -> None:
  print("foo: child process is", os.getpid())
  print("foo: parent process is", os.getppid())

def bar() -> None:
  print("bar: child process is", os.getpid())
  print("bar: parent process is", os.getppid())

def baz() -> None:
  print("baz: child process is", os.getpid())
  print("baz: parent process is", os.getppid())

if __name__ == "__main__":
  print("parent process:", os.getpid())
  child1 = Process(target=foo).start()
  child2 = Process(target=bar).start()
  child3 = Process(target=baz).start()

