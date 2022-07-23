import pickle
from datetime import datetime
from os import path
from time import sleep
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from configs import configure_logging
from constants import (COOKIES_DIR, COOKIES_FILE, DT_FORMAT, INTERVAL, LOGIN,
                       PASSWORD, STEP_INTERVAL, URL, URL_LOGIN, URL_RESUME)
from elements import (account_login_error, bloko_modal, login_by_password,
                      login_input_password, login_input_username, login_submit,
                      mainmenu_my_resumes, resume_update_button)
from exceptions import LoginOrPasswordErrorException

logger = configure_logging()


def get_time():
    """Возвращает текущее время.
    """
    return datetime.now().strftime(DT_FORMAT)


def _wait(driver: WebDriver, locator: Any, selector: str):
    """Функция ожидания необходимого контрола.
    """
    max_wait = 10
    try:
        return WebDriverWait(driver, max_wait).until(
            EC.presence_of_all_elements_located((locator, selector))
        )
    except:
        return 0


def update_resume(d: WebDriver):
    """Поднятие резюме.
    """
    d.get(URL + URL_RESUME)
    _wait(d, By.XPATH, resume_update_button)
    buttons_update = d.find_elements(By.XPATH, resume_update_button)
    for i, button_update in enumerate(buttons_update, start=1):
        if button_update.text == 'Поднять в поиске':
            button_update.click()
            _wait(d, By.XPATH, bloko_modal)
            logger.info(str_ := f'Поднял резюме под номером {i}.')
            print(get_time(), str_)
        else:
            logger.info(
                str_ := f'Время для поднятия резюме под номеро {i} '
                'еще не пришло...'
            )
            print(get_time(), str_)


def get_cookies(d: WebDriver):
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

    if _wait(d, By.XPATH, account_login_error):
        raise LoginOrPasswordErrorException

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
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
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
    except LoginOrPasswordErrorException as error:
        print(get_time(), 'Неправильные данные для входа.')
        logger.exception(error, exc_info=True)
    except Exception as error:
        print(get_time(), 'Непредвиденная ошибка.')
        logger.exception(error, exc_info=True)
    finally:
        driver.quit()
        logger.info('Драйвер остановлен!')


if __name__ == '__main__':
    while True:
        print(get_time(), 'Старт работы.')
        main()
        for i in tqdm(
            range(INTERVAL),
            desc=(f'{get_time()} До следующей проверки:')
        ):
            sleep(STEP_INTERVAL)
