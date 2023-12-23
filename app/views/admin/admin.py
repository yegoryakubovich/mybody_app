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


from typing import Any

from flet_core import Container, Column, Row, Image, MainAxisAlignment
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.accounts.list import AccountListView
from app.views.admin.articles.list import ArticleListView
from app.views.admin.currencies.list import CurrencyListView
from app.views.admin.languages.list import LanguageListView
from app.views.admin.products.list import ProductListView
from app.views.admin.texts.list import TextListView
from app.views.admin.timezones import TimezoneListView


class Setting:
    name: str
    icon: str
    on_click: Any

    def __init__(self, name: str, icon: str, on_click: Any):
        self.name = name
        self.icon = icon
        self.on_click = on_click


class Section:
    name: str
    settings: list[Setting]

    def __init__(self, name: str, settings: list[Setting]):
        self.name = name
        self.settings = settings


class AdminView(View):
    route = '/admin'

    async def build(self):
        self.bgcolor = '#FFFFFF'
        sections = [
            Section(
                name='admin_panel',
                settings=[
                    Setting(
                        name='accounts_forms',
                        icon='notifications',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='articles',
                        icon='notifications',
                        on_click=self.get_articles,
                    ),
                    Setting(
                        name='texts',
                        icon='notifications',
                        on_click=self.get_texts,
                    ),
                    Setting(
                        name='accounts',
                        icon='notifications',
                        on_click=self.get_accounts,
                    ),
                    Setting(
                        name='products',
                        icon='notifications',
                        on_click=self.get_products,
                    ),
                    Setting(
                        name='languages',
                        icon='notifications',
                        on_click=self.get_languages,
                    ),
                    Setting(
                        name='currencies',
                        icon='notifications',
                        on_click=self.get_currencies,
                    ),
                    Setting(
                        name='timezones',
                        icon='notifications',
                        on_click=self.get_timezones,
                    ),
                ],
            ),
        ]
        sections_controls = []
        for section in sections:
            sections_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Text(
                                        value=await self.client.session.gtv(section.name),
                                        font_family=Fonts.SEMIBOLD,
                                        size=30,
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='Menu'),
                                            font_family=Fonts.REGULAR,
                                        ),
                                        on_click=self.go_back,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Column(
                                controls=[
                                    Container(
                                        content=Row(
                                            controls=[
                                                Image(
                                                    src=get_svg(path=f'assets/icons/{setting.icon}.svg'),
                                                    width=36,
                                                ),
                                                Text(
                                                    value=await self.client.session.gtv(setting.name),
                                                    font_family=Fonts.REGULAR,
                                                    size=20,
                                                ),
                                            ],
                                            spacing=12,
                                        ),
                                        ink=True,
                                        on_click=setting.on_click,
                                    )
                                    for setting in section.settings
                                ],
                            ),
                        ],
                    ),
                    padding=10,
                ),
            ),
        self.controls = [
            await self.get_header(),
            *sections_controls,
        ]

    async def coming_soon(self):
        pass

    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def get_articles(self, _):
        await self.client.change_view(view=ArticleListView())

    async def get_texts(self, _):
        await self.client.change_view(view=TextListView())

    async def get_accounts(self, _):
        await self.client.change_view(view=AccountListView())

    async def get_products(self, _):
        await self.client.change_view(view=ProductListView())

    async def get_languages(self, _):
        await self.client.change_view(view=LanguageListView())

    async def get_currencies(self, _):
        await self.client.change_view(view=CurrencyListView())

    async def get_timezones(self, _):
        await self.client.change_view(view=TimezoneListView())
