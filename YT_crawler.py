from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import pandas
import time

url = "https://www.youtube.com/"

#driver設定
driver_location = "C:/Users/阿甘/Desktop/YT_crawler/chromedriver.exe"
driver = webdriver.Chrome(driver_location)
 
#進入YT
driver.get(url)

#點選登入
btn_1 = driver.find_elements_by_css_selector("tp-yt-paper-button")[1]
btn_1.click()
time.sleep(3)

#登入帳號
account = "410633010@mail.nknu.edu.tw"
input_1 = driver.find_element_by_id("identifierId")
input_1.send_keys(account)

#點選繼續
input_1.send_keys(Keys.ENTER)
time.sleep(5)

#輸入帳號
password = "***********748"
input_2 = driver.find_element_by_name("password")
input_2.send_keys(password)

#點選繼續
input_2.send_keys(Keys.ENTER)
time.sleep(5)

#點選右側導覽
driver.get("https://youtu.be/hVsf2ZE0C3M")
time.sleep(3)

#一直往下滑
html = driver.find_element_by_tag_name('html')
js_1="var q=document.documentElement.scrollTop=0"
js_2="var q=document.documentElement.scrollTop=100000"
js_3 = "return action=document.documentElement.scrollTop"
height_1 = driver.execute_script(js_3)						#取得當前高度height_1
#print("height_1",height_1)
while(1):
	driver.execute_script(js_2)								#滑到底
	time.sleep(2)
	height_2 = driver.execute_script(js_3)					#取得當前高度height_2
#	print("height_1",height_1)
#	print("height_2",height_2)
	if(height_2==height_1):									#比較是否相等
		break
	else:
		height_1=height_2

#儲存並剖析所有訊息
all = [] #存放所有留言
soup = BeautifulSoup(driver.page_source, 'html.parser')
#names = soup.find_all("span", class_="style-scope ytd-comment-renderer")
comments = soup.find_all("div", class_="style-scope ytd-comment-renderer", id="main")

print(len(comments))
for comment in comments:
	dic = {}	
	dic['name'] = comment.find("span", class_="style-scope ytd-comment-renderer").string
	try:
		a =  comment.find("yt-formatted-string", class_="style-scope ytd-comment-renderer", id="content-text", slot="content").string
		if( a == None ):
			m_comments = comment.find_all("span", class_="style-scope yt-formatted-string", dir="auto")
			m_comment_1 = ""
			for m_comment in m_comments:
				m_comment_1 = m_comment.string + m_comment_1
			a = m_comment_1
		dic['data'] = a
		print(a)
	except AttributeError: #非文字檔			
		dic['data'] = '圖檔'
	all.append(dic)

#輸出
out_dir = './data'
out_name = '留言內容2.csv'
df = pandas.DataFrame(data = all)
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
fullname = os.path.join(out_dir, out_name)    
df.to_csv(fullname, encoding='utf_8_sig', index=False)

print("OK")