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


import json
from typing import List

from flet_core import Column, ScrollMode
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import ClientBaseView
from app.controls.navigation.pagination import PaginationWidget
from app.utils import Fonts


class ServiceCreateView(ClientBaseView):
    service = dict
    page_account: int = 1
    total_pages: int = 1
    tf_id_str: str
    dd_answers: List[Dropdown] = []
    tf_answers: List[TextField] = []

    def __init__(self, service_id_str):
        super().__init__()
        self.service_id_str = service_id_str
        self.answers = {}
        self.page_answers = {}
        self.order = []

    async def build(self):
        await self.set_type(loading=True)
        self.service = await self.client.session.api.client.service.get(
            id_=self.service_id_str,
        )
        print(self.service)
        await self.set_type(loading=False)

        questions_data = json.loads(self.service['questions'])
        self.total_pages = len(questions_data)

        current_title = questions_data[self.page_account - 1]['title']
        current_questions = questions_data[self.page_account - 1]['questions']

        main_section_controls = [
            Text(
                value=current_title,
                size=18,
                font_family=Fonts.SEMIBOLD,
            ),
        ]

        for question in current_questions:
            question_name = question['name']
            question_type = question['type']

            if question_type == 'dropdown':
                value_options = [
                    Option(
                        text=value,
                        key=value,
                    ) for value in question.get('values', [])
                ]
                dd_answer = Dropdown(
                    label=await self.client.session.gtv(key='answer'),
                    options=value_options,
                )
                self.dd_answers.append(dd_answer)
                row_controls = [
                    Text(
                        value=question_name,
                        size=18,
                        font_family=Fonts.SEMIBOLD,
                    ),
                    dd_answer,
                ]
            else:
                tf_answer = TextField(
                    label=await self.client.session.gtv(key='answer'),
                )
                self.tf_answers.append(tf_answer)
                row_controls = [
                    Text(
                        value=question_name,
                        size=18,
                        font_family=Fonts.SEMIBOLD,
                    ),
                    tf_answer,
                ]

            main_section_controls.append(Column(controls=row_controls))

        if self.page_account == self.total_pages:
            main_section_controls.append(
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='send_form'),
                    ),
                    on_click=self.send_form,
                )
            )

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.service['name_text']),
            main_section_controls=main_section_controls + [
                PaginationWidget(
                    current_page=self.page_account,
                    total_pages=self.total_pages,
                    on_back=self.previous_page,
                    on_next=self.next_page,
                ),
            ]
        )

    async def send_form(self, _):
        self.save_current_answers()
        answers = self.page_answers[self.page_account]
        new_answers = [answer for answer in answers if isinstance(answer, str)]
        answers = json.dumps(new_answers, ensure_ascii=False)
        await self.client.session.api.client.service.create(
            id_str=self.tf_id_str,
            service=self.service_id_str,
            answers=answers,
        )

    async def next_page(self, _):
        if self.page_account < self.total_pages:
            self.save_current_answers()
            self.page_account += 1
            await self.build()
            await self.update_async()

    async def previous_page(self, _):
        if self.page_account > 1:
            self.save_current_answers()
            self.page_account -= 1
            await self.build()
            await self.update_async()

    def save_current_answers(self):
        new_answers = [dd.value for dd in self.dd_answers] + [tf.value for tf in self.tf_answers]
        if self.page_account not in self.page_answers or new_answers != self.page_answers[self.page_account]:
            self.page_answers[self.page_account] = new_answers
