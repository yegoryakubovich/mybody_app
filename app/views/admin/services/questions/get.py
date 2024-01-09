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


from flet_core import Row, ScrollMode, Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AdminBaseView, Section


class ServiceQuestionView(AdminBaseView):
    route = '/admin/service/get'
    service: dict
    tf_title: TextField

    def __init__(self, question):
        super().__init__()
        self.question = question

    async def build(self):
        print(self.question)
        self.tf_title = TextField(
            label=await self.client.session.gtv(key='title'),
            value=self.question['title'],
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=self.question['title'],
            main_section_controls=[
                self.tf_title,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_question,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_question,
                        ),
                    ],
                )
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='questions'),
                    controls=[
                        TextField(
                            label=question['type'],
                            value=question['name'],
                        )
                        if question['type'] != 'dropdown'
                        else Column(
                            controls=[
                                TextField(
                                    label=await self.client.session.gtv(key='answer'),
                                    value=value,
                                )
                                for value in question['values']
                            ]
                        )
                        for question in self.question['questions']
                    ]
                )
            ],
        )

    async def update_question(self, _):
        pass

    async def delete_question(self, _):
        pass
