import time, os, re, sys,  string, datetime, traceback, configparser
from selenium.webdriver.common.by import By
from core.parse_shadow_ids import get_shadows, lock
from core.loginer import tinder_login
from lib.group import group
from lib.info import *

config = configparser.ConfigParser()

config.read('config.ini')
port = config.get('Settings', 'port')


def core():
    fold = "Screen/"
    mat_group, ver_group, sha_group, cap_group = group(port)
    folder_checker(fold)
    now = datetime.datetime.now()
    directory = now.strftime("%Y_%m_%d %H_%M_%S")
    path = os.path.join(fold, directory)
    os.mkdir(path)
    locked_ver, locked_sha = get_shadows(ver_group, sha_group, port)
    lock(locked_ver, 1)
    lock(locked_sha, 2)

    return path, mat_group, cap_group


def screenshoter(port, path, mat_group, cap_group):

    while True:
        try:
            session = parse_line("sessions").strip()
            session_name = parse_line("session_names").strip()
            driver = create_driver(session=session, port=port)
            pattern = r'[' + string.punctuation + ']'
            session_name = re.sub(pattern, "", session_name)
            driver.get("https://tinder.com")
            time.sleep(10)
            try:
                tinder_login(driver=driver)
            except:
                pass

            try:
                driver.find_element(By.XPATH, "(//span[@class='D(b) Expand'])[1]").click()
                time.sleep(2)
                driver.find_element(By.XPATH, "(//span[@class='D(b) Expand'])[3]").click()
                time.sleep(10)
                try:
                    driver.find_element(By.TAG_NAME, "textarea").send_keys("hi")
                    update_profile_group(session, mat_group, port)
                    continue
                except:
                    print("shadow")
                    continue
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, "h3[class='Fz($m) Typs(heading-1)']")
                    time.sleep(1)
                    delete(session)
                except:
                    update_profile_group(session, cap_group, port)
        except:
            pass
        finally:
            try:
                driver.save_screenshot(f'{path}/{session_name.strip()}{session}.png')
            except:
                traceback.print_exc()
                pass
            try:
                driver.quit()
            except:
                pass
