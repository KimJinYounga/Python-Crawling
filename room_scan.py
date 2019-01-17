from selenium import webdriver
# import mysql1 as sql
from selenium.webdriver.common.keys import Keys
import pandas,time
import requests
# import upload_image

def room_scan(room, driver):
    driver.switch_to_window(driver.window_handles[1])
    # 상담자
    nickName = driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[1]/div[1]/div/div/strong').text
    nickName = nickName.split('\n')[1]

    # up_img = upload_image.Upload_image()

    # 담당자
    chat_manager = driver.find_element_by_class_name('tit_profile').text

    top_chat = driver.find_element_by_class_name('item_chat')

    # 스크롤 올리기
    isTop = False
    while True:
        time.sleep(0.2)
        element = driver.find_element_by_tag_name('body')
        element.click()
        element.send_keys(Keys.HOME)  # home키를 누르게 하여 스크롤 올림
        print("page up")
        # scroll_count -= 1
        if len(driver.window_handles) == 3:
            print('window=====' + str(1) + 'handles======' + str(len(driver.window_handles)))
            driver.switch_to_window(driver.window_handles[2]) # 사진이 클릭 되었을 시 창 닫음
            driver.close()
            driver.switch_to_window(driver.window_handles[1])
            print('num ======= ' + str(1))
        current_caht = driver.find_element_by_class_name('item_chat')

        if isTop:
            break
        if current_caht == top_chat:
            isTop = True
        top_chat = current_caht

    # 대화방 날짜 별로 가져오기
    days = driver.find_elements_by_xpath("//*[@id=\"room\"]/div/div")
    time.sleep(2)
    for day in days:
        chat_date = day.find_element_by_class_name("bg_line").text
        print("=================" + chat_date)
        items = day.find_elements_by_class_name("item_chat")
        for item in items:
            chat_msg = item.find_element_by_class_name('set_chat').text
            img_url = ''
            if str(item.get_attribute("class")).find("item_save") != -1:
                # 이미지 저장
                img_url = item.find_element_by_class_name('link_pic').get_attribute('href')
                filename = img_url.split('/')[-1]
                r = requests.get(img_url, allow_redirects=True)
                open(filename, 'wb').write(r.content)
                # img_url = up_img.saveImage(filename, nickName)
            print("============================")
            print("nick name :" + nickName)
            print("manager :" + chat_manager)
            print("message :" + chat_msg)
            # print("url :" + img_url)
            # print("============================")
            # sql.save_msg(str(nickName), chat_date, '', chat_manager, str(chat_msg), img_url)
    driver.close()
    return driver



