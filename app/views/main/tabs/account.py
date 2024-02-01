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


from functools import partial
from typing import Any

from flet_core import Container, alignment, padding, Column, CrossAxisAlignment, CircleAvatar, Image, colors

from app.controls.button import ListItemButton
from app.controls.information import Text
from app.utils import Fonts, Icons
from app.views.admin.admin import AdminView
from app.views.main.tabs.base import BaseTab
from config import settings


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

    def __init__(self, name: str, settings_: list[Setting]):
        self.name = name
        self.settings = settings_


class AccountTab(BaseTab):
    go_admin_counter: int

    async def go_admin(self, _):
        self.go_admin_counter += 1
        if self.go_admin_counter < 5:
            return
        self.go_admin_counter = 0
        if 'admin' not in self.client.session.account.permissions:
            pass  # FIXME
        await self.client.change_view(view=AdminView())

    async def update_language(self, _):
        from app.views.auth.language import LanguageView
        await self.client.change_view(view=LanguageView(), delete_current=True)

    async def logout(self, _):
        await self.client.session.set_cs(key='token', value=None)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView(), delete_current=True)

    async def build(self):
        # Bottom Sheets
        on_click_coming_soon = partial(
            self.client.session.bs_info.open_,
            icon=Icons.CHILL,
            title=await self.client.session.gtv(key='coming_soon'),
            description=await self.client.session.gtv(key='coming_soon_description'),
        )
        on_click_logout = partial(
            self.client.session.bs_info.open_,
            icon=Icons.LOGOUT,
            title=await self.client.session.gtv(key='logout_title'),
            description=await self.client.session.gtv(key='logout_description'),
            button_title=await self.client.session.gtv(key='confirm'),
            button_on_click=self.logout,
        )

        # Go Admin
        self.go_admin_counter = 0

        firstname = self.client.session.account.firstname
        lastname = self.client.session.account.lastname
        username = self.client.session.account.username

        sections = [
            Section(
                name='my_account',
                settings_=[
                    Setting(
                        name='notifications',
                        icon=Icons.NOTIFICATIONS,
                        on_click=on_click_coming_soon,
                    ),
                    Setting(
                        name='security',
                        icon=Icons.SECURITY,
                        on_click=on_click_coming_soon,
                    ),
                    Setting(
                        name='language',
                        icon=Icons.LANGUAGE,
                        on_click=self.update_language,
                    ),
                    Setting(
                        name='logout',
                        icon=Icons.LOGOUT,
                        on_click=on_click_logout,
                    ),
                ],
            ),
            Section(
                name='info',
                settings_=[
                    Setting(
                        name='articles',
                        icon=Icons.ARTICLES,
                        on_click=on_click_coming_soon,
                    ),
                ],
            ),
            Section(
                name='help',
                settings_=[
                    Setting(
                        name='about',
                        icon=Icons.ABOUT,
                        on_click=on_click_coming_soon,
                    ),
                    Setting(
                        name='support',
                        icon=Icons.SUPPORT,
                        on_click=on_click_coming_soon,
                    ),
                    Setting(
                        name='faq',
                        icon=Icons.FAQ,
                        on_click=on_click_coming_soon,
                    ),
                    Setting(
                        name='privacy_policy',
                        icon=Icons.PRIVACY_POLICY,
                        on_click=on_click_coming_soon,
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
                                size=26,
                            ),
                        ),
                        Column(
                            controls=[
                                ListItemButton(
                                    icon=setting.icon,
                                    name=await self.client.session.gtv(key=setting.name),
                                    on_click=setting.on_click,
                                )
                                for setting in section.settings
                            ],
                            spacing=4,
                        ),
                    ],
                ),
                padding=padding.only(top=12),
                margin=padding.symmetric(horizontal=16),
            ) for section in sections
        ]

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        CircleAvatar(
                            content=Image(
                                src=Icons.ACCOUNT,
                                color=colors.TERTIARY,  # FIXME
                            ),
                            bgcolor=colors.TERTIARY_CONTAINER,
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
                padding=padding.only(top=24),
                alignment=alignment.center,
            ),
        ] + sections_controls + [
            Container(
                content=Text(
                    value=f'{await self.client.session.gtv(key="version")} {settings.version}',
                    font_family=Fonts.REGULAR,
                    size=16,
                ),
                alignment=alignment.center,
                on_click=self.go_admin,
                padding=padding.symmetric(vertical=4),
                ink=True,
            ),
        ]

    async def get_services(self, _):
        await self.client.change_view(view=ServiceListView())
