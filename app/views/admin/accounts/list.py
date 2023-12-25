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

from flet_core import Container, Row, Card, Text, Column, ScrollMode

from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.articles.create import CreateArticleView
from app.views.admin.articles.get import ArticleView


class AccountListView(View):
    route = '/admin'
    accounts: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.account.get()
        self.accounts = response  # FIXME
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='Account'),
                            on_create_click=self.create_article,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Row(
                                            controls=[
                                                Text(
                                                    value=await self.client.session.gtv(
                                                        key=account['firstname']),
                                                    size=18,
                                                    font_family=Fonts.SEMIBOLD,
                                                ),
                                                Text(
                                                    value=await self.client.session.gtv(
                                                        key=account['lastname']),
                                                    size=18,
                                                    font_family=Fonts.SEMIBOLD,
                                                ),
                                            ],
                                        ),
                                        Text(
                                            value=await self.client.session.gtv(key=account['country']),
                                            size=15,
                                            font_family=Fonts.REGULAR,
                                        ),
                                        Text(
                                            value=await self.client.session.gtv(key=account['language']),
                                            size=15,
                                            font_family=Fonts.REGULAR,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.article_view, account['id']),
                            ),
                            margin=0,
                        )
                        for account in self.accounts
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_article(self, _):
        await self.client.change_view(view=CreateArticleView())

    async def article_view(self, article_id, _):
        await self.client.change_view(view=ArticleView(article_id=article_id))
