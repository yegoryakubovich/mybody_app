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


from datetime import datetime
from functools import partial
from typing import Any

from flet_core import Column, Row, Container, MainAxisAlignment, Image, colors
from mybody_api_client.utils import ApiException
from pytz import timezone, FixedOffset

from app.controls.button import ProductChipButton
from app.controls.information import Text
from app.utils import Fonts, Icons
from app.views.client.meal import MealView, MealWeekView
from app.views.client.training.get import TrainingView
from app.views.main.tabs.base import BaseTab
from config import settings


class Meal:
    name: str
    nutrients: list[int]
    meal_report_id: int = None
    on_click: Any
    color: str = None

    def __init__(self, name: str, nutrients: list[int], on_click: Any, meal_report_id: int = None):
        self.name = name
        self.nutrients = nutrients
        self.meal_report_id = meal_report_id
        self.on_click = on_click


class Training:
    name: str
    on_click: Any

    def __init__(self, name: str, on_click: Any):
        self.name = name
        self.on_click = on_click


class MealButton(Container):
    def __init__(
            self,
            name: str,
            nutrients: list[int],
            on_click: Any,
            meal_report_id: int = None,
            color: str = None,
            bgcolor: str = None,
    ):
        super().__init__()
        self.meal_report_id = meal_report_id
        self.on_click = on_click
        self.height = 50
        self.bgcolor = bgcolor
        self.border_radius = 10
        self.padding = 10
        images = [
            Icons.CARBOHYDRATES,
            Icons.PROTEIN,
            Icons.FATS,
        ]
        self.name_text = Text(
            value=name,
            size=18,
            font_family=Fonts.SEMIBOLD,
            color=color
        )
        self.nutrient_texts = list(map(lambda value: Text(value=value, font_family=Fonts.REGULAR, color=color), nutrients))
        self.images = list(map(lambda src: Image(src=src, width=15, color=color), images))
        self.arrow_image = Image(src=Icons.NEXT, width=15, color=color)
        self.content = Row(
            controls=[
                Container(content=self.name_text, expand=7),
                Container(
                    content=Row(
                        controls=[
                            control
                            for i, text in enumerate(self.nutrient_texts)
                            for control in (self.images[i], text)
                        ],
                        spacing=10,
                    ),
                    expand=11,
                ),
                self.arrow_image
            ],
            expand=True,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )


