import time, traceback, datetime, os
from lib.info import create_driver, get_profile_name, parse_line
from selenium.webdriver.common.by import By

def tinder_login(driver):
    driver.find_element(By.CSS_SELECTOR, "a[class='c1p6lbu0 Miw(120px)'] div[class='l17p5q9z']").click()
    time.sleep(5)
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    time.sleep(2)
    driver.find_element(By.XPATH, "(//body)[1]").click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']").click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(15)

def loginer(port):
    now = datetime.datetime.now()
    parent_dir = "D:/Skript/Tinder Shade/Screenshots/logged_in"
    directory = now.strftime("%Y_%m_%d %H_%M_%S")
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    while True:
        try:
            session = parse_line("sessions_to_login")
            session_name = get_profile_name(session, port)
            driver = create_driver(session, port)
            driver.get("https://tinder.com")
            time.sleep(15)
            tinder_login()
            driver.save_screenshot(f'{path}/{session_name.strip()}.png')
            driver.quit()
        except:
            traceback.print_exc()
            try:
                driver.quit()
            except:
                pass
            continue

