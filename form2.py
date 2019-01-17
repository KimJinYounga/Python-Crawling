from selenium import webdriver

driver = webdriver.Chrome('C:/chromedriver')

# 웹 자원 로드를 위해 3초 대기
driver.implicitly_wait(3)

# 평생교육원 채팅방 url 호출
driver.get('https://center-pf.kakao.com/_AxipcV/chats')

# 로그인하기
# 아이디/패스워드 입력하기
driver.find_element_by_id('loginEmail').send_keys('') #아이디 보안상 삭제함
driver.find_element_by_id('loginPw').send_keys('') #비번은 보안상 삭제함

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/button').click()

# 카톡방 열기
# 특정 카톡방 클릭
driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div/li[3]').click()

main_window = driver.window_handles[0] # 부모창
chatting_window = driver.window_handles[1] # 자식창

driver.switch_to_window(chatting_window) # 카톡방이 새 창으로 뜨기에, 창 스위치 해주어야 함.

# 대화 내용 긁어오기

chats = driver.find_elements_by_class_name('item_chat')

for chat in chats:
    print(chat.text)
    print('-----------------------------------')