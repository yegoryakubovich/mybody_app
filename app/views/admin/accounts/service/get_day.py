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

from flet_core import ScrollMode, colors, Row
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text, SnackBar
from app.controls.information.card import Card
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts
from app.views.admin.accounts.service.meal.create import AccountMealCreateView
from app.views.admin.accounts.service.meal.get import AccountMealView
from app.views.admin.accounts.service.report.get_list import ReportListView
from app.views.admin.accounts.service.training.exercise import AccountTrainingExerciseView, \
    AccountTrainingExerciseCreateView


class DayView(AdminBaseView):
    route = '/admin/account/service/day/get'
    day: dict
    tf_water_amount: TextField
    role: list
    meals: list[dict]
    training: dict
    exercises: list[dict]
    snack_bar: SnackBar
    dd_type: Dropdown
    tf_date: TextField
    dd_articles: Dropdown
    snack_bar: SnackBar
    meals_reports_ids: dict

    def __init__(self, day_id):
        super().__init__()
        self.day_id = day_id

    async def build(self):
        await self.set_type(loading=True)
        self.day = await self.client.session.api.admin.days.get(id_=self.day_id)
        self.exercises = []
        if self.day['training']['exercises']:
            for i, training in enumerate(self.day['training']['exercises']):
                training_info = await self.client.session.api.client.exercises.get(id_=training['exercise'])
                training_exercise = self.day['training']['exercises'][i]
                if training_exercise:
                    training_info['training_exercise'] = training_exercise
                self.exercises.append(training_info)
        await self.set_type(loading=False)

        self.meals_reports_ids = {
            meal['type']: meal['meal_report_id'] for meal in self.day['meals'] if meal['meal_report_id'] is not None
        }
        self.exercises.sort(key=lambda x: x['training_exercise']['priority'])
        self.meals = self.day['meals']
        self.meals = sorted(
            self.meals,
            key=lambda meal: int(meal['type'].split('_')[1])
        )
        self.tf_water_amount = TextField(
            label=await self.client.session.gtv(key='water_amount'),
            value=self.day['water_amount'],
        )
        self.snack_bar = SnackBar(
            content=Text(
                value=await self.client.session.gtv(key='successful'),
            ),
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=self.day['date'],
            main_section_controls=[
                self.snack_bar,
                self.tf_water_amount,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_day,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_day,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='report'),
                            ),
                            on_click=self.view_report,
                        ),
                    ],
                ),
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='meals'),
                    create_button=self.create_meal,
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key=meal['type']),
                                    size=18,
                                    font_family=Fonts.SEMIBOLD,
                                    color=colors.ON_PRIMARY,
                                ),
                            ],
                            on_click=partial(self.meal_view, meal['meal_id']),
                        )
                        for meal in self.meals
                    ],
                ),
                Section(
                    title=await self.client.session.gtv(key='exercises'),
                    create_button=self.create_exercise,
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key=exercise['name_text']),
                                    size=18,
                                    font_family=Fonts.SEMIBOLD,
                                    color=colors.ON_PRIMARY,
                                ),
                            ],
                            on_click=partial(self.exercise_view, exercise),
                        )
                        for exercise in self.exercises
                    ],
                )
            ],
        )

    async def update_day(self, _):
        try:
            await self.set_type(loading=True)
            await self.client.session.api.admin.days.update(
                id_=self.day['id'],
                water_amount=self.tf_water_amount.value,
            )
            await self.set_type(loading=False)
            self.snack_bar.open = True
            await self.update_async()
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)

    async def delete_day(self, _):
        await self.client.session.api.admin.days.delete(id_=self.day['id'])
        await self.client.change_view(go_back=True, delete_current=True, with_restart=True)

    async def exercise_view(self, exercise, _):
        await self.client.change_view(
            AccountTrainingExerciseView(
                exercise=exercise,
                exercises_training=self.exercises,
                training_id=self.day['training']['id'],
            ),
        )

    async def create_exercise(self, _):
        await self.client.change_view(
            AccountTrainingExerciseCreateView(
                training_id=self.day['training']['id'],
                exercises=self.exercises,
            ),
        )

    async def meal_view(self, meal_id, _):
        await self.client.change_view(view=AccountMealView(meal_id=meal_id))

    async def create_meal(self, _):
        await self.client.change_view(
            view=AccountMealCreateView(
                account_service_id=self.day['account_service_id'],
                meal_date=self.day['date'],
            ),
        )

    async def view_report(self, _):
        await self.client.change_view(
            view=ReportListView(
                training_report_id=self.day['training']['training_report_id'],
                training_id=self.day['training']['id'],
                meals_reports_ids=self.meals_reports_ids,
            ),
        )

