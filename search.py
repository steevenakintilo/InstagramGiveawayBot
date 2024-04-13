from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import os.path

import re
import pickle
from selenium.webdriver.common.action_chains import ActionChains
import emoji
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

class Data:
    with open("configuration.yml", "r",encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    accounts_to_tag_ = data["accounts_to_tag"]
    accounts_to_tag_ = random.sample(accounts_to_tag_, len(accounts_to_tag_))
    accounts_to_tag = []
    sentence_for_tag = data["sentence_for_tag"]
    sentence_for_random_comment = data["sentence_for_random_comment"]
    add_sentence_to_tag = data["add_sentence_to_tag"]
    word_list_to_check_for_special_comment = data["word_list_to_check_for_special_comment"]
    word_list_to_check_for_comment = data["word_list_to_check_for_comment"]
    short_word_list_to_check_for_comment = data["short_word_list_to_check_for_comment"]
    word_list_to_check_for_tag = data["word_list_to_check_for_tag"]
    one_poeple_list = data["one_poeple_list"]
    two_poeple_list = data["two_poeple_list"]
    three_or_more_poeple_list = data["three_or_more_poeple_list"]
    word_list_to_not_check_for_copy = data["word_list_to_not_check_for_copy"]


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


def get_the_right_word(sentence):
    new_sentence = ""
    
    guillemet_counter = 0
    for i in range(len(sentence)):
        if sentence[i] == '"' or sentence[i] == '“' or sentence[i] == '«' or sentence[i] == "»":
            guillemet_counter = guillemet_counter + 1
        if guillemet_counter >= 2:
            break
        if guillemet_counter == 1 or sentence[i] == '"' or sentence[i] == '“' or sentence[i] == "«" or sentence[i] == "»":
            new_sentence = new_sentence + sentence[i]
    
    return (new_sentence.replace('"',"").replace("“","").replace("«","").replace("»",""))


def get_list_of_comment_of_a_post(S,url):
    try:
      list_of_comment = []
      S.driver.implicitly_wait(15)
      S.driver.get(url)
      
      element = WebDriverWait(S.driver, 3).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[3]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/span")))      
      S.driver.execute_script("arguments[0].scrollIntoView();", element)
      time.sleep(0.1)
      list_of_comment.append(element.text)
      return (list_of_comment)
    except Exception as e:
     if "net::ERR_NAME_NOT_RESOLVED" in str(e):
        print("Wifi error sleeping 3 minutes")
        time.sleep(180)
        return(False)
     else:
        return(False)

def copy_a_comment(selenium_session,url):
    account_to_blacklist = print_file_info("account_blacklist.txt")
    try:
        tag_nb = 0
        d = Data()
        list_of_comment_of_a_tweet = get_list_of_comment_of_a_post(selenium_session,url)
        time.sleep(4)

        if list_of_comment_of_a_tweet == False or len(list_of_comment_of_a_tweet) == 0 or len(list_of_comment_of_a_tweet[0]) > 135:
            return (d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)])

        check_if_tag_only = list_of_comment_of_a_tweet[0].replace("\n","").split(" ")
        if list_of_comment_of_a_tweet[0].count("@") == len(check_if_tag_only):
            return (d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)])
        xxx = list_of_comment_of_a_tweet[0]
        rs = re.sub(r'@\w+\s*', '', xxx)   
        return (rs)          
            
    except:
        d = Data()
        return (d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)])    

def what_to_comment(sentences,S,url):
    s = sentences.split("\n")
    d = Data()
    special_char = ",;.!?@"
    forbiden = False
    for word in d.word_list_to_not_check_for_copy:
        if word.lower() in sentences.lower():
            forbiden = True
    
    if forbiden == False:
        for word in d.word_list_to_check_for_special_comment:
            s = sentences.lower()
            if word in sentences.lower():
                print(" yeahahahahahah")
                next_part = s.split(word)[1]
                copied_comment = copy_a_comment(S,url)
                if copied_comment != False:
                    return copied_comment

    for word in d.word_list_to_check_for_special_comment:
        if word in sentences.lower():
          return ("Ok!")
    return ("Ok!")

def check_if_we_need_to_comment(text):
    d = Data()

    for elem in d.word_list_to_check_for_comment:
        if elem.lower() in text.lower():
            return True
    
    for word_to_check in d.short_word_list_to_check_for_comment:
        for word in text.split():
            if word.lower().startswith(word_to_check.lower()) and len(word) <= len(word_to_check):
                return True

    text = text.lower()
    return False


def check_if_we_need_to_tag(text):
    d = Data()
    
    if "-tag" in text.lower() or "#tag" in text.lower():
        return True
    
    for elem in d.word_list_to_check_for_tag:
        if elem.lower() in text.lower() and elem.lower() != "tag":
            return True
    
    for word_to_check in d.word_list_to_check_for_tag:
        for word in text.split():
            if (word.lower().startswith(word_to_check.lower()) and "tag" in word.lower()):
                return True
    return False

def delete_url(s):
    s_ = s.split(" ")
    n_s = []
    for i in range(len(s_)):
        if "https" not in s_[i]:
            n_s.append(s_[i])
    n =  " ".join(n_s)
    n = n.strip()

    return n

