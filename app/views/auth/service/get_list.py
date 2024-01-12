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


import functools

from flet_core import ScrollMode

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import ClientBaseView
from app.utils import Fonts
from app.views.auth.service.get import ServiceView


class ServiceListView(ClientBaseView):
    services: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        self.services = await self.client.session.api.client.service.get_list()
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='client_service_get_list_view_title'),
            main_section_controls=[
                Text(
                    value=await self.client.session.gtv(key='Выберите желаемый пакет услуг'),
                    size=18,
                    font_family=Fonts.SEMIBOLD,
                ),
                *[Card(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key=service['name_text']),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=functools.partial(self.service_view, service['id_str']),
                )
                    for service in self.services]
            ]
        )

    async def service_view(self, service_id_str, _):
        await self.client.change_view(view=ServiceView(service_id_str=service_id_str))
