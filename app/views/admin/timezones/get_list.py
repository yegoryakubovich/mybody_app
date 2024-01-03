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

from flet_core import Container, Text, Column, ScrollMode

from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.timezones.create import CreateTimezoneView
from app.views.admin.timezones.get import TimezoneView


class TimezoneListView(AdminBaseView):
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
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_timezone_get_list_view_title'),
                        on_create_click=self.create_timezone,
                        main_section_controls=[
                            Card(
                                controls=[
                                    Text(
                                        value=timezone['id_str'],
                                        size=18,
                                        font_family=Fonts.SEMIBOLD,
                                    ),
                                ],
                                on_click=functools.partial(self.timezone_view, timezone['id_str']),
                            )
                            for timezone in self.timezones
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def create_timezone(self, _):
        await self.client.change_view(view=CreateTimezoneView())

    async def timezone_view(self, timezone_id_str, _):
        await self.client.change_view(view=TimezoneView(timezone_id_str=timezone_id_str))
