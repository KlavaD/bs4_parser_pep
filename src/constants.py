import csv
from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS_DIR = BASE_DIR / 'results'
DOWNLOADS_DIR = BASE_DIR / 'downloads'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DIALECT = csv.unix_dialect()

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

PRETTY = 'pretty'
FILE = 'file'

LOGGING_PHRASE = {
    'start': 'Парсер запущен!',
    'stop': 'Парсер завершил работу.',
    'args': 'Аргументы командной строки: {args}',
    'file': 'Файл с результатами был сохранён: {args}',
    'download': 'Архив был загружен и сохранён: {args}',
    'error': 'Сбой в работе программы {args}',
    'connection_error': 'Возникла ошибка при загрузке страницы {args}',
}