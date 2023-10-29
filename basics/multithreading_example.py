import threading
import os


def foo():
  print("foo: thread id is", threading.get_native_id())
  print("foo: my pid is", os.getpid())


def bar():
  print("bar: thread id is", threading.get_native_id())
  print("bar: my pid is", os.getpid())


def baz():
  print("baz: thread id is", threading.get_native_id())
  print("baz: my pid is", os.getpid())


if __name__ == "__main__":
  print("my pid is", os.getpid())
  thread1 = threading.Thread(target=foo).start()
  thread2 = threading.Thread(target=bar).start()
  thread3 = threading.Thread(target=baz).start()
