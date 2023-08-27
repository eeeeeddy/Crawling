from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# 웹 사이트 접근
driver = webdriver.Chrome()
# driver.maximize_window()
driver.get("http://shshop.testy.kr")
time.sleep(2)

# Link_Text
# driver.find_element(By.LINK_TEXT, "패션의류")
driver.get("http://shshop.testy.kr/shop/goods_list.php?cate_id=1")
time.sleep(2)
categorySearch = driver.find_element(By.CSS_SELECTOR, "input.input_box150")
categorySearch.send_keys("자켓")
time.sleep(2)
driver.find_elements(By.CLASS_NAME, "button_small")[1].click()
time.sleep(2)

# # 검색창에 티셔츠 검색
# searchElem = driver.find_element(By.NAME, "sch_text")
# searchElem.send_keys("티셔츠")
# searchElem.send_keys(Keys.RETURN)
# time.sleep(3)
#
# # 상품 티셔츠 제목 추출
# searchList = driver.find_elements(By.CLASS_NAME, 'goods_name')
# for i in searchList:
#     print(i.text)

# Selenium 드라이버 종료
driver.close()