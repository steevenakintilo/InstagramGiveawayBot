from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import os.path

import pickle
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
import traceback
import yaml
from random import randint
import random

import traceback
from selenium.webdriver.common.keys import Keys  

import sys 


MINTIME = 0
MAXTIME = 0

class Scraper:
    
    wait_time = 5
    options = webdriver.FirefoxOptions()
    options.add_argument('headless')
    options.add_argument("--log-level=3")  # Suppress all logging levels
    driver = webdriver.Firefox(options=options)


def write_into_file(path, x):
    with open(path, "a") as f:
        f.write(str(x))

def print_file_info(path):
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return(content)

def reset_file(path):  
    f = open(path, "w")
    f.write("")    
    f.close  

def insta_giveaway(S,i,page_nb):
    urls = []
    file_urls = print_file_info("urls.txt").split("\n")
    S.driver.get(f"https://www.jeu-concours.biz/concours-instagram.php?page={page_nb}")
    cookiesbtn = "/html/body/div[14]/div[2]/div[1]/div[2]/div[2]/button[1]/p"
    element =  WebDriverWait(S.driver,3).until(
        EC.presence_of_element_located((By.XPATH, cookiesbtn)))

    element.click()
    time.sleep(1)
    ggw = f"/html/body/section/div/div/div[1]/div[2]/article[{str(i)}]/nav/ul/li[4]/a"
    element =  WebDriverWait(S.driver,5).until(
        EC.presence_of_element_located((By.XPATH, ggw)))
    
    S.driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(0.5)
    element.click()

    new_window = S.driver.window_handles[-1]
    S.driver.switch_to.window(new_window)
    time.sleep(2)

    new_window_url = S.driver.current_url

    if new_window_url not in urls and new_window_url not in file_urls:
       write_into_file("urls.txt",new_window_url + "\n")
       urls.append(new_window_url)

    # Close the new window
    S.driver.close()

    # Switch back to the original window if needed
    original_window = S.driver.window_handles[0]
    S.driver.switch_to.window(original_window)

    time.sleep(2)


def fck():
  try:
    S = Scraper()
    nb = int(sys.argv[2])
    insta_giveaway(S,int(sys.argv[1]),nb)
    S.driver.close()
  except:
    S.driver.close()

fck()