def who_many_people_to_tag(text,accounts_to_tag):
    text = text.replace("\n", " ") 
    d = Data()
    
    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return(accounts_to_tag[0])
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return(accounts_to_tag[0]+" "+accounts_to_tag[1])
    
    return(" ".join(accounts_to_tag))
    
def check_if_we_need_to_tag_two(text):
    text = text.replace("\n", " ") 
    d = Data()
    
    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return True
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return True
    
    for other in d.three_or_more_poeple_list:
        if other.lower() in text.lower():
            return True
    return False    

def check_alpha_numeric(string):
    string = string.lower()
    alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789_@."
    for elem in string:
        if elem not in alphanumeric:
            return False
    return True

def check_alpha_numeric_pos(string):
    string = string.lower()
    alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789_@."
    for i in range(len(string)):
        if string[i] not in alphanumeric:
            return i
    return 0

def remove_non_alphanumeric(string):
    s = string.split("\n")
    return s[0]

def remove_emojie(text):
    return emoji.replace_emoji(text, replace='')
    #return emoji.get_emoji_regexp().sub(r'',text)

def list_of_account_to_follow(maker_of_the_tweet,sentence):
    
    sentence = remove_emojie(sentence).replace("\n"," ")
    account_to_follow = [maker_of_the_tweet.replace("@","")]
    s = sentence.split(" ")
    for word in s:
        try:
            if word[0] == "@" and word.replace("@","") != maker_of_the_tweet.replace("@",""):
                if "\n" in word:
                    word = word.split("\n")[0]
                if check_alpha_numeric(word) == False:
                    word = word[0:check_alpha_numeric_pos(word)]
                account_to_follow.append(remove_non_alphanumeric(word.replace("@","")))
        except:
            pass
    account_to_follow = list(dict.fromkeys(account_to_follow))
    return (" ".join(account_to_follow))

def giveaway_from_url_file(S,tweets_text,account_list,tweet_from_url):
    try:
      d = Data()
      accounts_to_tag_ = d.accounts_to_tag_
      accounts_to_tag_ = random.sample(accounts_to_tag_, len(accounts_to_tag_))
      accounts_to_tag = []
      if len(accounts_to_tag_) >= 3:
          for i in range(3):
              if i == 0:
                  accounts_to_tag.append(" " + accounts_to_tag_[i])
              else:
                  accounts_to_tag.append(accounts_to_tag_[i])
      else:
          accounts_to_tag = [' @Instagram ', '@Mrbeast ', '@433 ']   
      
      #tweet_from_url = print_file_info("recent_url.txt").split("\n")
      tweets_need_to_comment_or_not = []
      tweets_full_comment = []
      tweets_account_to_follow = []
      full_phrase = ""
      print_data = False
      idxx = 0
      iihe = 0
      
      for t in tweets_text:
        current_url = tweet_from_url[idxx]
        what_to_cmt = what_to_comment(t,S,current_url)
        if what_to_cmt == "Ok!":
            what_to_cmt = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)]
        if check_if_we_need_to_tag(t) == True:
          if check_if_we_need_to_comment(t) == True:
              if what_to_cmt == "Ok!":
                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
              else:
                full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
          else:
              nb_word = what_to_cmt.split()
              full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
              if what_to_cmt == "Ok!":
                  if d.add_sentence_to_tag == True and len(nb_word) >= 5:
                    full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                  else:
                    full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
              else:
                  if d.add_sentence_to_tag == True and len(nb_word) >= 5:
                    full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                  elif d.add_sentence_to_tag == False and len(nb_word) >= 5:
                    full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                
        else:
          if check_if_we_need_to_comment(t) == True:
              full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + " "
          else:
              full_phrase = ""  
        if check_if_we_need_to_tag(t) == True or (check_if_we_need_to_tag_two(t) == True and check_if_we_need_to_tag(t) == True):
          tweets_need_to_comment_or_not.append(True)
        else:
          tweets_need_to_comment_or_not.append(True)
        tweets_full_comment.append(remove_emojie(full_phrase).replace('"',"").replace("“","").replace("«","").replace("»","").replace("”",""))
        tweets_account_to_follow.append(list_of_account_to_follow("" ,t))  
        idxx+=1
      
      for a in account_list:
        if a not in tweets_account_to_follow and a != "f":
              tweets_account_to_follow.append(a.lower())
      
      full_list_of_account_to_follow = []

      for account in tweets_account_to_follow:
          if " " in account:
              a = account.split(" ")
              for k in range(len(a)):
                  if k not in full_list_of_account_to_follow and len(a[k]) > 1:
                      full_list_of_account_to_follow.append(a[k])
          else:
              if len(account) > 1 and account not in full_list_of_account_to_follow:
                  full_list_of_account_to_follow.append(account)
      if print_data == True:
          print(tweets_full_comment)
          print(tweets_need_to_comment_or_not)
          print(full_list_of_account_to_follow)
      #print(tweets_need_to_comment_or_not)
      print("nb of acc to follow " , len(full_list_of_account_to_follow))
      
      return (tweets_need_to_comment_or_not,tweets_full_comment,full_list_of_account_to_follow)

      
    except Exception as e:
        print("YOLO YOLO BANG BANG")
        print("Error " )
        traceback.print_exc()
        return (tweets_need_to_comment_or_not,tweets_full_comment,tweets_account_to_follow)