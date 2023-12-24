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


from flet_core import Container, Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View


class CreateServiceView(View):
    route = '/admin'
    tf_name: TextField
    tf_id_str: TextField
    tf_questions: TextField

    async def build(self):
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='id_str'),
        )
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.tf_questions = TextField(
            label=await self.client.session.gtv(key='questions'),
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='create_service'),
                            create_button=False,
                        ),
                        self.tf_id_str,
                        self.tf_name,
                        self.tf_questions,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create'),
                                size=16,
                            ),
                            on_click=self.create_service,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_service(self, _):
        if len(self.tf_id_str.value) < 2 or len(self.tf_id_str.value) > 32:
            self.tf_id_str.error_text = await self.client.session.gtv(key='id_str_min_max_letter')
        elif len(self.tf_name.value) < 1 or len(self.tf_name.value) > 1024:
            self.tf_name.error_text = await self.client.session.gtv(key='name_min_max_letter')
        elif len(self.tf_questions.value) < 2 or len(self.tf_questions.value) > 8192:
            self.tf_questions.error_text = await self.client.session.gtv(key='questions_min_max_letter')
        else:
            response = await self.client.session.api.service.create(
                id_str=self.tf_id_str.value,
                name=self.tf_name.value,
                questions=self.tf_questions.value
            )
            print(response)
            await self.client.change_view(go_back=True)
            await self.client.page.views[-1].restart()
