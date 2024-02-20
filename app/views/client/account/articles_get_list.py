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


import webbrowser
from functools import partial

from flet_core import Text

from app.controls.information.card import Card
from app.controls.layout import ClientBaseView
from app.utils import Fonts
from app.utils.article import get_url_article, UrlTypes


class ArticleListView(ClientBaseView):
    route = '/client/article/list/get'
    articles: dict

    async def build(self):
        await self.set_type(loading=True)
        self.articles = await self.client.session.api.client.articles.get_list()
        await self.set_type(loading=False)
        visible_articles = [article for article in self.articles if not article['is_hide']]

        controls = []
        if visible_articles:
            for article in visible_articles:
                controls.append(
                    Card(
                        controls=[
                            Text(
                                value=await self.client.session.gtv(key=article['name_text']),
                                size=18,
                                font_family=Fonts.SEMIBOLD,
                            ),
                        ],
                        on_click=partial(self.article_view, article['id']),
                    )
                )
        else:
            controls.append(
                Text(
                    value=await self.client.session.gtv(key='not_articles'),
                    size=18,
                    font_family=Fonts.SEMIBOLD,
                )
            )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='articles'),
            main_section_controls=controls,
        )

    async def article_view(self, article_id, _):
        url = get_url_article(
            id_=article_id,
            token=self.client.session.token,
            is_admin=False,
            type_=UrlTypes.GET,
        )
        webbrowser.open(url)
