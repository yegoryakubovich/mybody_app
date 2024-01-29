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

from flet_core import Row, ScrollMode, PopupMenuButton, PopupMenuItem, IconButton, icons

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AdminBaseView, Section


class ServiceQuestionView(AdminBaseView):
    route = '/admin/service/get'
    service: dict
    questions: list[dict] = []
    textfields: list[tuple] = []
    question_type: str = 'str'
    dropdown_values: list[list[TextField]] = []
    tf_title: TextField

    def __init__(self, question):
        super().__init__()
        self.question = question

    async def build(self):
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
                        Row(
                            controls=[
                                TextField(
                                    label=question['type'],
                                    value=question['name'],
                                ),
                                IconButton(
                                    icon=icons.DELETE,
                                    on_click=functools.partial(self.remove_textfield, question)
                                ),
                            ],
                        )
                        for question in self.question['questions']
                         ] + [
                             Row(
                                 controls=[
                                     tf,
                                     IconButton(
                                         icon=icons.DELETE,
                                         on_click=functools.partial(self.remove_textfield, tf)
                                     ),
                                 ],
                             )
                             for _, tf in self.textfields
                         ] + (
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
                             ) for dropdown in self.dropdown_values[-1]]
                             if self.dropdown_values and self.question_type == 'dropdown' else []
                         ) + [
                             Row(
                                 controls=[
                                     PopupMenuButton(
                                         items=[
                                             PopupMenuItem(text='title', on_click=functools.partial(
                                                 self.set_question_type, 'title')),
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
                )
            ],
        )

    async def set_question_type(self, question_type, _):
        self.question_type = question_type
        if question_type == 'dropdown':
            new_dropdown = TextField(
                label=await self.client.session.gtv(key='admin_service_create_view_dropdown'),
                height=50,
                width=300,
            )
            self.dropdown_values.append([new_dropdown])
        elif question_type != 'dropdown':
            self.dropdown_values.append([])
        tf = TextField(
            label=await self.client.session.gtv(key='question'),
            expand=True,
        )
        self.textfields.append((self.question_type, tf))
        await self.build()
        await self.update_async()

    async def save_questions(self, _):
        await self.update_async()

    async def add_dropdown_field(self, _):
        new_dropdown = TextField(
            label=await self.client.session.gtv(key='admin_service_create_view_dropdown'),
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

    async def remove_textfield(self, tf, _):
        for i, (question_type, existing_tf) in enumerate(self.textfields):
            if existing_tf == tf:
                del self.textfields[i]
                del self.dropdown_values[i]
                await self.build()
                await self.update_async()
                break

    async def update_question(self, _):
        pass

    async def delete_question(self, _):
        pass
