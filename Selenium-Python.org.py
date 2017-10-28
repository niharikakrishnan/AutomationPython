from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_id("searchText")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
WebDriverWait(10)
assert "No results found." not in driver.page_source
driver.close()
