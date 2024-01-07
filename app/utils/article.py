from urllib.parse import urlencode

from config import IS_TEST

URL_ARTICLES_TEST_GET = 'https://articles.test.mybody.one/get?'
URL_ARTICLES_TEST_UPDATE = 'https://articles.test.mybody.one/update?'
URL_ARTICLES_GET = 'https://articles.mybody.one/get?'
URL_ARTICLES_UPDATE = 'https://articles.mybody.one/update?'


class UrlTypes:
    GET = 'get'
    UPDATE = 'update'


def get_url_article(id_, token, is_admin, type_, language=None):

    url_base = None

    if type_ == UrlTypes.GET:
        if IS_TEST:
            url_base = URL_ARTICLES_TEST_GET
        else:
            url_base = URL_ARTICLES_GET
    elif type_ == UrlTypes.UPDATE:
        if IS_TEST:
            url_base = URL_ARTICLES_TEST_UPDATE
        else:
            url_base = URL_ARTICLES_UPDATE

    params = {
        'id_': id_,
        'token': token,
        'is_admin': is_admin,
    }

    if language:
        params['language'] = language

    return url_base + urlencode(params)
