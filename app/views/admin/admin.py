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

from flet_core import Container, Column, margin, Row, Image
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import View
from app.utils import Fonts


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

    async def clear_cs(self, _):
        await self.client.session.set_cs(key='language', value=None)
        await self.client.session.set_cs(key='token', value=None)

    async def build(self):
        sections = [
            Section(
                name='admin_panel',
                settings=[
                    Setting(
                        name='accounts_forms',
                        icon='doc',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='articles',
                        icon='plan',
                        on_click=self.coming_soon,
                    ),
                    Setting(
                        name='texts',
                        icon='notifications',
                        on_click=self.coming_soon,
                    ),
                ],
            ),
        ]
        sections_controls = []
        for section in sections:
            sections_controls.append(Container(
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
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='Menu'),
                                size=16,
                                font_family=Fonts.MEDIUM,
                            ),
                            on_click=self.go_home,
                        ),
                    ],
                ),
            ))
        self.controls = [
            await self.get_header(),
            *sections_controls,
        ]

    async def coming_soon(self):
        pass

    async def go_home(self, _):
        from app.views.main import MainView
        await self.client.change_view(view=MainView())
