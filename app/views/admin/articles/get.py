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


import functools
from urllib.parse import urlencode

from flet_core import Container, Row, Column, ScrollMode

from app.controls.button import FilledButton
from app.controls.button.switch import StitchButton
from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminView, Section
from app.utils import Fonts
from app.views.admin.articles.create import CreateArticleView
from app.views.admin.articles.translations.create import ArticleCreateTranslationView
from app.views.admin.articles.translations.get import ArticleTranslationView
from config import URL_ARTICLES_UPDATE, URL_ARTICLES_GET


class ArticleView(AdminView):
    route = '/admin'
    article = list[dict]
    is_hide = bool

    def __init__(self, article_id):
        super().__init__()
        self.article_id = article_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.article.get(
            id_=self.article_id
        )
        self.article = response.article
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key=self.article['name_text']),
                        main_section_controls=[
                            StitchButton(
                                label=await self.client.session.gtv(key='admin_article_get_view_hide'),
                                value=self.article['is_hide'],
                                on_change=self.change_visibility
                            ),
                            Row(
                                controls=[
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='admin_article_get_view'),
                                        ),
                                        url=URL_ARTICLES_GET + urlencode(
                                            {
                                                'id_': self.article.get('id'),
                                                'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                                'is_admin': False,
                                            },
                                        ),
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='update'),
                                        ),
                                        url=URL_ARTICLES_UPDATE + urlencode(
                                            {
                                                'id_': self.article.get('id'),
                                                'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                                'is_admin': True,
                                            },
                                        ),
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='delete'),
                                        ),
                                        on_click=self.delete_article,
                                    ),

                                ],
                            ),
                        ],
                        sections=[
                            Section(
                                title=await self.client.session.gtv(key='admin_article_get_view_translations'),
                                on_create_click=self.create_translation,
                                controls=[
                                    Card(
                                        controls=[
                                            Text(
                                                value=await self.client.session.gtv(
                                                    key=translation.get('language')
                                                ),
                                                size=15,
                                                font_family=Fonts.REGULAR,
                                            ),
                                        ],
                                        on_click=functools.partial(self.translate_view, translation),
                                    )
                                    for translation in self.article['translations']
                                ],
                            ),
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def delete_article(self, _):
        await self.client.session.api.article.delete(
            id_=self.article_id
        )
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()

    async def change_visibility(self, _):
        await self.client.session.api.article.update(
            id_=self.article_id,
            is_hide=not self.article['is_hide'],
        )
        await self.update_async()

    async def create_translation(self, _):
        await self.client.change_view(view=ArticleCreateTranslationView(article_id=self.article_id))

    async def create_article(self, _):
        await self.client.change_view(view=CreateArticleView())

    async def translate_view(self, translation, _):
        await self.client.change_view(view=ArticleTranslationView(
            article_id=self.article_id,
            language=translation
            ),
        )
