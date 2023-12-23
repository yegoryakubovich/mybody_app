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
from app.views.admin.currencies import CreateCurrencyView, CurrencyView
from app.views.admin.languages import LanguageView
from app.views.admin.languages.create import CreateLanguageView
from app.views.admin.timezones import CreateTimezoneView, TimezoneView


class TimezoneListView(View):
    route = '/admin'
    timezones: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.timezone.get_list()
        self.timezones = response.timezones
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='timezones'),
                            on_create_click=self.create_timezone,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=timezone['id_str'],
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Text(
                                            value=await self.client.session.gtv(
                                                key=f'deviation:') + str(timezone['deviation']),
                                            size=10,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.timezone_view, timezone['id_str']),
                            ),
                            margin=0,
                        )
                        for timezone in self.timezones
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_timezone(self, _):
        await self.client.change_view(view=CreateTimezoneView())

    async def timezone_view(self,timezone_id_str, _):
        await self.client.change_view(view=TimezoneView(timezone_id_str=timezone_id_str))
