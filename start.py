from os import system 
import traceback
import time

from giveaway import print_file_info , reset_file
from os import system

from random import randint

MAX = 11

def start():
  reset_file("recent_urls.txt")
  try:
    for j in range(1,5):
      for i in range(1,51):
        try:
          system(f"python giveaway.py {i} {j}")
          print("Nb of giveaway found " , len(print_file_info("recent_urls.txt").split("\n")))
          if len(print_file_info("recent_urls.txt").split("\n")) >= MAX:
            return(True)
        except:
          traceback.print_exc()
          return(True)
  except:
    return(False)
    pass

print("1")
start()
system("python main.py")
print("Sleeping Zzzz...")
time.sleep((3600) * 10 - randint(0,1000))
print("2")
start()
system("python main.py")

