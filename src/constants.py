from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS_DIR = BASE_DIR / 'results'
DOWNLOADS_DIR = BASE_DIR / 'downloads'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

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

OUTPUT_TABLE = 'pretty'
OUTPUT_FILE = 'file'

# LOGGING_PHRASE = {
#     'start': 'Парсер запущен!',
#     'stop': 'Парсер завершил работу.',
#     'args': 'Аргументы командной строки: {args}',
#     'file': 'Файл с результатами был сохранён: {args}',
#     'download': 'Архив был загружен и сохранён: {args}',
#     'error': 'Сбой в работе программы {args}',
#     'connection_error': 'Возникла ошибка при загрузке страницы {args}',
# }

# LOGGING_START = 'Парсер запущен!'
# LOGGING_FINISH = 'Парсер завершил работу.'
# LOGGING_COMMAND_ARGS = 'Аргументы командной строки: {args}'
# LOGGING_OUTPUT_FILE = 'Файл с результатами был сохранён: {args}'
# LOGGING_DOWNLOAD = 'Архив был загружен и сохранён: {args}'
# LOGGING_ERROR = 'Сбой в работе программы {args}'
