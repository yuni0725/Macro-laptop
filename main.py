from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pause
from datetime import datetime, date

from login import *
from apply import *

from random import randint

URL = "http://mysangsan.cafe24.com/dms/regi/login.php"

#setting time
today = date.today()

login_time = datetime(today.year, today.month, today.day, 6, 28, 30) #6시 28분 30초
submit_time = datetime(today.year, today.month, today.day, 6, 29, 0) #6시 29분 

#setting driver
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)
driver.implicitly_wait(time_to_wait=5)

pause.until(login_time)

#login
login(driver)
login(driver)
agree(driver)

#apply
apply_access(driver)

value = randint(1, 8)

print(f"Applying for laptop number : {value}")

pause.until(submit_time)

while True:
    try:
        text = driver.find_element(By.CSS_SELECTOR, "body > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > b > font")
        print("Waiting for apply...")
        driver.execute_script("location.reload()")
        sleep(0.5)
    except:
        while True:
            apply(driver, value)
            sleep(0.1)


