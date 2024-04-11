from os import system 
import traceback
import time

try:
  for j in range(1,5):
    for i in range(1,51):
      try:
        system(f"python search.py {i} {j}")
      except:
        traceback.print_exc()
except:
  pass