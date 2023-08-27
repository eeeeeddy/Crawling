from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://www.opinet.co.kr/user/main/mainView.do")
time.sleep(2)
test = driver.find_elements(By.CLASS_NAME, "gnbTopa")[0]
ActionChains(driver).move_to_element(test).perform()
time.sleep(2)
driver.find_element(By.LINK_TEXT, "지역별").click()

region = driver.find_element(By.ID, "SIDO_NM0")
region_detail = region.find_elements(By.TAG_NAME, "option")
for i in region_detail:
    print(i.text)

# 지역을 "부산"으로 선택
region_detail[2].click()
time.sleep(2)

region_second = driver.find_element(By.NAME, "SIGUNGU_NM0")
region_second_detail = region_second.find_elements(By.TAG_NAME, "option")[1:]

# <p class="haha">안녕?</p> <- get_attribute("class") = "haha"
# 강서구, 금정구, 기장군, 남구, ...
region_second_detail_list = [i.get_attribute("value") for i in region_second_detail]

for i in region_second_detail:
    # print(i.text)
    region_second = driver.find_element(By.NAME, "SIGUNGU_NM0")
    region_second_detail = region_second.find_elements(By.TAG_NAME, "option")[1:]
    i.click()
    time.sleep(2)

    # 반복할 지역구를 하나씩 선택
    i.click()
    time.sleep(2)

    # 조회 버튼 클릭
    driver.find_element(By.ID, "searRgSelect").click()
    time.sleep(2)

    # 엑셀 저장 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="glopopd_excel"]').click()
    time.sleep(2)

driver.close()