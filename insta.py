from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import os.path
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import traceback
from random import randint
import undetected_chromedriver as uc 
import pickle
import os
import emoji

import yaml

class Scraper:
    
    wait_time = 5
    
    options = uc.ChromeOptions() 
    options.add_experimental_option(
    "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
    #options.add_argument('headless')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    options.add_argument(f'--user-agent={ua}') 
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    login_link = "https://chat.openai.com/auth/login"
    emailxpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input"
    passwordxpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input"
    accept_coockie_xpath = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]"
    refuse_coockie_xpath = "/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
    connect_btn_xpath="/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div"
    with open("configuration.yml", "r") as file:
      data = yaml.load(file, Loader=yaml.FullLoader)
    
    account_email_or_username = data["account_email_or_username"]
    account_password = data["account_password"]

def login(S,username,password):
    try:
      S.driver.implicitly_wait(15)
      S.driver.get("https://www.instagram.com/")
      
      try:
        element = WebDriverWait(S.driver, 5).until(
          EC.presence_of_element_located((By.XPATH, S.accept_coockie_xpath)))
      except:
        element = WebDriverWait(S.driver, 5).until(
          EC.presence_of_element_located((By.XPATH, S.refuse_coockie_xpath)))
      
      element.click()

      time.sleep(2)
      element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.XPATH, S.emailxpath)))
      element.click()
      time.sleep(2)
      element.send_keys(username)

      element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.XPATH, S.passwordxpath)))
      element.click()
      time.sleep(2)
      element.send_keys(password)

      element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.XPATH, S.connect_btn_xpath)))
      element.click()
      time.sleep(5)
      
      print("Login done")
      time.sleep(5)
    except:
       print("Login not done wrong username/password check it on the configuration.yml file")
       time.sleep(5)
       exit()

def like_a_post(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)
    element = WebDriverWait(S.driver, 15).until(
      EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]/div[1]/span[1]/div/div")))
    element.click()
    time.sleep(2)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref like")
        
def comment_a_post(S,url,text):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)
    element = WebDriverWait(S.driver, 15).until(
      EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea")))
    time.sleep(3)
    element.click()
    time.sleep(3)
    # S.driver.execute_script("arguments[0].scrollIntoView();", element)
    # element.send_keys(text)

    S.driver.switch_to.active_element.send_keys(text)
    element = WebDriverWait(S.driver, 15).until(
      EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/div[2]/div")))
    element.click()

    time.sleep(2)
    print("comment done")
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref comment")

def follow_an_user(S,user):
   
  try:
    S.driver.implicitly_wait(15)
    S.driver.get("https://www.instagram.com/" + user + "/")

    try:
      button_follow = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Suivre')]")))      
      button_follow.click()
      print("You have followed an another account " , user)
    except:
       print("You already follow the account")
    time.sleep(3)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref follow")
        traceback.print_exc()


def save_a_post(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)

    try:
      element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Enregistrer']")))      
      element.click()
    except:
       print("You have already saved the post")
    time.sleep(3)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref save")
        traceback.print_exc()

def get_tweet_text(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)
    element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/span")))      
    time.sleep(3)
    return (element.text)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return("")
     else:
        print("Bref text")
        return("")


def get_tweet_user(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)
    element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/div/span[1]/div/a/div/div/span")))      
    time.sleep(3)
    return (element.text)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return("")
     else:
        print("Bref text user")
        return("")

def save_coockie(selenium_session):
    pickle.dump(selenium_session.driver.get_cookies(), open(f"cookies.pkl", "wb"))

def print_pkl_info():
    file_path = f"cookies.pkl"
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return (data)

def instabot():
  S = Scraper()
  # try:
  #   #a = 10/0
  #   ck = print_pkl_info()
  #   if len(str(ck)) > 5:
  #     S.driver.implicitly_wait(15)
  #     S.driver.get("https://www.instagram.com/")
  #     try:
  #       element = WebDriverWait(S.driver, 15).until(
  #         EC.presence_of_element_located((By.XPATH, S.accept_coockie_xpath)))
  #     except:
  #       element = WebDriverWait(S.driver, 15).until(
  #         EC.presence_of_element_located((By.XPATH, S.refuse_coockie_xpath)))
    
  #     element.click()
  #     cookies = pickle.load(open(f"cookies.pkl","rb"))
  #     for cookie in cookies:
  #         S.driver.add_cookie(cookie)
  #     time.sleep(0.2)
  #     time.sleep(5)
  #     comment_a_post(S,"https://www.instagram.com/p/C5OopjjsM3m/","conndedede ded dard")
  #     time.sleep(10000)
  # except:
  #   print("fin bref")
  #   login(S,"totogaming1010","steeven1")
  #   comment_a_post(S,"https://www.instagram.com/p/C5OopjjsM3m/","conndedede ded dard")
  #   save_coockie(S)
  #   time.sleep(10000)
  
  login(S,"totogaming1010","steeven1")
  get_tweet_user(S,"https://www.instagram.com/p/C5OopjjsM3m/")
  time.sleep(10000)
  pass