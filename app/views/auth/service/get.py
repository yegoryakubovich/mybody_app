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


from flet_core import Row, ScrollMode

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import ClientBaseView
from app.views.auth.service import ServiceCreateView


class ServiceView(ClientBaseView):
    route = '/admin/articles/get'
    service = dict

    def __init__(self, service_id_str):
        super().__init__()
        self.service_id_str = service_id_str

    async def build(self):
        await self.set_type(loading=True)
        self.service = await self.client.session.api.client.service.get(
            id_=self.service_id_str
        )
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            back_with_restart=True,
            title=await self.client.session.gtv(key=self.service['name_text']),
            main_section_controls=[
                Text(
                    value=await self.client.session.gtv(key='описание сервиса и предложения пройти анкету'),
                ),
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='go_questionnaire'),
                            ),
                            on_click=self.create_service,
                        ),
                    ],
                )
            ],
        )

    async def create_service(self, _):
        await self.client.change_view(view=ServiceCreateView(service_id_str=self.service_id_str))
