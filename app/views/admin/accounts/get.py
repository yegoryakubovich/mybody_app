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


from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.meal.get_list import AccountMealListView
from app.views.admin.accounts.role import AccountRoleListView
from app.views.admin.accounts.service.get import AccountServiceView
from app.views.admin.accounts.training import AccountTrainingListView


class AccountView(AdminBaseView):
    route = '/admin/accounts/get'
    account = list
    service = list
    account_service = list

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    async def build(self):
        await self.set_type(loading=True)
        self.account = await self.client.session.api.admin.account.get(
            id_=self.account_id
        )
        await self.set_type(loading=False)

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_get_view_title'),
            main_section_controls=[
                Text(
                    value=await self.client.session.gtv(key='basic_information'),
                    size=20,
                    font_family=Fonts.SEMIBOLD,
                ),
                Text(
                    value=f"{await self.client.session.gtv(key='firstname')}: {self.account['firstname']}\n"
                          f"{await self.client.session.gtv(key='lastname')}: {self.account['lastname']}\n"
                          f"{await self.client.session.gtv(key='surname')}: "
                          f"{self.account['surname'] if self.account['surname'] else await self.client.session.gtv(key='absent')}",
                    size=15,
                    font_family=Fonts.MEDIUM,
                ),
                Text(
                    value=await self.client.session.gtv(key='contact_details'),
                    size=20,
                    font_family=Fonts.SEMIBOLD,
                ),
                Text(
                    value=f"{await self.client.session.gtv(key='country')}: {self.account['country']}\n"
                          f"{await self.client.session.gtv(key='language')}: {self.account['language']}\n",
                    size=15,
                    font_family=Fonts.MEDIUM,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='roles'),
                    ),
                    on_click=self.role_view,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='meal'),
                    ),
                    on_click=self.meal_view,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='training'),
                    ),
                    on_click=self.training_view,
                ),
            ],
        )

    async def delete_article(self):
        pass

    async def role_view(self, _):
        await self.client.change_view(view=AccountRoleListView(account_id=self.account_id))

    async def service_view(self, _):
        await self.client.change_view(view=AccountServiceView(account_id=self.account_id))

    async def meal_view(self, _):
        account_service_id = 4
        await self.client.change_view(view=AccountMealListView(account_service_id=account_service_id))

    async def training_view(self, _):
        account_service_id = 4
        await self.client.change_view(view=AccountTrainingListView(account_service_id=account_service_id))
