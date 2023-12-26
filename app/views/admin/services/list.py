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
from app.views.admin.services.get import ServiceView
from app.views.admin.services.create import CreateServiceView


class ServiceListView(View):
    route = '/admin'
    services: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.service.get_list()
        self.services = response.services
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='services'),
                            on_create_click=self.create_service,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=service['name_text'].upper(),
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.service_view, service['id_str']),
                            ),
                            margin=0,
                        )
                        for service in self.services
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_service(self, _):
        await self.client.change_view(view=CreateServiceView())

    async def service_view(self, service_id_str, _):
        await self.client.change_view(view=ServiceView(service_id_str=service_id_str))
