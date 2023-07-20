from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

LOGGING_CONNECTION_ERROR = (
    'Возникла ошибка при загрузке страницы {url}'
)
LOGGING_TAG_ERROR = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException :
        raise ConnectionError(
            LOGGING_CONNECTION_ERROR.format(url=url)
        )


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features=features)


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=attrs if attrs is not None else {})
    if searched_tag is None:
        raise ParserFindTagException(
            LOGGING_TAG_ERROR.format(tag=tag, attrs=attrs)
        )
    return searched_tag
