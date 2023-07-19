from http import HTTPStatus

from bs4 import BeautifulSoup
from requests import RequestException

from constants import LOGGING_PHRASE
from exceptions import ParserFindTagException, UrlNotAvailable


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise ConnectionError(
            LOGGING_PHRASE['connection_error'].format(args=url)
        )


def get_soup(session, url):
    response = get_response(session, url)
    if response.status_code != HTTPStatus.OK:
        raise UrlNotAvailable(
            f'URL не доступен, {response.status_code}, {response.reason}')
    return BeautifulSoup(response.text, features='lxml')


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=attrs if attrs is not None else {})
    if searched_tag is None:
        raise ParserFindTagException(
            'Не найден тег {tag} {attrs}'.format(tag=tag, attrs=attrs)
        )
    return searched_tag
