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

from flet_core import Container, Column, PopupMenuButton, PopupMenuItem, ScrollMode, Row, IconButton, icons, \
    MainAxisAlignment

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AdminView
from app.utils import Fonts


class CreateServiceView(AdminView):
    route = '/admin'
    questions: list[dict] = []
    textfields: list[tuple] = []
    question_type: str = 'str'
    dropdown_values: list[list[TextField]] = []
    tf_name: TextField
    tf_id_str: TextField

    async def build(self):
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='key'),
        )
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_service_create_view_title'),
                        main_section_controls=[
                            self.tf_id_str,
                            self.tf_name,
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='create'),
                                ),
                                on_click=self.create,
                            ),
                            Row(
                                controls=[
                                    Text(
                                        value=await self.client.session.gtv(key='questions'),
                                        size=30,
                                        font_family=Fonts.BOLD,
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='save'),
                                        ),
                                        on_click=self.save_questions,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ] + [tf for _, tf in self.textfields] + (
                            [Row(
                                controls=[
                                    dropdown,
                                    IconButton(
                                        icon=icons.ADD,
                                        on_click=self.add_dropdown_field,
                                    ),
                                    ] + (
                                        [IconButton(
                                            icon=icons.DELETE,
                                            on_click=functools.partial(self.remove_dropdown_field, dropdown),
                                            )] if len(self.dropdown_values[-1]) > 1 else []
                                        ),
                            ) for dropdown in self.dropdown_values[-1]] if self.question_type == 'dropdown' else []
                        ) + [
                            Row(
                                controls=[
                                    PopupMenuButton(
                                        items=[
                                            PopupMenuItem(text='str', on_click=functools.partial(
                                                self.set_question_type, 'str')),
                                            PopupMenuItem(text='int', on_click=functools.partial(
                                                self.set_question_type, 'int')),
                                            PopupMenuItem(text='dropdown', on_click=functools.partial(
                                                self.set_question_type, 'dropdown')),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def set_question_type(self, question_type, _):
        self.question_type = question_type
        if question_type == 'dropdown':
            new_dropdown = TextField(
                label=await self.client.session.gtv(key='dropdown_list_values'),
                height=50,
                width=300,
            )
            self.dropdown_values.append([new_dropdown])
        else:
            self.dropdown_values.append([])
        tf = TextField(label=f'question for {self.question_type}')
        self.textfields.append((self.question_type, tf))
        await self.build()
        await self.update_async()

    async def add_dropdown_field(self, _):
        new_dropdown = TextField(
            label=await self.client.session.gtv(key='dropdown_list_values'),
            height=50,
            width=300,
        )
        self.dropdown_values[-1].append(new_dropdown)
        await self.build()
        await self.update_async()

    async def remove_dropdown_field(self, dropdown, _):
        self.dropdown_values[-1].remove(dropdown)
        await self.build()
        await self.update_async()

    async def save_questions(self, _):
        for i, (question_type, tf) in enumerate(self.textfields):
            question = {"name": tf.value, "type": question_type}
            if question_type == 'dropdown':
                question["values"] = [dv.value for dv in self.dropdown_values[i]]
            self.questions.append(question)
        self.textfields = []
        await self.build()
        await self.update_async()

    async def create(self, _):
        for i, (question_type, tf) in enumerate(self.textfields):
            question = {"name": tf.value, "type": question_type}
            if question_type == 'dropdown':
                question["values"] = [dv.value for dv in self.dropdown_values[i]]
            self.questions.append(question)
        self.textfields = []
        await self.build()
        await self.update_async()
