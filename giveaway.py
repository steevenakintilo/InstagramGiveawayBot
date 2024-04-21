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

import undetected_chromedriver as uc 


import traceback
from selenium.webdriver.common.keys import Keys  

import sys 
import logging
import pandas as pd

MINTIME = 0
MAXTIME = 0

class Scraper:
    
    wait_time = 5
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppress all logging levels
    options.add_argument('headless')    
    driver = webdriver.Chrome(options=options)  # to open the chromedriver    
    
    
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
    insta_url = "G:/Mon Drive/bot/data_insta.csv"

    urls = []
    file_urls = print_file_info("url.txt").split("\n")
    S.driver.get(f"https://www.jeu-concours.biz/concours-instagram.php?page={page_nb}")
    cookiesbtn = "/html/body/div[14]/div[2]/div[1]/div[2]/div[2]/button[1]/p"
    try:
        element =  WebDriverWait(S.driver,7).until(
            EC.presence_of_element_located((By.XPATH, cookiesbtn)))
        element.click()
    
    except:
       time.sleep(1)
       S.driver.refresh()
       element =  WebDriverWait(S.driver,7).until(
            EC.presence_of_element_located((By.XPATH, cookiesbtn)))
       element.click()
    
       
    time.sleep(0.1)
    giveaway_xpath = f"/html/body/section/div/div/div[1]/div[2]/article[{str(i)}]/nav/ul/li[4]/a"
    element =  WebDriverWait(S.driver,15).until(
        EC.presence_of_element_located((By.XPATH, giveaway_xpath)))
    
    S.driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(0.1)
    element.click()

    new_window = S.driver.window_handles[-1]
    S.driver.switch_to.window(new_window)
    time.sleep(0.1)

    new_window_url = S.driver.current_url
    last = new_window_url[:-1]
    lastchar = new_window[-1]
    split_url = new_window_url.split("/")
    last_split_elem = split_url[-2].replace("/","")
    if new_window_url not in urls and new_window_url not in file_urls and last not in urls and last not in file_urls and last_split_elem not in urls and last_split_elem not in file_urls: 
        write_into_file("url.txt",new_window_url + "\n")
        write_into_file("recent_urls.txt",new_window_url + "\n")
        urls.append(new_window_url)

    S.driver.close()

    original_window = S.driver.window_handles[0]
    S.driver.switch_to.window(original_window)

def giveaway_launcher():
  try:
    S = Scraper()
    nb = int(sys.argv[2])
    insta_giveaway(S,int(sys.argv[1]),nb)
    S.driver.close()
  except:
    S.driver.close()
    pass
    

giveaway_launcher()