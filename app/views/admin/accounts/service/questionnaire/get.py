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

from flet_core import ScrollMode

from app.controls.information import Text
from app.controls.layout import AdminBaseView
from app.utils import Fonts


class AccountQuestionnaireGetView(AdminBaseView):
    route = '/admin/account/service/questionnaire/get'
    service = list

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.service = await self.client.session.api.admin.accounts.services.get(
            id_=self.account_service_id,
        )
        await self.set_type(loading=True)
        self.scroll = ScrollMode.AUTO
        questions = json.loads(self.service['questions'])
        answers = json.loads(self.service['answers'])

        main_section_controls = []
        for section in questions:
            for question in section['questions']:
                key = question['key']
                answer = answers.get(key, '')
                question_text = Text(
                    value=await self.client.session.gtv(key=question['name_text']),
                    size=16,
                    font_family=Fonts.SEMIBOLD,
                )
                answer_text = Text(
                    value=str(answer),
                    size=14,
                    font_family=Fonts.REGULAR,
                )
                main_section_controls.extend([question_text, answer_text])

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='questionnaire'),
            main_section_controls=main_section_controls,
        )