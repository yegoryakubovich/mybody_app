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


from flet_core import Container, Column, ScrollMode

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View


class ServiceView(View):
    route = '/admin'
    service:  dict
    tf_name: TextField
    tf_questions: TextField

    def __init__(self, service_id_str):
        super().__init__()
        self.service_id_str = service_id_str

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.service.get(
            id_str=self.service_id_str
        )
        self.service = response.service
        await self.set_type(loading=False)

        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
            value=self.service['name'],
        )
        self.tf_questions = TextField(
            label=await self.client.session.gtv(key='value_default'),
            value=self.service['questions'],
        )
        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=await self.client.session.gtv(key=self.service['name_text']),
                         create_button=False,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete_service'),
                            ),
                            on_click=self.delete_service,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def delete_service(self, _):
        await self.client.session.api.service.delete(
            id_str=self.service_id_str
        )
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()
