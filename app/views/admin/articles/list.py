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

from flet_core import Container, Row, MainAxisAlignment, Card, Text, Column, ScrollMode

from app.controls.button import FilledButton
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.articles.create import CreateArticleView
from app.views.admin.articles.get import ArticleView


class ArticleListView(View):
    route = '/admin'

    def __init__(self, articles_data):
        super().__init__()
        self.articles_data = articles_data

    async def build(self):
        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='Articles'),
                            on_create_click=self.create_article,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=await self.client.session.gtv(key=article['name_text']),
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.article_view, article),
                            ),
                            margin=0,
                        )
                        for article in self.articles_data.articles
                    ],
                ),
                padding=10,
            ),

        ]

    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def create_article(self, _):
        await self.client.change_view(view=CreateArticleView())

    async def article_view(self, articles_data, _):
        await self.client.change_view(view=ArticleView(articles_data=articles_data))
