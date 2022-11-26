import pickle
from datetime import datetime
from os import path
from time import sleep

from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from configs import configure_logging
from constants import (COOKIES_DIR, COOKIES_FILE, DT_FORMAT, INTERVAL,
                       LOGIN, PASSWORD, STEP_INTERVAL, URL, URL_LOGIN,
                       URL_RESUME, COUNT_OF_WAIT_ATTEMPTS)
from elements import (account_login_error, bloko_modal, login_by_password,
                      login_input_password, login_input_username, login_submit,
                      mainmenu_my_resumes, resume_update_button)
from exceptions import LoginOrPasswordErrorException

logger = configure_logging()

init(autoreset=True)

start_time = None


def get_time() -> str:
    """Возвращает текущее время."""
    return datetime.now().strftime(DT_FORMAT)


def _wait(
    driver: WebDriver, locator: str, selector: str
) -> list[WebElement] | None:
    """Функция ожидания необходимого контрола."""
    max_wait = 10

    for _ in range(COUNT_OF_WAIT_ATTEMPTS):
        try:
            return WebDriverWait(driver, max_wait).until(
                EC.presence_of_all_elements_located((locator, selector))
            )
        except:
            driver.refresh()


def _is_not_element_present(
    driver: WebDriver, locator: str, selector: str
) -> list[WebElement] | None:
    max_wait = 4

    try:
        WebDriverWait(driver, max_wait).until(
            EC.presence_of_element_located((locator, selector)))
    except TimeoutException:
        return True

    return False


def update_resume(d: WebDriver) -> None:
    """Поднятие резюме."""
    d.get(URL + URL_RESUME)
    _wait(d, By.XPATH, resume_update_button)
    buttons_update = d.find_elements(By.XPATH, resume_update_button)
    for i, button_update in enumerate(buttons_update, start=1):
        if button_update.text == 'Поднять в поиске':
            button_update.click()
            _wait(d, By.XPATH, bloko_modal)
            logger.info(str_ := f'Поднял резюме под номером {i}.')
            print(Fore.GREEN + f'{get_time()} {str_}')
        else:
            logger.info(
                str_ := f'Время для поднятия резюме под номером {i} '
                'еще не пришло...'
            )
            print(Fore.BLUE + f'{get_time()} {str_}')


def get_cookies(d: WebDriver) -> WebDriver:
    """Сохранение или получение cookies."""
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

    if not _is_not_element_present(d, By.XPATH, account_login_error):
        raise LoginOrPasswordErrorException

    _wait(d, By.XPATH, mainmenu_my_resumes)

    with open(COOKIES_FILE, 'wb') as file:
        pickle.dump(d.get_cookies(), file)
        logger.info('Cookies записаны в файл.')

    return d


def set_options() -> Options:
    """Установка опций для драйвера."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--log-level=3')
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging', 'enable-automation']
    )
    options.add_experimental_option('useAutomationExtension', False)
    return options


def main() -> None:
    """Точка входа в программу. Создание драйвера, применение опций."""
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=set_options())
    logger.info('-' * 30)
    logger.info('Драйвер запущен!')
    try:
        driver = get_cookies(driver)
        update_resume(driver)
    except LoginOrPasswordErrorException as error:
        print(Fore.RED + f'{get_time()} Неправильные данные для входа.')
        logger.exception(error, exc_info=True)
        exit()
    except WebDriverException as error:
        print(
            Fore.RED + f'{get_time()} Пытаюсь взаимодействовать с не '
            'существующим контролом.'
        )
        logger.exception(error, exc_info=True)
    except Exception as error:
        print(Fore.RED + f'{get_time()} Непредвиденная ошибка.')
        logger.exception(error, exc_info=True)
        exit()
    finally:
        driver.quit()
        logger.info('Драйвер остановлен!')


# Проверяю действительно ли куки живут целлый год, или отваливаются раньше,
# если куки будут отваливаться, попробовать запустить код с этой функцией.

# def check_cookie():
#     """Удаляет куки каждую неделю."""
#     global start_time
#     if start_time is None:
#         start_time = datetime.now()

#     end_time = datetime.now() - start_time
#     if end_time.seconds >= LIFE_TIME:
#         shutil.rmtree(COOKIES_DIR)
#         start_time = None


if __name__ == '__main__':
    print(get_time(), 'Старт работы.')
    # shutil.rmtree(COOKIES_DIR, ignore_errors=True)
    while True:
        main()
        # check_cookie()
        for i in tqdm(
            range(INTERVAL),
            desc=(f'{get_time()} До следующей проверки:')
        ):
            sleep(STEP_INTERVAL)
