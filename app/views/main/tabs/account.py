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

from flet_core import Container, alignment, padding, Column, CrossAxisAlignment, CircleAvatar, \
    Image, BottomSheet, margin, TextAlign, Row
from flet_manager.utils import get_svg

from app.controls.information import Text
from app.utils import Fonts
from app.views.admin import AdminView
from app.views.main.tabs.base import BaseTab
from config import VERSION


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


class AccountTab(BaseTab):
    bs_comming_soon: BottomSheet
    go_admin_couner: int

    async def go_admin(self, _):
        self.go_admin_couner += 1
        if self.go_admin_couner < 5:
            return
        self.go_admin_couner = 0
        await self.client.change_view(view=AdminView())

    async def coming_soon(self, _):
        self.bs_comming_soon.open = True
        await self.bs_comming_soon.update_async()

    async def logout(self, _):
        await self.view.set_type(loading=True)
        await self.client.session.set_cs(key='token', value=None)

        # Change view
        view = await self.client.session.init()
        await self.view.set_type(loading=False)
        await self.client.change_view(view=view)

    async def bs_init(self):
        self.bs_comming_soon = BottomSheet(
            Container(
                Column(
                    controls=[
                        Container(
                            content=Image(
                                src=get_svg(
                                    path='assets/icons/chill.svg',
                                ),
                                color='#1d1d1d',  # FIXME
                            ),
                            margin=margin.only(bottom=16),
                        ),
                        Text(
                            value=await self.client.session.gtv(key='coming_soon'),
                            font_family=Fonts.SEMIBOLD,
                            size=28,
                        ),
                        Text(
                            value='This feature is temporarily unavailable. We are already working on it!',  # FIXME
                            font_family=Fonts.REGULAR,
                            size=16,
                            text_align=TextAlign.CENTER,
                        ),
                    ],
                    spacing=4,
                    tight=True,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                padding=padding.symmetric(vertical=24, horizontal=128),
            ),
            open=False,
        )
        self.view.client.page.overlay.append(self.bs_comming_soon)

    async def build(self):
        await self.bs_init()

        # Go Admin
        self.go_admin_couner = 0

        firstname = self.client.session.account.firstname
        lastname = self.client.session.account.lastname
        username = self.client.session.account.username

        sections = [
            Section(
                name='my_account',
                settings=[
                    Setting(
                        name='notifications',
                        icon='notifications',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='security',
                        icon='security',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='language',
                        icon='language',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='logout',
                        icon='logout',
                        on_click=self.logout,
                    ),
                ],
            ),
            Section(
                name='info',
                settings=[
                    Setting(
                        name='articles',
                        icon='notifications',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='policies',
                        icon='security',
                        on_click=self.coming_soon,
                    ),
                ],
            ),
        ]
        sections_controls = [
            Container(
                content=Column(
                    controls=[
                        Container(
                            content=Text(
                                value=await self.client.session.gtv(section.name),
                                font_family=Fonts.SEMIBOLD,
                                size=30,
                            ),
                            margin=margin.symmetric(horizontal=16),
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
                                    margin=margin.symmetric(horizontal=16),
                                    ink=True,
                                    on_click=setting.on_click,
                                )
                                for setting in section.settings
                            ],
                            spacing=12,
                        ),
                    ],
                ),
                bgcolor='#FFFFFF',  # FIXME
                padding=padding.only(top=12, bottom=24),
                margin=margin.only(top=12),
            ) for section in sections
        ]

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        CircleAvatar(
                            content=Image(
                                src=get_svg(
                                    path='assets/icons/account.svg',
                                ),
                                color='#1d1d1d',  # FIXME
                            ),
                            bgcolor='#E4E4E4',
                            radius=38,
                        ),
                        Text(
                            value=f'{firstname} {lastname}',
                            font_family=Fonts.SEMIBOLD,
                            size=30,
                        ),
                        Text(
                            value=f'@{username}',
                            font_family=Fonts.SEMIBOLD,
                            size=12,
                        ),
                    ],
                    spacing=0,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                bgcolor='#FFFFFF',  # FIXME
                padding=padding.symmetric(vertical=24),
                alignment=alignment.center,
            ),
        ] + sections_controls + [
            Container(
                content=Text(
                    value=await self.client.session.gtv(key='version: ') + VERSION,  # FIXME
                    font_family=Fonts.REGULAR,
                    size=16,
                ),
                alignment=alignment.center,
                on_click=self.go_admin,
                padding=padding.symmetric(vertical=4),
            ),
        ]
