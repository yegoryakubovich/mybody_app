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


from flet_core import ScrollMode, ExpansionPanel, ListTile, ExpansionPanelList

from app.controls.information import Text
from app.controls.layout import ClientBaseView


class QuestionView(ClientBaseView):
    async def build(self):
        self.scroll = ScrollMode.AUTO
        questions_answers = {
            await self.client.session.gtv(key='Сколько зарплата?'):
                await self.client.session.gtv(key='многаааа'),
            await self.client.session.gtv(key='Хотите денег? Есть темка'):
                await self.client.session.gtv(key='егор дай денег')
        }
        expansion_panels = [
            ExpansionPanel(
                header=ListTile(
                    title=Text(value=question),
                ),
                content=ListTile(
                    title=Text(value=answer),
                ),
            )
            for question, answer in questions_answers.items()
        ]
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='faq'),
            main_section_controls=[
                ExpansionPanelList(
                    controls=expansion_panels
                ),
            ],
        )
