from datetime import timedelta as Delta, datetime
import time

_start = None

def start():
  global _start
  _start = time.monotonic()

def stop():
  _stop = time.monotonic()
  midnight = datetime(2000, 1, 1)
  adjusted = midnight + Delta(seconds=_stop - _start)
  return adjusted.strftime("%M:%S")
