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
import json

import emoji

from search import giveaway_from_url_file , get_list_of_comment_of_a_post
import yaml

class Scraper:
    
    wait_time = 5
    
    options = uc.ChromeOptions() 
    options.add_experimental_option(
    "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
    options.add_argument('headless')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    options.add_argument(f'--user-agent={ua}') 
    #options.add_argument("chrome.switches")
    options.add_argument("--disable-extensions")
    #chromeProfilePath = r"C:\Users\sakin\AppData\Local\Google\Chrome\User Data\Profile "
    
    #options.add_argument("user-data-dir=" + chromeProfilePath)
    
    
    #options.add_argument(r"--user-data-dir=C:\Users\sakin\AppData\Local\Google\Chrome\User Data\Profile 3")
    #options.add_argument(r'--profile-directory=Profile 3')
    
    #options.add_argument(r'--profile-directory=Profile ' + str(profiles))

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

def print_file_info(path):
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return(content)

def login(S,username,password):
    try:
      S.driver.implicitly_wait(15)
      S.driver.get("https://www.instagram.com/")
      #time.sleep(1000000)
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
      time.sleep(10)
    except:
       print("Login not done wrong username/password check it on the configuration.yml file")
       time.sleep(5)
       exit()

def like_a_post(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)
    time.sleep(2.5)
    try:     
        element = WebDriverWait(S.driver, 5).until(
        EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]/div[1]/span[1]/div/div/span")))
        S.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2.5)
        actions = ActionChains(S.driver)

        actions.move_to_element(element).click().perform()
        time.sleep(0.2)
        actions.move_to_element(element).click().perform()
        time.sleep(0.2)
        actions.move_to_element(element).click().perform()
        time.sleep(0.2)
        actions.move_to_element(element).click().perform()
        
        time.sleep(2.5)
        return True
    except:
       return True
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return True
     else:
        print("Bref like")
        return True
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
    return True
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref comment")
        return False

def follow_an_user(S,user,mode):
   
  try:
    S.driver.implicitly_wait(15)
    S.driver.get("https://www.instagram.com/" + user + "/")

    try:
      if mode == 1:
        button_follow = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Suivre')]")))      
        S.driver.execute_script("arguments[0].scrollIntoView();", button_follow)
        button_follow.click()

      else:
        button_follow = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Suivre')]")))      
        S.driver.execute_script("arguments[0].scrollIntoView();", button_follow)
        time.sleep(5)
        actions = ActionChains(S.driver)
        actions.move_to_element(button_follow).click().perform()

      print("You have followed an another account " , user)
      return True
    except:
      print("You already follow the account")
      return False
    time.sleep(3)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref follow")


def save_a_post(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)

    try:
      element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Enregistrer']")))      
      element.click()
      time.sleep(1)
      return True
    except:
       return True
    time.sleep(3)

  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return True
     else:
        print("Bref save")
        return True


def is_post_save(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)

    try:
      element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Supprimer']")))      
      print("You have already saved the post")
      return True
    except:
       try:
        element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Enregistrer']")))      
        return False
       except:
        return False       

    time.sleep(3)

  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return False
     else:
        print("Bref unsave")
        return False  

def unsave_a_post(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)

    try:
      element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Supprimer']")))      
      element.click()
      return True
    except:
       return False
    time.sleep(3)

  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return True
     else:
        print("Bref unsave")
        return True
     

