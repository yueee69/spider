from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import time
import os

os.system('chcp 65001')
print('\n均一網站\n>>> https://www.junyiacademy.org/\n')

url = input('請輸入網址的url後綴(https://www.junyiacademy.org/XXXXXXXXXXXXXXXX)(XXX部分)\n')

if url.split('/')[0] == 'exam':#高中or國小
    print('\n<國小/高中端>\n網址>>> https://www.junyiacademy.org/' +url)
    answer = requests.get('https://www.junyiacademy.org/api/v2/perseus/' +url+ '/get_question')

    if answer.status_code == 200:
        driver = webdriver.Chrome()
        driver.get('https://www.junyiacademy.org/' + url)

        for i in range(2):
            try:
                time.sleep(1)
                driver.find_elements(By.CLASS_NAME, "MuiButton-containedPrimary")[0].click()#skip
            except:
                break

        for length in range(len(answer.json()["data"])):
            try:
                time.sleep(2)
                button_elements = []
                try:
                    button_elements = driver.find_elements(By.CSS_SELECTOR, "li.perseus-radio-option")
                except:
                    button_elements = driver.find_elements(By.CSS_SELECTOR, "perseus_radio_18")

                try:
                    for idx, choice in enumerate(answer.json()["data"][length]["question"]["answerArea"]["options"]["choices"]):
                        if choice["correct"]:
                            button_elements[idx].click()
                except:
                    for idx, choice in enumerate(answer.json()["data"][length]["question"]["question"]["widgets"]["radio 1"]["options"]["choices"]):
                        if choice["correct"]:
                            button_elements[idx].click()
            except:
                button_elements = []
                while(len(button_elements)==0):
                    button_elements = driver.find_elements(By.CLASS_NAME, "perseus-input")

                for idx,element in enumerate(button_elements):
                    try:
                        element.send_keys(answer.json()["data"][length]["question"]["answerArea"]["options"]["value"])
                    except:
                        try:
                            element.send_keys(answer.json()["data"][length]["question"]["question"]["widgets"][f"input-number {idx+1}"]["options"]["value"])
                        except:
                            element.send_keys(answer.json()["data"][length]["question"]["question"]["widgets"]["draggable-container 1"]["options"]["widgets"][f"input-number {idx+1}"]["options"]["value"])

            if length != len(answer.json()["data"])-1:
                driver.find_element(By.ID,"check-answer-button").click()

    else:
        print('獲取失敗 請確認網址是否正確\n>>> https://www.junyiacademy.org/exam/' + url)


else:#國中
    print('\n<國中端>\n網址>>> https://www.junyiacademy.org/' +url)
    answer = requests.get('https://www.junyiacademy.org/api/v2/perseus/' +url.split('/')[-1]+ '/get_question')

    if answer.status_code == 200:
        driver = webdriver.Chrome()
        driver.get('https://www.junyiacademy.org/' + url)

        for i in range(2):
            try:
                time.sleep(1)
                driver.find_elements(By.CLASS_NAME, "MuiButton-containedPrimary")[0].click()#skip
            except:
                break

        for length in range(len(answer.json()["data"])):
            time.sleep(2)
            button_elements = []
            button_elements = driver.find_elements(By.CLASS_NAME, 'perseus-radio-option')

            for idx, choice in enumerate(answer.json()["data"][length]["question"]["question"]["widgets"]["radio 1"]["options"]["choices"]):
                if choice["correct"]:
                    button_elements[idx].click()

            driver.find_element(By.ID,"check-answer-button").click()
            driver.find_element(By.ID,"next-question-button").click()

    else:
        print('獲取失敗 請確認網址是否正確\n>>> https://www.junyiacademy.org/exam/' + url)



print('\n程式已經結束 請自行交卷。')
os.system('pause')


    

