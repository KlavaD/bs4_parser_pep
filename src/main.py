import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (MAIN_DOC_URL, PEP_DOC_URL, DOWNLOADS_DIR,
                       LOGGING_PHRASE, EXPECTED_STATUS)

from exceptions import ParserFindTagException
from outputs import control_output
from utils import get_soup, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1')
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup(session, version_link)
        results.append((
            version_link,
            find_tag(soup, 'h1').text,
            find_tag(soup, 'dl').text.replace('\n', ' ')
        ))
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    ul_tags = soup.select('div.sphinxsidebarwrapper ul')
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
    soup = get_soup(session, downloads_url)
    pdf_a4_link = soup.select_one('table.docutils a[href$=pdf-a4\.zip]')['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(LOGGING_PHRASE['download'].format(args=archive_path))


def pep(session):
    soup = get_soup(session, PEP_DOC_URL)
    count_status_peps = defaultdict(int)
    tbody_tags = soup.select('#index-by-category tbody')
    error_status_message = None
    for tbody in tqdm(tbody_tags):
        tr_tags = tbody.find_all('tr')
        for tr in tr_tags:
            status = tr.find('abbr').text[1:]
            pep_link = urljoin(
                PEP_DOC_URL,
                tr.find('a', class_='pep reference internal')['href']
            )
            soup = get_soup(session, pep_link)
            dl_tag = find_tag(soup, 'dl',
                              {'class': 'rfc2822 field-list simple'})
            status_tag = dl_tag.find(string='Status').parent.find_next_sibling(
                'dd')
            status_card = status_tag.abbr.text
            if status_card not in EXPECTED_STATUS[status]:
                error_status_message = (
                    'Несовпадающие статусы: '
                    f'{pep_link} '
                    f'Статус в карточке: {status_card} '
                    f'Ожидаемые статусы: {EXPECTED_STATUS[status]}'
                )
            count_status_peps[status_card] += 1
    if error_status_message:
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
    logging.info(LOGGING_PHRASE['start'])
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(LOGGING_PHRASE['args'].format(args=args))
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    try:
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            LOGGING_PHRASE['error'].format(args=error)
        )
    logging.info(LOGGING_PHRASE['stop'])


if __name__ == '__main__':
    main()
