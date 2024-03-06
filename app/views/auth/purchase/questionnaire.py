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

from flet_core import Row, MainAxisAlignment, ScrollMode
from flet_core.dropdown import Option

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
    service_id_str: str

    def __init__(self, gender, dd_answers, tf_answers):
        super().__init__(scroll=ScrollMode.AUTO)
        self.gender = gender
        self.dd_answers = dd_answers
        self.tf_answers = tf_answers

    async def build(self):
        await self.set_type(loading=True)
        self.services = await self.client.session.api.client.services.get_list()
        self.service = await self.client.session.api.client.services.get(
            id_str=self.services[0]['id_str'],
        )
        await self.set_type(loading=False)
        titles = json.loads(self.service.questions)
        if self.gender == 'Men':
            titles = [title for title in titles if title['title'] != 'service_1_questions_3']
        self.total_pages = len(titles)

        title = titles[self.page_account - 1]
        controls = []
        for question in title['questions']:
            controls.append(
                Text(
                    value=await self.client.session.gtv(key=question['name']),
                    size=15,
                    font_family=Fonts.REGULAR,
                ),
            )
            if question['type'] == 'dropdown':
                value_options = [
                    Option(
                        text=await self.client.session.gtv(key=value),
                        key=value,
                    ) for value in question['values']
                ]
                initial_value = self.client.session.answers.get(question['key'], value_options[0].key)
                dd_answer = Dropdown(
                    label=await self.client.session.gtv(key='answer'),
                    value=initial_value,
                    options=value_options,
                    key=question['key'],
                )
                self.dd_answers.append(dd_answer)
                controls.append(dd_answer)
            else:
                initial_value = self.client.session.answers.get(question['key'])
                tf_answer = TextField(
                    label=await self.client.session.gtv(key='answer'),
                    value=initial_value,
                    key_question=f"{question['key']}_{question['type']}",
                )
                self.tf_answers.append(tf_answer)
                controls.append(tf_answer)

        pagination_controls = [
            Row(
                controls=[
                    PaginationWidget(
                        current_page=self.page_account,
                        total_pages=self.total_pages,
                        on_back=self.previous_page,
                        on_next=self.next_page if self.page_account < self.total_pages else self.send_form,
                        text_back=await self.client.session.gtv(key='back'),
                        text_next=await self.client.session.gtv(key='next'),
                        disable_next_button=False,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=title['title']),
            go_back=True,
            controls=controls + pagination_controls,
        )

    async def check_errors(self, field_list, min_len, max_len):
        for field in field_list:
            key_question_parts = field.key_question.split('_')
            type_ = key_question_parts[-1]
            check_int = type_ == 'int'
            if not await Error.check_field(self, field, check_int=check_int, min_len=min_len, max_len=max_len):
                return False
        return True

    async def send_form(self, _):
        if not await self.check_errors(self.tf_answers, 1, 1024):
            return

        answers = {
            '_'.join(tf.key_question.split('_')[:-1]): int(tf.value) if tf.key_question.split('_')[
                                                                            -1] == 'int' else tf.value
            for tf in self.tf_answers
        }
        answers.update({dd.key: dd.value for dd in self.dd_answers})

        # Проверка и добавление ключей, если они отсутствуют
        for key in ['service_1_questions_3_1', 'service_1_questions_3_2', 'service_1_questions_3_3']:
            if key not in answers:
                answers[key] = 'no answers'

        answers_json = json.dumps(answers, ensure_ascii=False)

        account_service = await self.client.session.api.client.accounts.services.create(
            service=self.services[0]['id_str'],
            answers=answers_json,
        )
        self.client.session.account_service = account_service
        await self.client.change_view(view=PurchaseFirstView(), delete_current=True)

    async def next_page(self, _):
        if not await self.check_errors(self.tf_answers, 1, 1024):
            return
        self.client.session.answers = {
            '_'.join(tf.key_question.split('_')[:-1]): tf.value for tf in self.tf_answers
        }
        self.client.session.answers.update({dd.key: dd.value for dd in self.dd_answers})
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
            self.client.session.answers = {
                '_'.join(tf.key_question.split('_')[:-1]): tf.value for tf in self.tf_answers
            }
            self.client.session.answers.update({dd.key: dd.value for dd in self.dd_answers})
            self.page_account -= 1
            await self.restart()

    async def logout(self, _):
        await self.client.session.set_cs(key='token', value=None)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView(), delete_current=True)
