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

from flet_core import Row

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView


class AccountServiceView(AdminBaseView):
    route = '/admin/accounts/service/get'
    account = list
    service = list

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='individual_nutrition_plan'),
            main_section_controls=[
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='meals'),
                            ),
                            on_click=self.meal_view,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='trainings'),
                            ),
                            on_click=self.training_view,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='go_questionnaire'),
                            ),
                            on_click=self.questionnaire_view,
                        ),
                    ],
                    wrap=True,
                )
            ],
        )

    async def training_view(self, _):
        from app.views.admin.accounts.service.training import AccountTrainingListView
        await self.client.change_view(view=AccountTrainingListView(account_service_id=self.account_service_id))

    async def meal_view(self, _):
        from app.views.admin.accounts.service.meal import AccountMealListAllView
        await self.client.change_view(view=AccountMealListAllView(account_service_id=self.account_service_id))

    async def questionnaire_view(self, _):
        from app.views.admin.accounts.service.questionnaire import AccountQuestionnaireGetView
        await self.client.change_view(view=AccountQuestionnaireGetView(account_service_id=self.account_service_id))
