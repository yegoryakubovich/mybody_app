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
from app.controls.input import TextField
from app.controls.layout import AdminBaseView
from app.utils import Error


class ServiceView(AdminBaseView):
    route = '/admin/service/get'
    service: dict
    tf_name: TextField
    tf_questions: TextField

    def __init__(self, service_id_str):
        super().__init__()
        self.service_id_str = service_id_str

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.service.get(
            id_=self.service_id_str
        )
        self.service = response.service
        await self.set_type(loading=False)

        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
            value=self.service['name_text'],
        )
        self.tf_questions = TextField(
            label=await self.client.session.gtv(key='questions'),
            value=self.service['questions'],
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.service['name_text']),
            main_section_controls=[
                self.tf_name,
                self.tf_questions,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.delete_service,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_service,
                        ),
                    ],
                )
            ],
         )

    async def delete_service(self, _):
        await self.client.session.api.admin.service.delete(
            id_str=self.service_id_str,
        )
        await self.client.change_view(go_back=True)

    async def update_service(self, _):
        fields = [(self.tf_questions, 2, 8192), (self.tf_name, 1, 1024)]
        for field, min_len, max_len, error_key in fields:
            if not await Error.check_field(self, field, min_len, max_len):
                return
        await self.client.session.api.admin.country.update(
            id_str=self.service_id_str,
            name=self.tf_name.value,
            questions=self.tf_questions.value,
        )
        await self.client.change_view(go_back=True)
