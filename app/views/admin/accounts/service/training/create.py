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


from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.input.textfielddate import TextFieldDate
from app.controls.layout import AdminBaseView


class AccountTrainingCreateView(AdminBaseView):
    route = '/admin/account/training/create'
    tf_date: TextField
    dd_articles: Dropdown

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        self.tf_date = TextFieldDate(
            label=await self.client.session.gtv(key='date'),
            client=self.client,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_create_view_title'),
            main_section_controls=[
                self.tf_date,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_training,
                ),
            ],
        )

    async def create_training(self, _):
        from app.views.admin.accounts.service.training.get import AccountTrainingView
        await self.set_type(loading=True)
        try:
            training_id = await self.client.session.api.admin.trainings.create(
                account_service_id=self.account_service_id,
                date=self.tf_date.value,
            )
            await self.set_type(loading=False)
            await self.client.change_view(AccountTrainingView(training_id=training_id), delete_current=True)
        except ApiException as code:
            await self.set_type(loading=False)
            return await self.client.session.error(code=code)
