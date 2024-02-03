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
from collections import defaultdict
from datetime import timedelta, datetime

from flet_core import ScrollMode
from mybody_api_client.utils.base_section import ApiException

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.service.meal import AccountMealListView
from app.views.admin.accounts.service.meal.create import AccountMealCreateView


class AccountMealListAllView(AdminBaseView):
    route = '/admin/account/meals/list/get'
    meals: list[dict]
    role: list
    duplicate: list[dict]
    date: str = None

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        # noinspection DuplicatedCode
        await self.set_type(loading=True)
        self.meals = await self.client.session.api.admin.meal.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        meals_by_date = defaultdict(list)
        for meal in self.meals:
            meals_by_date[meal['date']].append(meal)

        sorted_dates = sorted(meals_by_date.keys(), reverse=True)
        self.duplicate = meals_by_date[sorted_dates[0]]
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_meal_get_list_view_title'),
            on_create_click=self.create_meal,
            on_create_duplicate_click=self.create_duplicate_meal,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=date,
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=partial(self.meal_view, date),
                )
                for date in sorted_dates
            ],
        )

    async def meal_view(self, meal_date, _):
        await self.client.change_view(
            view=AccountMealListView(
                meal_date=meal_date,
                account_service_id=self.account_service_id,
            ),
        )

    async def create_meal(self, _):
        await self.client.change_view(
            view=AccountMealCreateView(
                account_service_id=self.account_service_id,
            ),
        )

    async def create_duplicate_meal(self, _):
        await self.set_type(loading=True)
        try:
            for meal in self.duplicate:
                original_date = datetime.strptime(meal['date'], '%Y-%m-%d')
                new_date = original_date + timedelta(days=1)
                new_date_str = new_date.strftime('%Y-%m-%d')

                meal_response = await self.client.session.api.admin.meal.create(
                    account_service_id=self.account_service_id,
                    date=new_date_str,
                    type_=meal['type'],
                    fats=meal['fats'],
                    proteins=meal['proteins'],
                    carbohydrates=meal['carbohydrates'],
                )
                for product in meal['products']:
                    await self.client.session.api.admin.meal.create_product(
                        meal_id=meal_response,
                        product_id=product['product'],
                        value=product['value'],
                    )
            await self.set_type(loading=False)
            await self.restart()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
