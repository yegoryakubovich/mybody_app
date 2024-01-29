#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from urllib.parse import urlencode

from config import settings


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
        if settings.is_test:
            url_base = URL_ARTICLES_TEST_GET
        else:
            url_base = URL_ARTICLES_GET
    elif type_ == UrlTypes.UPDATE:
        if settings.is_test:
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
