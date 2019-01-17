
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('C:/chromedriver')

browser.get('https://stackoverflow.com/questions/3369073/controlling-browser-using-python')
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 29

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

provider_elems = browser.find_elements_by_class_name("className")

for post in provider_elems:
    print(post.text)