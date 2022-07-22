import pickle
from datetime import datetime
from os import path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from configus import configure_logging
from constants import (URL, URL_RESUME, URL_LOGIN, LOGIN, PASSWORD, INTERVAL,
                       STEP_INTERVAL, DT_FORMAT, COOKIES_DIR, COOKIES_FILE)
from elements import (login_by_password, login_input_password,
                      login_input_username, login_submit, mainmenu_my_resumes,
                      resume_update_button, bloko_modal)

logger = configure_logging()


def _wait(driver, locator, selector):
    """Функция ожидания необходимого контрола.
    """
    max_wait = 10
    WebDriverWait(driver, max_wait).until(
        EC.presence_of_all_elements_located((locator, selector))
    )


def update_resume(d):
    """Поднятие резюме.
    """
    d.get(URL + URL_RESUME)
    _wait(d, By.XPATH, resume_update_button)

    button_update = d.find_element(By.XPATH, resume_update_button)
    if button_update.text == 'Поднять в поиске':
        button_update.click()
        _wait(d, By.XPATH, bloko_modal)
        logger.info(str_ :='Поднял резюме.')
        print(str_)
    else:
        logger.info(str_ := 'Время еще не пришло...')
        print(str_)


def get_cookies(d):
    """Сохранение или получение cookies.
    """
    COOKIES_DIR.mkdir(exist_ok=True)

    if path.exists(COOKIES_FILE):
        d.get(URL)
        with open(COOKIES_FILE, 'rb') as file:
            for cookie in pickle.load(file):
                d.add_cookie(cookie)
            d.refresh()
            logger.info('Cookies добавлены к драйверу.')
            return d

    d.get(URL + URL_LOGIN)
    _wait(d, By.XPATH, login_by_password)

    d.find_element(By.XPATH, login_by_password).click()
    _wait(d, By.XPATH, login_input_username)

    d.find_element(By.XPATH, login_input_username).send_keys(LOGIN)
    d.find_element(By.XPATH, login_input_password).send_keys(PASSWORD)
    d.find_element(By.XPATH, login_submit).click()
    _wait(d, By.XPATH, mainmenu_my_resumes)

    with open(COOKIES_FILE, 'wb') as file:
        pickle.dump(d.get_cookies(), file)
        logger.info('Cookies записаны в файл.')

    return d


def set_options():
    """Установка опций для драйвера.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-infobars')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options


def main():
    """Точка входа в программу. Создание драйвера, применение опций.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=set_options())
    logger.info('-' * 30)
    logger.info('Драйвер запущен!')
    try:
        driver = get_cookies(driver)
        update_resume(driver)
    except Exception as error:
        logger.error(error)
    finally:
        driver.quit()
        logger.info('Драйвер остановлен!')


if __name__ == '__main__':
    while True:
        print('Старт работы.')
        main()
        time_now = datetime.now().strftime(DT_FORMAT)
        for i in tqdm(
                range(INTERVAL),
                desc=f'{time_now} До следующей проверки:'):
            sleep(STEP_INTERVAL)
