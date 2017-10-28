import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys




x=webdriver.Chrome()


x.get('https://www.google.co.in/maps/')


def get_lat_long(name):
  x.find_element_by_css_selector('#searchboxinput').clear()
  x.find_element_by_css_selector('#searchboxinput').send_keys(name)
  x.find_element_by_css_selector('#searchboxinput').send_keys(Keys.ENTER)
  time.sleep(2)
  temp=x.current_url.split('/')[6].split(',')[0:2]
  
  print (temp)

get_lat_long("SRM University, Chennai")
