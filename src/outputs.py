import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (DATETIME_FORMAT, BASE_DIR, OUTPUT_TABLE, OUTPUT_FILE)

LOGGING_OUTPUT_FILE = 'Файл с результатами был сохранён: {args}'
DIALECT = csv.unix_dialect()
RESULTS_DIR = BASE_DIR / 'results'


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(f, dialect=DIALECT).writerows(results)
        logging.info(LOGGING_OUTPUT_FILE.format(args=file_path))


CHOOSE_OUTPUT = {
    OUTPUT_TABLE: pretty_output,
    OUTPUT_FILE: file_output,
    None: default_output
}


def control_output(results, cli_args):
    CHOOSE_OUTPUT[cli_args.output](results, cli_args)
