import os
from pathlib import Path

from dotenv import load_dotenv

URL = 'https://hh.ru/'
URL_LOGIN = 'account/login?backurl=%2F&hhtmFrom=main'
URL_RESUME = 'applicant/resumes?hhtmFrom=main&hhtmFromLabel=header'

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

INTERVAL = 60 * 30
STEP_INTERVAL = 1

BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'log.log'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

DT_FORMAT = '%d.%m.%Y %H:%M:%S'

COOKIES_DIR = BASE_DIR / 'cookies'
COOKIES_FILE = COOKIES_DIR / f'{LOGIN}_cookies'
