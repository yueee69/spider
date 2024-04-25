from selenium import webdriver                 #import網頁啟動器
import requests                                #import爬蟲
from selenium.webdriver.common.by import By    #import網頁啟動器的抓取html元素資料
import time                                    #import sleep函數
import os                                      #import控制台

os.system('chcp 65001')                        #讓輸出文字接受utf-8
print('\n均一網站\n>>> https://www.junyiacademy.org/\n') 

url = input('請輸入網址的url後綴(https://www.junyiacademy.org/XXXXXXXXXXXXXXXX)(XXX部分)\n') #讓使用者輸入網址

if url.split('/')[0] == 'exam':#高中or國小      #解析網址，各平台的json格式不同
    print('\n<國小/高中端>\n網址>>> https://www.junyiacademy.org/' +url) #印出用戶打的網址，以便用戶確認
    answer = requests.get('https://www.junyiacademy.org/api/v2/perseus/' +url+ '/get_question') #利用爬蟲get該測驗的解答

    if answer.status_code == 200:               #如果request的狀態碼=200(也就是請求成功)
        driver = webdriver.Chrome()             #開啟chrome的瀏覽器
        driver.get('https://www.junyiacademy.org/' + url)  #開啟用戶指定的網頁

        for i in range(2):                      #2次的迴圈，用於關掉彈出來的廣告
            try:                                #這裡用try-except是因為廣告不一定是每次都彈，若不用可能會報錯找不到元素
                time.sleep(1)                   #等待1秒
                driver.find_elements(By.CLASS_NAME, "MuiButton-containedPrimary")[0].click()#skip #廣告關閉按鈕的class_name
            except:                             #如果沒廣告就跳出
                break

        for length in range(len(answer.json()["data"])):  #迴圈答案json的長度(是陣列，一個答案長度為1，所以有N個答案就迴圈N次)
            try:                               #這裡的try-except是判斷是否為"填充題"，是則進入下方的except(因為填充題的答案json格式和選擇不相同，如果不用try-except會報錯)
                time.sleep(2)                  #每一題間隔兩秒
                button_elements = []           #取得該題所有選項的html-button
                try:                           #這裡用try-except是為了判斷是高中還是國小端(兩邊的html-class_selector都不一樣，如果只寫一種會報錯)
                    button_elements = driver.find_elements(By.CSS_SELECTOR, "li.perseus-radio-option") #高中端的class_selector_name(讓button_elements填滿該題所有選項)
                except:
                    button_elements = driver.find_elements(By.CSS_SELECTOR, "perseus_radio_18")        #國小端的class_selector_name(同上)

                try:                           #這裡用try是為了判斷高中與國小端的json差異(印證了上述所說的各端格式不同)
                    for idx, choice in enumerate(answer.json()["data"][length]["question"]["answerArea"]["options"]["choices"]): #高中端的答案json
                        if choice["correct"]:  #遍歷該題的答案，如果為正確就按下button_elements中對應的index(這就是為什麼要用enumerate())
                            button_elements[idx].click() #按下答案的按鈕
                except:
                    for idx, choice in enumerate(answer.json()["data"][length]["question"]["question"]["widgets"]["radio 1"]["options"]["choices"]): #國小端的json
                        if choice["correct"]:  #同高中端的處理方式
                            button_elements[idx].click()
            except:                            #處理填充題
                button_elements = []           #初始化button_elements
                while(len(button_elements)==0): #填充題可能很多格要填，所以用while獲取直到長度不為0
                    button_elements = driver.find_elements(By.CLASS_NAME, "perseus-input") #這裡的find是一次獲取該題所有答案，所以不用寫額外邏輯

                for idx,element in enumerate(button_elements): #迴圈答案數量次
                    try:                        #判別兩端
                        element.send_keys(answer.json()["data"][length]["question"]["answerArea"]["options"]["value"]) #高中端的填充答案json格式
                    except:
                        try:                    #這裡的try-except是解析國小端的json，又分為兩種
                            element.send_keys(answer.json()["data"][length]["question"]["question"]["widgets"][f"input-number {idx+1}"]["options"]["value"]) #國小端的第一種json
                        except:
                            element.send_keys(answer.json()["data"][length]["question"]["question"]["widgets"]["draggable-container 1"]["options"]["widgets"][f"input-number {idx+1}"]["options"]["value"]) #國小端的第二種json

            if length != len(answer.json()["data"])-1: #判斷是否為最後一題
                driver.find_element(By.ID,"check-answer-button").click() #如果是，則只按選項，而不按下一題

    else:
        print('獲取失敗 請確認網址是否正確\n>>> https://www.junyiacademy.org/exam/' + url)


else:#國中端
    print('\n<國中端>\n網址>>> https://www.junyiacademy.org/' +url)
    answer = requests.get('https://www.junyiacademy.org/api/v2/perseus/' +url.split('/')[-1]+ '/get_question') #獲取國中端答案api，網址較高中/國小端不同，也較複雜

    if answer.status_code == 200: #同高中/國小端的處理方式
        driver = webdriver.Chrome()
        driver.get('https://www.junyiacademy.org/' + url)

        for i in range(2): #同高中/國小端的處理方式
            try:
                time.sleep(1)
                driver.find_elements(By.CLASS_NAME, "MuiButton-containedPrimary")[0].click()#skip #國中端關閉廣告按鈕的class_name
            except:
                break

        for length in range(len(answer.json()["data"])): #重複答案數量次
            time.sleep(2)
            button_elements = [] #這裡因為只有國中端，所以不用判斷按鈕/json差異，因此沒有大量的try-except
            button_elements = driver.find_elements(By.CLASS_NAME, 'perseus-radio-option') #獲取該題的所有答案

            for idx, choice in enumerate(answer.json()["data"][length]["question"]["question"]["widgets"]["radio 1"]["options"]["choices"]):
                if choice["correct"]: #為甚麼這裡用for?，因為國中端有"多選題"
                    button_elements[idx].click() #按該題的每一個答案為true的按鈕

            driver.find_element(By.ID,"check-answer-button").click() #國中端下一題要按兩次，超麻煩
            driver.find_element(By.ID,"next-question-button").click()
            #國中端沒有填充題，所以不用做最外面的try-except。取而代之的是多選題
    else:
        print('獲取失敗 請確認網址是否正確\n>>> https://www.junyiacademy.org/exam/' + url)



print('\n程式已經結束 請自行交卷。') 
os.system('pause')


    

