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

from flet_core import ScrollMode
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import ClientBaseView
from app.controls.navigation.pagination import PaginationWidget
from app.utils import Fonts


class ServiceCreateView(ClientBaseView):
    service = dict[dict]
    page_account: int = 1
    total_pages: int = 1
    answers: dict = {}
    dd_answers: List[Dropdown] = []
    tf_answers: List[TextField] = []

    def __init__(self, service_id_str):
        super().__init__()
        self.service_id_str = service_id_str

    async def build(self):
        await self.set_type(loading=True)
        self.service = await self.client.session.api.client.service.get(
            id_=self.service_id_str,
        )
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO

        titles = json.loads(self.service['questions'])
        self.total_pages = len(titles)

        title = titles[self.page_account - 1]

        controls = [
            Text(
                value=await self.client.session.gtv(key=title['title_text']),
                size=20,
                font_family=Fonts.BOLD,
            ),
        ]
        for question in title['questions']:
            controls.append(
                Text(
                    value=await self.client.session.gtv(key=question['name_text']),
                    size=15,
                    font_family=Fonts.REGULAR,
                ),
            )
            if question['type'] == 'dropdown':
                value_options = [
                    Option(
                        text=value,
                        key=value,
                    ) for value in question.get('values', [])
                ]
                dd_answer = Dropdown(
                    label=await self.client.session.gtv(key='answer'),
                    on_change=self.save_answer(question['key'], question['type']),
                    value=value_options[0],
                    options=value_options,
                )
                self.dd_answers.append(dd_answer)
                controls.append(dd_answer)
            else:
                tf_answer = TextField(
                    label=await self.client.session.gtv(key='answer'),
                    on_change=self.save_answer(question['key'], question['type']),
                )
                self.tf_answers.append(tf_answer)
                controls.append(tf_answer)

        if self.page_account == self.total_pages:
            controls.append(
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='send_form'),
                    ),
                    on_click=self.send_form
                ),
            )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.service['name_text']),
            main_section_controls=controls + [
                PaginationWidget(
                    current_page=self.page_account,
                    total_pages=self.total_pages,
                    on_back=self.previous_page,
                    on_next=self.next_page,
                ),
            ]
        )

    def save_current_answers(self):
        for dd_answer in self.dd_answers:
            dd_answer.on_change(dd_answer.value)
        for tf_answer in self.tf_answers:
            tf_answer.on_change(tf_answer.value)

    def save_answer(self, key, q_type):
        def inner(value):
            if q_type == 'int':
                self.answers[key] = int(value)
            else:
                self.answers[key] = value
        return inner

    async def send_form(self, _):
        self.save_current_answers()
        answers = json.dumps(self.answers, ensure_ascii=False)
        await self.client.session.api.client.account.create_service(
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
            self.page_account -= 1
            await self.build()
            await self.update_async()
