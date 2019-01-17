from selenium import webdriver
import room_scan
import time
from selenium.webdriver.common.keys import Keys

'''
##### 데이터 베이스 테이블 #####
create table dialog(
   chat_ID int PRIMARY KEY AUTO_INCREMENT,
   nickname varchar(30),
   chat_date varchar(30),
   chat_time varchar(30),
   manager varchar(30),
   chat_msg varchar(1024), 
   attach_url varchar(1024)
);

채팅방 읽는 모듈 : room_scan
사진 업로드 모듈 : upload_image
사진 다운로드 모듈 : download_image
'''

window = 1
driver = webdriver.Chrome('C:/chromedriver')

# 웹 자원 로드를 위해 3초 대기
driver.implicitly_wait(3)

# 평생교육원 채팅방 url 호출
driver.get('https://center-pf.kakao.com/_EvRij/chats')

# 로그인하기
# 아이디/패스워드 입력하기
driver.find_element_by_id('loginEmail').send_keys('skuinc.internship@skuniv.ac.kr')  # 아이디 보안상 삭제함
driver.find_element_by_id('loginPw').send_keys('!@#$intern12')                       # 비번은 보안상 삭제함

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/button').click()

# 채팅방 리스트를 한번에 가져옴
chat_room = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div').find_element_by_tag_name('li')
main_window = driver.window_handles[0] # 부모창

# 채팅방 카운트
chat_count = 1

# 첫번쨰 방, 접속후 순회
# 대화방 scan 데이터 처리 메소드 ???
chat_room.click()
room_scan.room_scan(chat_room, driver)

# 메인 화면으로 포커스 변경
driver.switch_to_window(driver.window_handles[0])

# 현재 읽는 대화방 지정
current_chat = chat_room

time.sleep(2)

# 채팅방 리스트 가져오기
new_chat_rooms = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div').find_elements_by_tag_name('li')

# 채팅방 순회 알고리즘 ( 현재 -> 이전방 , 비교후 다음요소 순회)
while True:
    isNext = False
    # 새롭게 가져온 방 리스트중
    for new_room in new_chat_rooms:
        # 새로운 방들중에, 방금전 채팅방과 같으면
        # isNext를 true로 바꾸고 continue
        if chat_room == new_room and isNext is False:
            current_chat = new_room
            isNext = True
            continue
        # 같지않으면, 다음방비교하기
        elif chat_room != new_room and isNext is False:
            current_chat = new_room
            continue
        # flag가 True이면, continue를 통해 다음에 읽을 방을 받아온 상태이므로, for문 종료
        elif isNext:
            current_chat = new_room
            break

    # 다음에읽을 방이 직전에 읽었던 채팅방이라면,
    if chat_room == current_chat:
        break      # while문 break, 마지막 채팅방임

    # 읽어야 할 채팅방 클릭
    # 채팅방 읽기
    current_chat.click()
    room_scan.room_scan(current_chat,driver)
    #driver.close()

    # 스캔이 끝나면 이전노드로 저장
    chat_room = current_chat

    # 메인화면으로 포커스 변경
    driver.switch_to_window(driver.window_handles[0])

    # 메인 스크롤
    # 메인 화면 스크롤 지정, 클릭
    chat_list_scroll = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div')
    chat_list_scroll.click()
    driver.switch_to_window(driver.window_handles[1]) # 스크롤 내리기위해 클릭했던 채팅방 닫기
    driver.close()
    driver.switch_to_window(driver.window_handles[0]) # 메인화면으로 포커스 변경

    # 내려가는 속도를 맞추기 위함
    if chat_count % 4 == 0:  # 채팅방 4개 읽을 때 마다 스크롤 3번 다운
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)

    elif chat_count % 2 == 0: # 채팅방 2개 읽을 때 마다 스크롤 2번 다운
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)

    else: # 채팅방 1번 다운
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)

    # 스크롤이 내려가면 리스트가 바뀌기 때문에 바뀔시간 동안 기다리기
    time.sleep(2)
    driver.switch_to_window(driver.window_handles[0])

    # 바뀐 채팅방 리스트 가져옴
    new_chat_rooms = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div').find_elements_by_tag_name(
        'li')

    chat_count += 1

driver.close()
print("---------------끝---------------")
