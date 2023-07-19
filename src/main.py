import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    MAIN_DOC_URL, PEP_DOC_URL,
    EXPECTED_STATUS, BASE_DIR
)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_soup

LOGGING_START = 'Парсер запущен!'
LOGGING_FINISH = 'Парсер завершил работу.'
LOGGING_COMMAND_ARGS = 'Аргументы командной строки: {args}'
LOGGING_DOWNLOAD = 'Архив был загружен и сохранён: {args}'
LOGGING_ERROR = 'Сбой в работе программы {args}'
DOWNLOADS_DIR = BASE_DIR / 'downloads'
ERROR_STATUS_MESSAGE = ('Несовпадающие статусы: {link}'
                        ' Статус в карточке: {status_card} '
                        'Ожидаемые статусы: {status}'
                        )


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    a_tags = get_soup(session, whats_new_url).select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1 > a')
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    url_errors = []
    for a_tag in tqdm(a_tags):
        href = a_tag['href']
        version_link = urljoin(whats_new_url, href)
        try:
            soup = get_soup(session, version_link)
            results.append((
                version_link,
                find_tag(soup, 'h1').text,
                find_tag(soup, 'dl').text.replace('\n', ' ')
            ))
        except Exception as error:
            url_errors.append('{error}'.format(error=error))
    if len(url_errors) > 0:
        logging.error(url_errors)
    return results


def latest_versions(session):
    ul_tags = get_soup(
        session, MAIN_DOC_URL
    ).select('div.sphinxsidebarwrapper ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException(
            'Не найден список с версиями Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    pdf_a4_link = get_soup(session, downloads_url).select_one(
        'table.docutils a[href$="pdf-a4.zip"]'
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(LOGGING_DOWNLOAD.format(args=archive_path))


def pep(session):
    soup = get_soup(session, PEP_DOC_URL)
    count_status_peps = defaultdict(int)
    tbody_tags = soup.select('#index-by-category tbody')
    error_status_message = []
    url_errors = []
    for tbody in tqdm(tbody_tags):
        tr_tags = tbody.find_all('tr')
        for tr in tr_tags:
            status = tr.find('abbr').text[1:]
            pep_link = urljoin(
                PEP_DOC_URL,
                tr.find('a', class_='pep reference internal')['href']
            )
            try:
                soup = get_soup(session, pep_link)
                dl_tag = find_tag(soup, 'dl',
                                  {'class': 'rfc2822 field-list simple'})
                status_tag = dl_tag.find(
                    string='Status').parent.find_next_sibling(
                    'dd')
                status_card = status_tag.abbr.text
                if status_card not in EXPECTED_STATUS[status]:
                    error_status_message.append(
                        ERROR_STATUS_MESSAGE.format(
                            link=pep_link,
                            status_card=status_card,
                            status=EXPECTED_STATUS[status]
                        ))
                count_status_peps[status_card] += 1
            except Exception as error:
                url_errors.append('{error}'.format(error=error))
    if len(url_errors) > 0:
        logging.error(url_errors)
    if len(error_status_message):
        logging.error(error_status_message)
    return [
        ('Статус', 'Количество'),
        *count_status_peps.items(),
        ('Всего', sum(count_status_peps.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(LOGGING_START)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(LOGGING_COMMAND_ARGS.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            LOGGING_ERROR.format(args=error)
        )
    logging.info(LOGGING_FINISH)


if __name__ == '__main__':
    main()
