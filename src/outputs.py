import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (DATETIME_FORMAT, RESULTS_DIR, DIALECT, PRETTY, FILE,
                       LOGGING_PHRASE)


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
    RESULTS_DIR.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = RESULTS_DIR / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=DIALECT)
        writer.writerows(results)
    logging.info(LOGGING_PHRASE['file'].format(args=file_path))


CHOOSE_OUTPUT = {
    PRETTY: pretty_output,
    FILE: file_output,
    '': default_output
}


def control_output(results, cli_args):
    output = cli_args.output if cli_args.output else ''
    CHOOSE_OUTPUT[output](results, cli_args)