def get_post_text(S,url):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get(url)
    try:
      element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/span")))      
      return (element.text,"")
    except:
       print("fail")
    try:
      element = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div[1]")))      
      element_to_not_split = WebDriverWait(S.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div[1]")))      
      print("succed after 2nd retry")
      return (element_to_not_split.text,str(element.text).split("\n")[0])
    except:
       print("fail 2")
       pass
    time.sleep(3)
    return (element.text)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return("","")
     else:
        print("Bref text")
        return("","")


def get_post_user(S,url):
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
        return("")

def save_coockie(selenium_session):
    pickle.dump(selenium_session.driver.get_cookies(), open(f"cookies.pkl", "wb"))

def print_pkl_info():
    file_path = f"cookies.pkl"
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return (data)

def watch_reels(S,wait_time):
  try:
    S.driver.implicitly_wait(15)
    S.driver.get("https://www.instagram.com/reels/")  
    more_or_less_10_percent = int((wait_time * 2)/10)
    x = randint(1,3) 
    if x == 1:
      nb_of_reels_to_watch = wait_time * 2
    elif x == 2:
      nb_of_reels_to_watch = wait_time * 2 - more_or_less_10_percent
    else:
      nb_of_reels_to_watch = wait_time * 2 + more_or_less_10_percent
    
    for i in range(nb_of_reels_to_watch):
      action = ActionChains(S.driver)
      action.send_keys(Keys.ARROW_DOWN).perform()
      time.sleep(randint(25,35))
  except:
     print("Bref reels")
     time.sleep(wait_time + 1)


def reset_file(path):  
    f = open(path, "w")
    f.write("")    
    f.close  
def write_into_file(path, x):
    with open(path, "w") as f:
        f.write(str(x))

def instabot():
  S = Scraper()
  
  # try:
  #   login(S,S.account_email_or_username,S.account_password)
  # except:
  #   return("")
  
  try:
    #a = 10/0
    ck = print_pkl_info()
    if len(str(ck)) > 5:
      S.driver.implicitly_wait(15)
      S.driver.get("https://www.instagram.com/")
      try:
        element = WebDriverWait(S.driver, 15).until(
          EC.presence_of_element_located((By.XPATH, S.accept_coockie_xpath)))
      except:
        element = WebDriverWait(S.driver, 15).until(
          EC.presence_of_element_located((By.XPATH, S.refuse_coockie_xpath)))

      element.click()
      cookies = pickle.load(open(f"cookies.pkl","rb"))
      
      for cookie in cookies:
          S.driver.add_cookie(cookie)
      time.sleep(0.2)
      time.sleep(5)
  except:
    print("Login with coockies error")
    try:
      login(S,S.account_email_or_username,S.account_password)
    except:
       time.sleep(1500)
       return("")
    save_coockie(S)

  automate_account_warning = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[2]/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/span"

  try:
    element = WebDriverWait(S.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, S.automate_account_warning)))
    element.click()
  except:
     pass
  
  print("ok Inside Instagram")

  list_of_post_ = print_file_info("recent_urls.txt").split("\n")
  all_post = print_file_info("url.txt").split("\n")
  list_of_post = []
  for l in list_of_post_:
     if len(l) > 5:
        list_of_post.append(l)
  post_text = []
  post_user_made = []
  post_url = []
  failed_giveaway_url = []
  failed_giveaway_comment = []
  
  idx = 0
  for url in list_of_post:
    s_text , s_user_ = get_post_text(S,url)
    s_user = get_post_user(S,url)

    time.sleep(5)
    if s_user_ != "":
      post_text.append(s_text)
      post_user_made.append(s_user_)
      if s_text != "" and s_user_ != "":
        post_url.append(url)
    else:
      if s_text != "":
        post_text.append(s_text)
      if s_user != "":
        post_user_made.append(s_user)
      if s_text != "" and s_user != "":
        post_url.append(url)

  time.sleep(30)
  t_comment_or_not , t_full_comment, t_follows = giveaway_from_url_file(S,post_text,post_user_made,post_url)
  
  if len(t_comment_or_not) == 0:
    time.sleep(1500)
    return("")
     
  for url in post_url:
    print(f"Giveaway {idx} / {len(post_url)}")
    if is_post_save(S,url) == False:
      time.sleep(5)
      if t_comment_or_not[idx] == True:
        if comment_a_post(S,url,t_full_comment[idx]) == False:
          unsave_a_post(S,url)
          if randint(1,2) == 1:
            watch_reels(S,1)
          else:
              time.sleep(60)
          failed_giveaway_url.append(url)
        else:
          save_a_post(S,url)      
          like_a_post(S,url)

      x = randint(1,2)
      if "@" in t_full_comment[idx]:
          if x == 1:
            time.sleep(60)
          else:
            watch_reels(S,2)
      else:
          if x == 1:
            time.sleep(120)
          else:
            watch_reels(S,3)
    else:
      print("you have already liked the post")
      time.sleep(30)
    idx+=1
  
  user_nb = 0
  for acc in t_follows:
    print(f"User Nb: {user_nb} / {len(t_follows)}")
    x = randint(1,4)
    if follow_an_user(S,acc,1) == True:
      time.sleep(5)
      follow_an_user(S,acc,2)
      write_into_file("follow.txt",acc.lower()+"\n")
      if x == 4:
         watch_reels(S,3)
      else:
        time.sleep(180)
    else:
      time.sleep(20)
    user_nb+=1
  
  print("All done")
  pass

