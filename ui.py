

from config import ACCOUNT, PASSWORD


def validate_login(username: str, passowrd: str):
    import time

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    driver = webdriver.Chrome()
    driver.get('https://pintia.cn/auth/login')

    # wait for page load
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_elements(By.TAG_NAME, 'input'))

    # find all input elements
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    username_input = inputs[0]
    password_input = inputs[1]
    remember_me = inputs[2]
    login_button = driver.find_elements(By.TAG_NAME, 'button')[0]

    # fill in the form
    username_input.send_keys(username)
    password_input.send_keys(passowrd)
    remember_me.click()
    driver.implicitly_wait(1)
    login_button.click()

    # TODO: auto login for netease login

    while driver.current_url != 'https://pintia.cn/problem-sets/dashboard':
        time.sleep(1)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


if __name__ == '__main__':
    validate_login(ACCOUNT, PASSWORD)
