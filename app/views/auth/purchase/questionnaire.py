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

from flet_core import InputFilter
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AuthView
from app.controls.navigation.pagination import PaginationWidget
from app.utils import Fonts, Error
from app.views.auth.purchase.about import PurchaseFirstView


class QuestionnaireView(AuthView):
    services = list[dict]
    service = list[dict]
    page_account: int = 1
    total_pages: int = 1
    answers: dict = {}
    dd_answers: List[Dropdown] = []
    tf_answers: List[TextField] = []
    service_id_str: str

    def __init__(self, gender):
        super().__init__()
        self.gender = gender

    async def build(self):
        await self.set_type(loading=True)
        self.services = await self.client.session.api.client.services.get_list()
        self.service = await self.client.session.api.client.services.get(
            id_=self.services[0]['id_str'],
        )
        await self.set_type(loading=False)

        titles = json.loads(self.service.questions)
        if self.gender == 'men':
            titles = [title for title in titles if title['title_text'] != 'peculiarities']
        self.total_pages = len(titles)

        title = titles[self.page_account - 1]
        controls = []
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
                        text=await self.client.session.gtv(key=value),
                        key=value,
                    ) for value in question['values_texts']
                ]
                initial_value = self.answers.get(question['key'], value_options[0].key)
                dd_answer = Dropdown(
                    label=await self.client.session.gtv(key='answer'),
                    value=initial_value,
                    options=value_options,
                    key=question['key'],
                )
                self.dd_answers.append(dd_answer)
                controls.append(dd_answer)
            else:
                initial_value = self.answers.get(question['key'], '')
                tf_answer = TextField(
                    label=await self.client.session.gtv(key='answer'),
                    key_question=f"{question['key']}_{question['type']}",
                    value=initial_value,
                    input_filter=InputFilter(
                        allow=True, regex_string=r'[0-9]', replacement_string=''
                    ) if question['type'] == 'int' else None,
                )
                if tf_answer.value is not None:
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
            title=await self.client.session.gtv(key=title['title_text']),
            controls=controls + [
                PaginationWidget(
                    current_page=self.page_account,
                    total_pages=self.total_pages,
                    on_back=self.previous_page,
                    on_next=self.next_page,
                ),
            ]
        )

    async def check_errors(self, field_list, min_len, max_len):
        for field in field_list:
            key_question_parts = field.key_question.split('_')
            key_question, type_ = key_question_parts
            check_int = type_ == 'int'
            if not await Error.check_field(self, field, check_int=check_int, min_len=min_len, max_len=max_len):
                return False
        return True

    async def send_form(self, _):
        if not await self.check_errors(self.tf_answers, 1, 1024):
            return

        answers = {
            tf.key_question.split('_')[0]: int(tf.value) if tf.key_question.split('_')[1] == 'int' else tf.value
            for tf in self.tf_answers
        }
        answers.update({dd.key: dd.value for dd in self.dd_answers})
        answers_json = json.dumps(answers, ensure_ascii=False)
        await self.client.session.api.client.accounts.services.create(
            service=self.services[0]['id_str'],
            answers=answers_json,
        )
        await self.client.change_view(view=PurchaseFirstView())

    async def next_page(self, _):
        if not await self.check_errors(self.tf_answers, 1, 1024):
            return
        self.answers = {
            tf.key_question.split('_')[0]: tf.value for tf in self.tf_answers
        }
        self.answers.update({dd.key: dd.value for dd in self.dd_answers})
        if self.page_account < self.total_pages:
            self.page_account += 1
            await self.restart()

    async def previous_page(self, _):
        if self.page_account > 1:
            filled_tf_answers = [tf for tf in self.tf_answers if tf.value]
            if not await self.check_errors(filled_tf_answers, 1, 1024):
                return
        if self.page_account > 1:
            self.tf_answers = [tf for tf in self.tf_answers if tf.value]
            self.answers = {
                tf.key_question.split('_')[0]: tf.value for tf in self.tf_answers
            }
            self.answers.update({dd.key: dd.value for dd in self.dd_answers})
            self.page_account -= 1
            await self.restart()
