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


from collections import defaultdict
from functools import partial

from flet_core import ScrollMode, Row, Container, Image, MainAxisAlignment, AlertDialog, TextButton
from mybody_api_client.utils import ApiException

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.input import TextField
from app.controls.input.textfielddate import TextFieldDate
from app.controls.layout import AdminBaseView
from app.utils import Fonts, Icons
from app.views.admin.accounts.service.meal import AccountMealListView
from app.views.admin.accounts.service.meal.create import AccountMealCreateView


class AccountMealListAllView(AdminBaseView):
    route = '/admin/account/meals/list/get'
    meals: list[dict]
    role: list
    duplicate: list[dict]
    date: str = None
    duplicate_date: str = None
    dlg_modal = AlertDialog
    tf_date_duplicate_meal = TextField

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        self.meals = await self.client.session.api.admin.meals.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        meals_by_date = defaultdict(list)
        for meal in self.meals:
            meals_by_date[meal['date']].append(meal)

        sorted_dates = sorted(meals_by_date.keys(), reverse=True)
        if sorted_dates:
            self.duplicate = meals_by_date[sorted_dates[0]]

        self.tf_date_duplicate_meal = TextFieldDate(
            label=await self.client.session.gtv(key='date'),
            client=self.client
        )
        self.dlg_modal = AlertDialog(
            content=self.tf_date_duplicate_meal,
            actions=[
                Row(
                    controls=[
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create'),
                                size=16,
                            ),
                            on_click=self.create_duplicate_meal
                        ),
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='close'),
                                size=16,
                            ),
                            on_click=self.close_dlg,
                        ),
                    ],
                    alignment=MainAxisAlignment.END
                )
            ],
            modal=False,
        )

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_meal_get_list_view_title'),
            on_create_click=self.create_meal,
            main_section_controls=[
                self.dlg_modal, ] + [
                Card(
                    controls=[
                        Row(
                            controls=[
                                Text(
                                    value=date,
                                    size=18,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                                Container(
                                    content=Row(
                                        controls=[
                                            Image(
                                                src=Icons.CREATE,
                                                height=10,
                                                color='#FFFFFF',
                                            ),
                                            Text(
                                                value=await self.client.session.gtv(key='create_duplicate'),
                                                size=13,
                                                font_family=Fonts.SEMIBOLD,
                                                color='#FFFFFF',
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    padding=7,
                                    border_radius=24,
                                    bgcolor='#008F12',
                                    on_click=partial(self.open_dlg, date),
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    on_click=partial(self.meal_view, date),
                )
                for date in sorted_dates
            ],
        )

    async def close_dlg(self, _):
        self.dlg_modal.open = False
        await self.update_async()

    async def open_dlg(self, date, _):
        self.duplicate_date = date
        self.dlg_modal.open = True
        await self.update_async()

    async def create_duplicate_meal(self, _):
        await self.set_type(loading=True)
        duplicate_meal = await self.client.session.api.admin.meals.get_list(
            account_service_id=self.account_service_id,
            date=self.duplicate_date,
        )
        try:
            for meal in duplicate_meal:
                meal_response = await self.client.session.api.admin.meals.create(
                    account_service_id=self.account_service_id,
                    date=self.tf_date_duplicate_meal.value,
                    type_=meal['type'],
                    fats=meal['fats'],
                    proteins=meal['proteins'],
                    carbohydrates=meal['carbohydrates'],
                )
                for product in meal['products']:
                    await self.client.session.api.admin.meals.products.create(
                        meal_id=meal_response,
                        product_id=product['product'],
                        value=product['value'],
                    )
            await self.set_type(loading=False)
            await self.restart()
        except ApiException as code:
            await self.set_type(loading=False)
            return await self.client.session.error(code=code)

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
