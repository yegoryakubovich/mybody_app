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


from flet_core import ScrollMode, ExpansionPanel, ListTile, ExpansionPanelList, colors

from app.controls.information import Text
from app.controls.layout import ClientBaseView


class FAQView(ClientBaseView):
    route = '/client/FAQ/'

    async def build(self):
        questions_answers = {}
        i = 1
        while True:
            question_key = f'faq_question_{i}'
            answer_key = f'faq_answer_{i}'
            question = await self.client.session.gtv(key=question_key)
            answer = await self.client.session.gtv(key=answer_key)
            if '404' in question or '404' in answer:
                break
            questions_answers[question] = answer
            i += 1

        expansion_panels = [
            ExpansionPanel(
                header=ListTile(
                    title=Text(value=question, color=colors.ON_PRIMARY),
                ),
                content=ListTile(
                    title=Text(value=answer, color=colors.ON_PRIMARY),
                ),
                bgcolor=colors.PRIMARY,
            )
            for question, answer in questions_answers.items()
        ]

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title='FAQ',
            main_section_controls=[
                ExpansionPanelList(
                    controls=expansion_panels,
                    divider_color=colors.BACKGROUND,
                    expand_icon_color=colors.ON_PRIMARY,
                ),
            ],
        )
