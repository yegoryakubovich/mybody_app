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


from functools import partial

from flet_core import ScrollMode

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.service.meal.create import AccountMealCreateView
from app.views.admin.accounts.service.meal.get import AccountMealView


class AccountMealListView(AdminBaseView):
    route = '/admin/account/meals/list/get'
    meals: list[dict]
    role: list

    def __init__(self, account_service_id, meal_date):
        super().__init__()
        self.meal_date = meal_date
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.meals = await self.client.session.api.admin.meal.get_list(
            account_service_id=self.account_service_id,
            date=self.meal_date,
        )
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=self.meal_date,
            on_create_click=self.create_meal,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key=meal['type']),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=partial(self.meal_view, meal['id']),
                )
                for meal in self.meals
            ],
        )

    async def meal_view(self, meal, _):
        await self.client.change_view(view=AccountMealView(meal_id=meal))

    async def create_meal(self, _):
        await self.client.change_view(
            view=AccountMealCreateView(
                account_service_id=self.account_service_id,
                meal_date=self.meal_date,
            ),
        )
