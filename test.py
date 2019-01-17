from typing import List
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome('C:/chromedriver')

# 웹 자원 로드를 위해 3초 대기
driver.implicitly_wait(3)

# 평생교육원 채팅방 url 호출
driver.get('https://center-pf.kakao.com/_EvRij/chats')

# 로그인하기
# 아이디/패스워드 입력하기
driver.find_element_by_id('loginEmail').send_keys('skuinc.internship@skuniv.ac.kr') #아이디 보안상 삭제함
driver.find_element_by_id('loginPw').send_keys('!@#$intern12') #비번은 보안상 삭제함

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/button').click()

# 카톡방 열기

# 특정 카톡방 클릭
num=1
main_window = driver.window_handles[0] # 부모창

for i in driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div').find_elements_by_tag_name('li'):
    i.click()
    #카톡방이 새 창으로 뜨기에, 창 스위치 해주어야 함.
    driver.switch_to_window(driver.window_handles[num]) # 자식창,
    chats = driver.find_elements_by_class_name('item_chat')

    elem=driver.find_element_by_tag_name("body")

    no_of_pagedowns = 1

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1


    for post in chats:
        print(post.text)
        print('----------------')

    # for chat in chats:
    #     print(chat.text)
    #     print('-----------------------------------')
    num+=1
    driver.switch_to_window(main_window)





