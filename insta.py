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

from search import giveaway_from_url_file , get_list_of_comment_of_a_post
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
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref comment")

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
    except:
       print("You have already saved the post")
    time.sleep(3)
  except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
     else:
        print("Bref save")

def get_tweet_text(S,url):
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
        return("")

def save_coockie(selenium_session):
    pickle.dump(selenium_session.driver.get_cookies(), open(f"cookies.pkl", "wb"))

def print_pkl_info():
    file_path = f"cookies.pkl"
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return (data)


def write_into_file(path, x):
    with open(path, "w") as f:
        f.write(str(x))
def instabot():
  S = Scraper()
  
  try:
    login(S,S.account_email_or_username,S.account_password)
  except:
    S.driver.close()
    time.sleep(10)
    S = Scraper()
    login(S,S.account_email_or_username,S.account_password)
     
  time.sleep(5)  
  list_of_tweet_ = print_file_info("urls.txt").split("\n")
  list_of_tweet = []
  for l in list_of_tweet_:
     if len(l) > 5:
        list_of_tweet.append(l)
     else:
        print("skip")
  tweet_text = []
  tweet_user_made = []
  tweet_url = []
  idx = 0
  for url in list_of_tweet:
    s_text , s_user_ = get_tweet_text(S,url)
    s_user = get_tweet_user(S,url)

    time.sleep(5)
    if s_user_ != "":
      tweet_text.append(s_text)
      tweet_user_made.append(s_user_)
      if s_text != "" and s_user_ != "":
        tweet_url.append(url)
    else:
      if s_text != "":
        tweet_text.append(s_text)
      if s_user != "":
        tweet_user_made.append(s_user)
      if s_text != "" and s_user != "":
        tweet_url.append(url)

  t_comment_or_not , t_full_comment, t_follows = giveaway_from_url_file(S,tweet_text,tweet_user_made,tweet_url)
  
  a = "d"
  if a == "d":
    for url in tweet_url:
      print(f"Giveaway {idx} / {len(tweet_url)}")
      if like_a_post(S,url) == True:
        time.sleep(5)
        #a = like_a_post(S,url)
        #print("Value of a " , a)
        if t_comment_or_not[idx] == True:
          comment_a_post(S,url,t_full_comment[idx])
        save_a_post(S,url)

        if "@" in t_full_comment[idx]:
           time.sleep(300)
        else:
            time.sleep(600)
      else:
        print("you have already liked the post")
        time.sleep(30)
      idx+=1
    
  user_nb = 0
  for acc in t_follows:
    print(f"User Nb: {user_nb} / {len(t_follows)}")
    if follow_an_user(S,acc,1) == True:
      time.sleep(5)
      follow_an_user(S,acc,2)
      time.sleep(200)
    else:
      time.sleep(20)
    user_nb+=1
  print("All done")
  pass

