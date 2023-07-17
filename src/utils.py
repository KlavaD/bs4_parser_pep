import logging

from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def cmp_status(soup, status, link):
    dl_tag = find_tag(soup, 'dl', {'class': 'rfc2822 field-list simple'})
    status_tag = dl_tag.find(string='Status').parent.find_next_sibling('dd')
    status_card = status_tag.abbr.text
    if status_card not in status:
        error_msg = (f'Несовпадающие статусы:',
                     f'{link}',
                     f'Статус в карточке: {status_card}',
                     f'Ожидаемые статусы: {status}')
        logging.error(error_msg)
    return status_card
