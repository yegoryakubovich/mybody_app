#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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

from flet_core import Container, Row, MainAxisAlignment, Card, Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.articles.create import CreateArticleView
from config import URL_ARTICLES_UPDATE, URL_ARTICLES_GET


class ArticleView(View):
    route = '/admin'
    articles = list[dict]

    def __init__(self, article_id):
        super().__init__()
        self.article_id = article_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.article.get()
        self.articles = response.articles
        await self.set_type(loading=False)

        translations = self.articles.get('translations', [])

        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=await self.client.session.gtv(key=self.articles['name_text']),
                         on_create_click=self.create_article,
                        ),
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='get_article'),
                                    ),
                                    url=URL_ARTICLES_GET + urlencode(
                                        {
                                            'id_': self.articles.get('id'),
                                            'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                            'is_admin': False,
                                        },
                                    ),
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='update_article'),
                                    ),
                                    url=URL_ARTICLES_UPDATE + urlencode(
                                        {
                                            'id_': self.articles.get('id'),
                                            'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                            'is_admin': True,
                                        },
                                    ),
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='change_visibility'),
                                    ),
                                    on_click=self.change_visibility,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='delete_article'),
                                    ),
                                    on_click=self.delete_article,
                                ),

                            ],
                        ),
                        Row(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key='translation'),
                                    size=30,
                                    font_family=Fonts.BOLD,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='create_translation'),
                                    ),
                                    on_click=self.create_translation,
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=await self.client.session.gtv(
                                                key=translation.get('language')
                                            ),
                                            size=15,
                                            font_family=Fonts.REGULAR,
                                        ),
                                        Row()
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                url=URL_ARTICLES_GET.format(
                                    id_=self.articles.get('id')) + urlencode(
                                    {
                                        'is_admin': True,
                                        'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                    },
                                ),
                            ),
                            margin=0,
                        )
                        for translation in translations
                     ],
                ),
                padding=10,
            ),
        ]

    async def delete_article(self, _):
        from app.views.admin.articles.list import ArticleListView
        await self.client.session.api.article.delete(
            id=self.article_id
        )
        await self.client.change_view(view=ArticleListView())

    async def change_visibility(self, _):
        pass

    async def create_translation(self, _):
        pass

    async def create_article(self, _):
        await self.client.change_view(view=CreateArticleView())
