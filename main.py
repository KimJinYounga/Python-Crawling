from selenium import webdriver
import json
import os
from collections import OrderedDict
import pandas,time
import requests
import upload_file
from selenium.webdriver.common.keys import Keys

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

num = 1
chat_list = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div').find_elements_by_tag_name('li')
main_window = driver.window_handles[0] # 부모창

chat_items = []
iswhat=False
# 모든 채팅방 열기

while True:
    count=0
    for i in chat_list:
        # 채팅방 하나 클릭
        scroll_count2 = 1
        if (count % 5 == 0 and count > 0):
            if scroll_count2 > 0:
                time.sleep(1)
                element = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div')
                element.send_keys(Keys.PAGE_DOWN)  # home키를 누르게 하여 스크롤 올림
                scroll_count2 -= 1
                time.sleep(3)
                driver.switch_to_window(driver.window_handles[0])
                chat_list = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div').find_elements_by_tag_name('li')

            break

        count += 1
        i.click()
        windows = len(driver.window_handles)
        print(windows)
        # 창 변환
        driver.switch_to_window(driver.window_handles[num])

        # 상담자
        nickName = driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[1]/div[1]/div/div/strong').text
        nickName = nickName.split('\n')[1]

        # 담당자
        chat_manager = driver.find_element_by_class_name('tit_profile').text

        # 스크롤 올리는 while문 현재는 10번만 올림
        scroll_count = 2
        while scroll_count > 0:  # 50번 반복
            time.sleep(1)
            element = driver.find_element_by_tag_name('body')

            element.click()
            element.send_keys(Keys.HOME)  # home키를 누르게 하여 스크롤 올림
            scroll_count -= 1

            if windows + 1 == len(driver.window_handles):
                num += 1
                windows = len(driver.window_handles)
                print('num ======= ' + str(num))

        # 채팅방에서 item_chat 가져오기
        chats = driver.find_elements_by_class_name('item_chat')
        chat_date = driver.find_element_by_class_name('bg_line').text.split(' ')[0]

        if (chat_date != driver.find_element_by_class_name('bg_line').text.split(' ')[0]):
            chat_date = driver.find_element_by_class_name('bg_line').text.split(' ')[0]

        chat_time = ""
        # chatlogs json -> data로 변환


        for chat in chats:
            print(nickName)  # 닉네임 출력
            print(chat.find_element_by_class_name('set_chat').text)  # 메시지 출력

            chat_msg = chat.find_element_by_class_name('set_chat').text

            img_url = ''

            # chat_item = OrderedDict()
            # chat_item['name'] = nickName
            # chat_item['manager'] = chat_manager

            # chat_item['date'] = chat_date
            # chat_item['message'] = chat.find_element_by_class_name('set_chat').text
            #
            # print(nickName)  # 닉네임 출력
            # print(chat.find_element_by_class_name('set_chat').text) # 메시지 출력

            # 이미지 태그가 있는지 없는지 확인하는 try/except문
            # try:
            #     print(chat.find_element_by_class_name('link_pic').get_attribute('href'))
            #     img_url = chat.find_element_by_class_name('link_pic').get_attribute('href')
            #     chat_item['img'] = img_url
            #     filename = img_url.split('/')[-1]
            #     r = requests.get(img_url, allow_redirects=True)
            #     open(filename, 'wb').write(r.content)
            #     chat_item['img'] = img_url
            #   #  upload_file.saveImage(filename)
            # except Exception :
            #     pass
            #
            # # 시간 태그가 있는지 없는지 확인하는 try/except문
            # try:
            #     chat_time = chat.find_element_by_class_name('txt_time').text
            # except Exception :
            #     pass

            print(chat_time)
            print('=========================')
        num += 1

        driver.switch_to_window(main_window)