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
from datetime import datetime, timedelta

from flet_core import Text, ScrollMode, Column

from app.controls.layout import ClientBaseView
from app.utils import Fonts

from collections import defaultdict


class MealWeekView(ClientBaseView):
    meals: list[dict]
    role: list
    date: str = None

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        from app.views.main.tabs.home import MealButton
        await self.set_type(loading=True)
        print(self.date)
        self.meals = await self.client.session.api.client.meals.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        await self.set_type(loading=False)

        # Получение текущей даты и даты через 6 дней
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=6)

        # Фильтрация и группировка приемов пищи по датам
        meals_by_date = defaultdict(list)
        for meal in self.meals:
            meal_date = datetime.strptime(meal['date'], '%Y-%m-%d').date()
            if start_date <= meal_date <= end_date:
                meals_by_date[meal['date']].append(
                    MealButton(
                        name=await self.client.session.gtv(key=meal['type']),
                        nutrients=[meal['proteins'], meal['fats'], meal['carbohydrates']],
                        meal_report_id=meal['meal_report_id'],
                        on_click=partial(self.meal_view, meal['id']),
                    )
                )

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='client_meal_get_week_view_title'),
            main_section_controls=[
                Column(
                    controls=[
                        Text(
                            value=date,
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        *meals
                    ]
                )
                for date, meals in sorted(meals_by_date.items())
            ]
        )

    async def meal_view(self, meal_id, _):
        from app.views import MealView
        await self.client.change_view(view=MealView(meal_id=meal_id))
