from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def login(driver):
#id
    id_box = driver.find_element(By.CSS_SELECTOR, 'body > table:nth-child(3) > tbody > tr > td > table > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]')

    id_box.send_keys("STUDENT_ID") #STUDENT_ID
    id_box.send_keys(Keys.TAB)

#password
    password_box = driver.find_element(By.CSS_SELECTOR, 'body > table:nth-child(3) > tbody > tr > td > table > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input[type=password]')

    password_box.send_keys("PASSWORD") #PASSWORD
    password_box.send_keys(Keys.TAB)

#security code
    code_list = []
    codes = driver.find_elements(By.CSS_SELECTOR,'b')

    for code in codes:
        code_list.append(code.get_attribute("innerHTML")) 

    code_list = code_list[2:]   

    code = ''.join(code_list)

    code_box = driver.find_element(By.CSS_SELECTOR, 'body > table:nth-child(3) > tbody > tr > td > table > tbody > tr > td > table:nth-child(4) > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > form > table > tbody > tr:nth-child(5) > td:nth-child(2) > input[type=text]')
    code_box.send_keys(code)
    code_box.send_keys(Keys.ENTER)

    print("Login Succeeded!")

def agree(driver):
    arg1_y = driver.find_element(By.CSS_SELECTOR, "#agr1_y")
    arg1_y.click()

    arg2_y = driver.find_element(By.CSS_SELECTOR, "#agr2_y")
    arg2_y.click()

    enter = driver.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(5) > td > input[type=button]:nth-child(1)")
    enter.click()

    print("Agree Succeeded!")

    