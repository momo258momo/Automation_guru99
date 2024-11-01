from selenium import webdriver
from selenium.webdriver.common.by import By
#Đănh nhập

driver = webdriver.Firefox()

username = "mngr599452"
password = "pEtUmeh"
login_url = "https://www.demo.guru99.com/V4"
driver.get(login_url)

username_field = driver.find_element(By.NAME,"uid")
password_field = driver.find_element(By.NAME,"password")

username_field.send_keys(username)
password_field.send_keys(password)

login_button = driver.find_element(By.NAME,"btnLogin")
assert not login_button.get_attribute("disabled")
login_button.click()

success_element = driver.find_element(By.CSS_SELECTOR, ".barone")
assert success_element.text == "Guru99 Bank"


