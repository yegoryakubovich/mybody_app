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


from functools import partial
import json

from flet_core import PopupMenuButton, PopupMenuItem, ScrollMode, Row, IconButton, icons, \
    MainAxisAlignment
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AdminBaseView
from app.utils import Fonts, Error


class ServiceCreateView(AdminBaseView):
    route = '/admin/service/get'
    questions: list[dict] = []
    text_fields: list[tuple] = []
    question_type: str = 'str'
    dropdown_values: list[list[TextField]] = []
    tf_name: TextField
    tf_id_str: TextField
    tf_title: TextField

    async def build(self):
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='key'),
        )
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.tf_title = TextField(
            label=await self.client.session.gtv(key='title'),
        )
        rows = []
        for textfield in self.text_fields:
            if textfield[0] == 'title':
                question_type, tf = textfield
                row = Row(
                    controls=[
                        tf,
                        IconButton(
                            icon=icons.DELETE,
                            on_click=partial(self.remove_textfield, tf)
                        ),
                    ]
                )
            else:
                question_type, tf, key_tf = textfield
                row = Row(
                    controls=[
                        tf,
                        key_tf,
                        IconButton(
                            icon=icons.DELETE,
                            on_click=partial(self.remove_textfield, tf)
                        ),
                    ]
                )
            rows.append(row)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_service_create_view_title'),
            main_section_controls=[
                self.tf_id_str,
                self.tf_name,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                    ),
                    on_click=self.create_service,
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
            ] + rows + (
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
                                on_click=partial(self.remove_dropdown_field, dropdown),
                                )] if len(self.dropdown_values[-1]) > 1 else []
                            ),
                ) for dropdown in self.dropdown_values[-1]]
                if self.dropdown_values and self.question_type == 'dropdown' else []
            ) + [
                Row(
                    controls=[
                        PopupMenuButton(
                            items=[
                                PopupMenuItem(text='title', on_click=partial(
                                    self.set_question_type, 'title')),
                                PopupMenuItem(text='str', on_click=partial(
                                    self.set_question_type, 'str')),
                                PopupMenuItem(text='int', on_click=partial(
                                    self.set_question_type, 'int')),
                                PopupMenuItem(text='dropdown', on_click=partial(
                                    self.set_question_type, 'dropdown')),
                            ],
                        ),
                    ],
                ),
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
        key_tf = TextField(
            label=await self.client.session.gtv(key='key'),
            expand=True,
        )
        if question_type == 'title':
            self.tf_title = TextField(
                label=await self.client.session.gtv(key='title'),
                expand=True,
            )
            self.text_fields.append(('title', self.tf_title))
        else:
            self.text_fields.append((self.question_type, tf, key_tf))
        await self.build()
        await self.update_async()

    async def save_questions(self, _):
        questions_list = []
        title_value = ''
        for i, textfield in enumerate(self.text_fields):
            if textfield[0] == 'title':
                # Если это не первый title, сохраняем предыдущий набор вопросов
                if title_value:
                    entry = {'title': title_value, 'questions': questions_list}
                    self.questions.append(entry)
                    questions_list = []
                question_type, tf = textfield
                title_value = tf.value
            else:
                question_type, tf, key_tf = textfield
                question = {'name': tf.value, 'key': key_tf.value, 'type': question_type}
                if question_type == 'dropdown':
                    question['values'] = [dv.value for dv in self.dropdown_values[i]]
                questions_list.append(question)

        if title_value and questions_list:
            entry = {'title': title_value, 'questions': questions_list}
            self.questions.append(entry)
        self.text_fields = []
        self.dropdown_values = []

        await self.build()
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
        for i, textfield in enumerate(self.text_fields):
            if textfield[1] == tf:
                del self.text_fields[i]
                if textfield[0] != 'title':
                    del self.dropdown_values[i]
                await self.build()
                await self.update_async()

    async def create_service(self, _):
        from app.views.admin.services import ServiceView
        fields = [(self.tf_name, 1, 1024), (self.tf_id_str, 2, 64)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return

        questions = json.dumps(self.questions, ensure_ascii=False)
        try:
            service_id_str = await self.client.session.api.admin.services.create(
                id_str=self.tf_id_str.value,
                name=self.tf_name.value,
                questions=questions,
            )
            await self.client.change_view(view=ServiceView(service_id_str=service_id_str), delete_current=True)
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
