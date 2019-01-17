
#
############################### chatlog로 검사################################
#

from selenium import webdriver
import json
import pandas,time
import requests
import upload_file
from selenium.webdriver.common.keys import Keys

#크롬 드라이버 설치
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

num = 1;
#모든 채팅방 찾기
chat_list = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div').find_elements_by_tag_name('li')
main_window = driver.window_handles[0] # 부모창


nickName = '';

for i in chat_list:
    i.click()

# 모든 채팅방 열기
for i in chat_list:
    # 닉네임 가져오기
    print(i.find_element_by_class_name('txt_name').text)
    nickName = i.find_element_by_class_name('txt_name').text

    # 창 변환
    driver.switch_to_window(driver.window_handles[num])

    # 맨위로 스크롤하기 if문 + body선택
    scroll_count = 10
    while scroll_count > 0:
        time.sleep(1)
        element = driver.find_element_by_tag_name('body') #body 태그로 찾기
        element.click() #채팅방 화면 클릭
        element.send_keys(Keys.HOME) #클릭 후에 HOME키 누르기
        scroll_count -= 1

    # 채팅방에서 item_chat 가져오기
    chats = driver.find_elements_by_class_name('item_chat')
    print(driver.current_url)

    # 유저 url 가져와서 chatlogs url로 변환
    idUrl = str(driver.current_url).split('/').pop()
    print(idUrl)
    url = 'https://center-pf.kakao.com/api/profiles/_EvRij/chats/' + idUrl + '/chatlogs' #chatlog URL
    print(url)
    driver.get(url)

    # chatlogs text -> json 변환
    myJson = json.loads(driver.find_element_by_tag_name('body').text)

    # chatlogs json -> data로 변환
    for item in myJson['items']:
        result_ms = pandas.to_datetime(str(int(item['send_at'])/1000), unit='s')
        full_time = str(result_ms).split(' ')

        chat_item = {}

        chat_item['date'] = full_time[0] #날짜출력
        chat_item['time'] = full_time[1] #시간출력
        chat_item['name'] = nickName #닉네임출력
        chat_item['message'] = item['message'] #메시지출력


        #이미지 여부 검사
        try:
            img_url = item['attachment']['url']
            filename = img_url.split('/')[-1] #배열의 맨마지막
            r = requests.get(img_url, allow_redirects=True)
            open(filename, 'wb').write(r.content)
            chat_item['img'] = img_url
            upload_file.saveImage(filename)
        except Exception :
            pass

        print(json.dumps(chat_item, ensure_ascii=False, indent="\t"))

    num += 1
    driver.switch_to_window(main_window)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.NUMPAD1)


chatting_window = driver.window_handles[1] # 자식창