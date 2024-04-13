from os import system 
import traceback
import time

from giveaway import print_file_info , reset_file

MAX = 50

reset_file("recent_urls.txt")

try:
  for j in range(1,5):
    for i in range(1,51):
      try:
        system(f"python giveaway.py {i} {j}")
        print("Nb of giveaway found " , len(print_file_info("recent_urls.txt").split("\n")))
        if len(print_file_info("recent_urls.txt").split("\n")) > 50:
          exit()
      except:
        traceback.print_exc()
        exit()
except:
  exit()
  pass