class HomeTab(BaseTab):
    meals: list[dict] = None
    trainings: dict = None
    exercise: list[dict] = None
    account_service_id: int
    date: str
    user_tz: timezone

    async def build(self):
        await self.set_type(loading=True)
        deviation = await self.client.session.api.client.timezones.get(
            id_str=self.client.session.account.timezone,
        )
        self.user_tz = FixedOffset(deviation.deviation)
        self.date = datetime.now(self.user_tz).strftime('%Y-%m-%d')
        self.account_service_id = self.client.session.account_service.id
        self.meals = await self.client.session.api.client.meals.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        self.meals = sorted(
            self.meals,
            key=lambda meal: int(meal['type'].split('_')[1]),
        )
        try:
            self.trainings = await self.client.session.api.client.trainings.get_by_date(
                account_service_id=self.account_service_id,
                date=self.date,
            )
        except ApiException:
            self.trainings = {}
        await self.set_type(loading=False)

        self.exercise = []
        if self.trainings:
            for i, training in enumerate(self.trainings['exercises']):
                training_info = await self.client.session.api.client.exercises.get(
                    id_=training['exercise'],
                )
                training_exercise = self.trainings['exercises'][i]
                if training_exercise:
                    training_info['training_exercise'] = training_exercise
                self.exercise.append(training_info)
                self.exercise.sort(key=lambda x: x['training_exercise']['priority'])

        meals_buttons = []
        current_meal_with_report = False
        next_meal_after_report = False
        first_meal = False

        if not any(meal['meal_report_id'] for meal in self.meals):
            first_meal = True

        for meal in self.meals:
            if first_meal:
                meal_color = colors.ON_PRIMARY
                meal_bgcolor = colors.PRIMARY
                first_meal = False
            elif meal['meal_report_id']:
                meal_color = colors.ON_PRIMARY_CONTAINER
                meal_bgcolor = colors.PRIMARY_CONTAINER
                current_meal_with_report = True
            elif not meal['meal_report_id'] and current_meal_with_report and not next_meal_after_report:
                meal_color = colors.ON_PRIMARY
                meal_bgcolor = colors.PRIMARY
                next_meal_after_report = True
            else:
                meal_color = colors.ON_BACKGROUND
                meal_bgcolor = colors.SURFACE

            meal_button = MealButton(
                name=await self.client.session.gtv(key=meal['type']),
                nutrients=[meal['proteins'], meal['fats'], meal['carbohydrates']],
                on_click=partial(self.meal_view, meal['id']),
                meal_report_id=meal['meal_report_id'],
                color=meal_color,
                bgcolor=meal_bgcolor
            )
            meals_buttons.append(meal_button)

        trainings = [
            Training(
                name=str(exercise['training_exercise']['priority']) + '. ' + await self.client.session.gtv(
                    key=exercise['name_text']),
                on_click=self.training_view,
            ) for exercise in self.exercise
        ]

        current_time = datetime.now(self.user_tz)
        current_hour = current_time.hour
        if 6 <= current_hour < 12:
            greeting_key = 'good_morning'
        elif 12 <= current_hour < 18:
            greeting_key = 'good_afternoon'
        elif 18 <= current_hour < 23.59:
            greeting_key = 'good_evening'
        else:
            greeting_key = 'good_night'

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(
                                key=greeting_key
                            ) + f', {self.client.session.account.firstname}!',
                            size=25,
                            font_family=Fonts.BOLD,
                            color=colors.ON_BACKGROUND,
                        ),
                        Row(
                            controls=[
                                ProductChipButton(
                                    text=await self.client.session.gtv(key='meal_week'),
                                    on_click=self.meal_week_view,
                                ),
                                ProductChipButton(
                                    text=await self.client.session.gtv(key='training'),
                                    on_click=self.training_view,
                                ),
                                ProductChipButton(
                                    text=await self.client.session.gtv(key='support'),
                                    url=settings.url_telegram
                                ),
                            ],
                            wrap=True,
                        ),
                        Text(
                            value=await self.client.session.gtv(key='meals'),
                            size=25,
                            font_family=Fonts.BOLD,
                            color=colors.ON_BACKGROUND,
                        ),
                        any(meals_buttons) and Column(
                            controls=meals_buttons
                        ) or Text(
                            value=await self.client.session.gtv(key='meal_planning_stage'),
                            size=15,
                            font_family=Fonts.MEDIUM,
                            color=colors.ON_BACKGROUND,
                        ),
                        Text(
                            value=await self.client.session.gtv(key='training'),
                            size=25,
                            font_family=Fonts.BOLD,
                            color=colors.ON_BACKGROUND,
                        ),
                        any(trainings) and Container(
                            content=Row(
                                controls=[
                                    Container(
                                        content=Column(
                                            controls=[
                                                Row(
                                                    controls=[
                                                        Text(
                                                            value=training.name,
                                                            size=10,
                                                            color=colors.ON_PRIMARY_CONTAINER,
                                                            font_family=Fonts.REGULAR,
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                )
                                                for training in trainings
                                            ],
                                            spacing=1,
                                        ),
                                    ),
                                    Container(
                                        content=Image(
                                            src=Icons.NEXT,
                                            width=15,
                                            color=colors.ON_PRIMARY,
                                        ),
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=10,
                            bgcolor=colors.PRIMARY_CONTAINER,
                            border_radius=10,
                            on_click=self.training_view
                        ) or Text(
                            value=await self.client.session.gtv(key='training_planning_stage'),
                            size=15,
                            font_family=Fonts.MEDIUM,
                            color=colors.ON_BACKGROUND,
                        )

                    ],
                ),
                padding=10,
            ),
        ]

    async def training_view(self, _):
        if self.trainings and self.trainings['id']:
            training_id = self.trainings['id']
        else:
            training_id = None

        await self.client.change_view(
            view=TrainingView(
                exercise=self.exercise,
                training_id=training_id,
            ),
        )

    async def meal_week_view(self, _):
        await self.client.change_view(view=MealWeekView(account_service_id=self.account_service_id))

    async def meal_view(self, meal_id, _):
        await self.client.change_view(view=MealView(meal_id=meal_id))
