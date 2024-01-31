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

from flet_core import Column, Row, Container, MainAxisAlignment, Image, ResponsiveRow

from app.controls.button import FilledButton
from app.controls.information import Text
from app.utils import Fonts, Icons
from app.views.client.meal import MealView
from app.views.client.meal.get_week import MealWeekView
from app.views.client.training.get import TrainingView
from app.views.main.tabs.base import BaseTab


class Meal:
    name: str
    nutrients: list[int]
    meal_report_id: int = None
    on_click: Any

    def __init__(self, name: str, nutrients: list[int], on_click: Any, meal_report_id: int = None):
        self.name = name
        self.nutrition = nutrients
        self.meal_report_id = meal_report_id
        self.on_click = on_click


class Training:
    name: str
    on_click: Any

    def __init__(self, name: str, on_click: Any):
        self.name = name
        self.on_click = on_click


class MealButton(Container):
    def __init__(self, name: str, nutrients: list[int], on_click: Any, meal_report_id: int = None, prev_meal_had_report: bool = False):
        super().__init__()
        self.meal_report_id = meal_report_id
        self.on_click = on_click
        self.height = 50
        self.border_radius = 10
        self.padding = 10
        images = [
            Icons.CARBOHYDRATES,
            Icons.PROTEIN,
            Icons.FATS,
        ]
        self.name_text = Text(
            value=name,
            font_family=Fonts.REGULAR,
        )
        self.nutrient_texts = list(map(lambda value: Text(value=value, font_family=Fonts.REGULAR), nutrients))
        self.images = list(map(lambda src: Image(src=src, width=15), images))
        self.arrow_image = Image(src=Icons.NEXT, width=15)
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
        self.update_color(meal_report_id, prev_meal_had_report)

    def update_color(self, meal_report_id, prev_meal_had_report):
        if prev_meal_had_report:
            color = '#000000'
            bgcolor = '#005B0C'
        elif not meal_report_id:
            color = '#000000'
            bgcolor = '#B3E5B9'
        else:
            color = '#FFFFFF'
            bgcolor = '#008F12'

        self.bgcolor = bgcolor
        self.update_text_and_image_color(color)

    def update_text_and_image_color(self, color):
        self.name_text.color = color
        self.arrow_image.color = color
        for text in self.nutrient_texts:
            text.color = color
        for image in self.images:
            image.color = color


class HomeTab(BaseTab):
    meals: dict = None
    trainings: dict = None
    exercise: list[dict] = None
    training: dict = None
    account_service_id: int
    date: str

    async def build(self):
        now = datetime.now()
        self.date = now.strftime('%Y-%m-%d')
        self.account_service_id = self.client.session.account_service.id
        self.meals = await self.client.session.api.client.meal.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        self.trainings = await self.client.session.api.client.training.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        self.exercise = []
        if self.trainings:
            self.training = await self.client.session.api.client.training.get(
                id_=self.trainings[0]['id'],
            )
            for i, training in enumerate(self.training['exercises']):
                training_info = await self.client.session.api.client.exercise.get(id_=training['exercise'])
                # Находим соответствующий продукт в self.exercise['exercise']
                training_exercise = self.training['exercises'][i]
                if training_exercise is not None:
                    training_info['training_exercise'] = training_exercise
                self.exercise.append(training_info)
                self.exercise.sort(key=lambda x: x['training_exercise']['priority'])

        firstname = self.client.session.account.firstname

        meals = [
            Meal(
                name=await self.client.session.gtv(key=meal['type']),
                nutrients=[meal['proteins'], meal['fats'], meal['carbohydrates']],
                meal_report_id=meal['meal_report_id'],
                on_click=partial(self.meal_view, meal['id']),
            ) for meal in self.meals
        ]

        trainings = [
            Training(
                name=str(exercise['training_exercise']['priority']) + ' ' + await self.client.session.gtv(
                    key=exercise['name_text']),
                on_click=self.training_view,
            ) for exercise in self.exercise
        ]

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='good_morning') + f', {firstname}!',
                            size=25,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        ResponsiveRow(
                            controls=[
                                Container(
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='meal_week'),
                                            size=16,
                                            font_family=Fonts.MEDIUM,
                                        ),
                                        on_click=self.meal_week_view,
                                    ),
                                    col={"xs": 4, "sm": 4, "md": 4, "lg": 4},
                                ),
                                Container(
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='training'),
                                            size=16,
                                            font_family=Fonts.MEDIUM,
                                        ),
                                        on_click=self.training,
                                    ),
                                    col={"xs": 4, "sm": 4, "md": 4, "lg": 4},
                                ),
                                Container(
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='support'),
                                            size=16,
                                            font_family=Fonts.MEDIUM,
                                        ),
                                        on_click=self.support,
                                    ),
                                    col={"xs": 4, "sm": 4, "md": 4, "lg": 4},
                                ),
                            ],
                        ),
                        Text(
                            value=await self.client.session.gtv(key='meals'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        any(meals) and Column(
                            controls=[
                                MealButton(
                                    name=meal.name,
                                    nutrients=meal.nutrition,
                                    on_click=meal.on_click,
                                    meal_report_id=meal.meal_report_id,
                                ) for meal in meals
                            ],
                        ) or Text(
                            value=await self.client.session.gtv(key='meal_planning_stage'),
                            size=15,
                            font_family=Fonts.MEDIUM,
                        ),
                        Text(
                            value=await self.client.session.gtv(key='trainings'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        any(trainings) and Container(
                            content=Column(
                                controls=[
                                    Row(
                                        controls=[
                                            Text(
                                                value=training.name,
                                                color='#FFFFFF',
                                                font_family=Fonts.REGULAR,
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    )
                                    for training in trainings
                                ]
                            ),
                            bgcolor='#008F12',
                            border_radius=10,
                            padding=10,
                        ) or Text(
                            value=await self.client.session.gtv(key='training_planning_stage'),
                            size=15,
                            font_family=Fonts.MEDIUM,
                        ),
                    ],
                    spacing=15,
                ),
                padding=10,
            ),
        ]

    async def current_meal(self, _):
        pass

    async def training_view(self, _):
        await self.client.change_view(view=TrainingView())

    async def support(self, _):
        pass

    async def meal_week_view(self, _):
        await self.client.change_view(view=MealWeekView(account_service_id=self.account_service_id))

    async def meal_view(self, meal_id, _):
        await self.client.change_view(view=MealView(meal_id=meal_id))
