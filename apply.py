from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert

def apply_access(driver):
    apply_box = driver.find_element(By.CSS_SELECTOR, "body > table:nth-child(3) > tbody > tr > td > table > tbody > tr > td > ul > li:nth-child(4) > ul > li:nth-child(3) > a")
    URL_APPLY = apply_box.get_attribute("href")
    driver.get(url = URL_APPLY)

    print("Apply Access Succeeded!")

def apply(driver, value):
    driver.execute_script("location.reload()")

    select = Select(driver.find_element(By.NAME, "sel_roomseq"))

    select.select_by_value("0" + f"{value}")
        
    text_box = driver.find_element(By.CSS_SELECTOR, "body > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > form > table:nth-child(9) > tbody > tr:nth-child(2) > td:nth-child(2) > b > textarea")
    text_box.send_keys(".")

    submit_button = driver.find_element(By.CSS_SELECTOR, "body > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > form > table:nth-child(9) > tbody > tr:nth-child(2) > td:nth-child(3) > input[type=button]")
    submit_button.click()

    Alert(driver).accept()

    
