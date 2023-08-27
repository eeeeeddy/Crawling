from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Chrome 브라우저로 실행해라
driver = webdriver.Chrome()

# get() : 페이지 이동
driver.get("http://www.python.org")

# 요소 중에서 name의 속성 값이 'q' 인 값을 찾아라
# 요소가 1개일 때 -> find_element()
# 요소가 1개 이상일 때 -> find_elements() : 리스트 형태로 반환
elem = driver.find_element(By.NAME, "q")

# Input 태그의 입력란 초기화
elem.clear()

# send_keys() : 문자열 전달(입력), 명령 실행
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

# 사용이 끝나면 close()로 종료
driver.close()