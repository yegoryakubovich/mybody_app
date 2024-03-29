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

from flet_core import ScrollMode
from flet_core.dropdown import Option
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class AccountMealCreateView(AdminBaseView):
    route = '/admin/account/meal/create'
    dd_type: Dropdown
    tf_fats = TextField
    tf_proteins = TextField
    tf_carbohydrates = TextField

    def __init__(self, account_service_id, meal_date=None):
        super().__init__()
        self.meal_date = meal_date
        self.account_service_id = account_service_id

    async def build(self):
        meal_type_dict = {
            await self.client.session.gtv(key='meal_1'): 'meal_1',
            await self.client.session.gtv(key='meal_2'): 'meal_2',
            await self.client.session.gtv(key='meal_3'): 'meal_3',
            await self.client.session.gtv(key='meal_4'): 'meal_4',
            await self.client.session.gtv(key='meal_5'): 'meal_5',
        }
        meal_type_options = [
            Option(
                text=meal_type,
                key=meal_type_dict[meal_type],
            ) for meal_type in meal_type_dict
        ]
        self.dd_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=meal_type_options[0].key,
            options=meal_type_options,
        )
        self.tf_fats, self.tf_proteins, self.tf_carbohydrates = [
            TextField(
                label=await self.client.session.gtv(key=key),
            )
            for key in ['fats', 'proteins', 'carbohydrates']
        ]
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_meal_create_view_title'),
            main_section_controls=[
                self.dd_type,
                self.tf_fats,
                self.tf_proteins,
                self.tf_carbohydrates,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_meal,
                ),
            ]
        )

    async def create_meal(self, _):
        from app.views.admin.accounts.service.meal.get import AccountMealView
        fields = [(self.tf_fats, True), (self.tf_proteins, True), (self.tf_carbohydrates, True)]
        for field, check_int in fields:
            if not await Error.check_field(self, field, check_int):
                return
        try:
            await self.set_type(loading=True)
            meal_id = await self.client.session.api.admin.meals.create(
                account_service_id=self.account_service_id,
                date=self.meal_date,
                type_=self.dd_type.value,
                fats=self.tf_fats.value,
                proteins=self.tf_proteins.value,
                carbohydrates=self.tf_carbohydrates.value,
            )
            await self.set_type(loading=False)
            await self.client.change_view(AccountMealView(meal_id=meal_id), delete_current=True)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
