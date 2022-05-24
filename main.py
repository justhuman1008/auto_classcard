from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import chromedriver_autoinstaller

from bs4 import BeautifulSoup

import os
import warnings
import json
import requests
from time import sleep
import sys

# 함수 ==============================================================================================================

# 계정 
def check_account(id, pw):
    print("\n계정 정보가 올바른지 확인중입니다.")
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"login_id": id, "login_pwd": pw}
    res = requests.post("https://www.classcard.net/LoginProc", headers=headers, data=data)
    status = res.json()
    if status["result"] == "ok":
        return True
    else:
        return False

# 코드 본문 ==============================================================================================================

# 작동
warnings.filterwarnings("ignore", category=DeprecationWarning)
print("="*50)
print("클래스카드 세트 학습 매크로")
print("Made by Justhuman1008")
print("https://github.com/justhuman1008")
print("="*50)




# 계정 정보 확인
try:
    try: # 저장된 정보가 있음
        with open("account.json", "r", encoding="utf-8") as f:
            account_data = json.load(f)
            account_data["id"]
            account_data["pw"]
            
    except: # 저장된 정보가 없음(정보 저장)
        print("클래스카드 계정 정보가 없습니다.")
        while True:
            id = input("아이디를 입력하세요: ")
            password = input("비밀번호를 입력하세요: ")
            if check_account(id, password) == True:
                account_data = {"id": id, "pw": password}
                with open("account.json", "w", encoding="utf-8") as f:
                    json.dump(account_data, f, ensure_ascii=False, indent=4)
                print("아이디 비밀번호가 저장되었습니다.\n")
                print("="*50)
                break

            else:
                print("아이디 또는 비밀번호가 잘못되었습니다.\n")
                print("="*50)
                continue
except:
    print("오류 발생: `계정 정보 확인` 실패")
    sys.exit()




# 학습 세트 링크 받기
try:
    while True:
        Class_URL = input("학습할 세트의 URL: ")
        if Class_URL.find("https://www.classcard.net/set/") == 0:
            print("학습할 세트가 입력되었습니다.\n")
            print("="*50)
            break
        print("`https://www.classcard.net/set/숫자` 형식의 링크를 입력해주세요")
        print("="*50)
except:
    print("오류 발생: `학습 세트 링크 받기` 실패")
    sys.exit()




# 크롬 드라이버 연결
try:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(chromedriver_autoinstaller.install()), options=options)
    driver.implicitly_wait(10)
    driver.set_window_position(1000,0)
    driver.get("https://www.classcard.net/Login")
except:
    print("오류 발생: `크롬 드라이버 연결` 실패")
    driver.quit()
    sys.exit()




# 클래스카드 로그인
try:
    login_id = driver.find_element(By.ID, "login_id")
    login_id.send_keys(account_data["id"])
    login_pw = driver.find_element(By.ID, "login_pwd")
    login_pw.send_keys(account_data["pw"])
    login_pw.send_keys(Keys.RETURN)
    sleep(1)
    driver.get(Class_URL)
except:
    print("오류 발생: `클래스카드 로그인` 실패")
    driver.quit()
    sys.exit()



'''
# 단어 저장
try:
    html = BeautifulSoup(driver.page_source, "html.parser")
    cards_box = html.find("div", class_="flip-body")
    cards_num = len(cards_box.find_all("div", class_="flip-card"))

    Words_Eng_Kor:dict = {}
    Words_Kor_Eng:dict = {}
    for i in range(cards_num):
        Eng = driver.find_element(By.XPATH, f'//*[@id="tab_set_all"]/div[2]/div[{i+1}]/div[4]/div[1]/div[1]/div/div').text
        Kor = driver.find_element(By.XPATH, f'//*[@id="tab_set_all"]/div[2]/div[{i+1}]/div[4]/div[2]/div[1]/div/div').text

        Words_Eng_Kor[Eng] = Kor
        Words_Kor_Eng[Kor] = Eng
    print("단어 저장 완료")
    print(f'{Words_Eng_Kor}\n-----\n{Words_Kor_Eng}\n')
    print("="*50)
except:
    print("오류 발생: `단어 저장` 실패")
    driver.quit()
    sys.exit()




# 학습범위 변경
try:
    driver.find_element(By.CSS_SELECTOR, 'body > div.mw-1080 > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a').click()
    driver.find_element(By.CSS_SELECTOR, 'body > div.mw-1080 > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1) > a').click()
except:
    print("오류 발생: `학습범위 변경` 실패")
    driver.quit()
    sys.exit()



# 암기학습 진행
try:
    driver.find_element(By.CSS_SELECTOR, '#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(1)').click()
    sleep(1)
    for i in range(cards_num):
        sleep(1.5)
        driver.find_element(By.CSS_SELECTOR, '#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box > a').click()
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box').click()

    print(" - 암기학습 완료")
    driver.get(Class_URL)
    driver.switch_to_alert().accept()
    driver.switch_to.alert.accept()
except:
    print("오류 발생: `암기학습 진행` 실패")
    driver.quit()
    sys.exit()




driver.find_element(By.CSS_SELECTOR, '#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(2)').click()
sleep(2)
for i in range(1, cards_num):
    sleep(1)
    Q_Word = driver.find_element(By.XPATH, f'//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span').text
    print(Q_Word)
    for a in range(0, 3):
        A_Word = driver.find_element(By.XPATH, f'//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{a+1}]/div[2]/div').text

        if Words_Eng_Kor[Q_Word] == A_Word:
            driver.find_element(By.XPATH, f'//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{a+1}]/div[2]').click()
            break
'''