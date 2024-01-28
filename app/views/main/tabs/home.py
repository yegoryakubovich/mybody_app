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
from typing import Any

from flet_core import Column, Row, Container, MainAxisAlignment, Image

from app.controls.button import FilledButton
from app.controls.information import Text
from app.utils import Fonts, Icons
from app.views.auth.service import ServiceListView
from app.views.main.meal.meal import MealView
from app.views.main.tabs.base import BaseTab
from app.views.main.training.training import TrainingView


class Meal:
    name: str
    nutrients: list[int]
    start_time: str
    end_time: str
    on_click: Any

    def __init__(self, name: str, nutrients: list[int], end_time: str, start_time: str, on_click: Any):
        self.name = name
        self.nutrition = nutrients
        self.start_time = start_time
        self.end_time = end_time
        self.on_click = on_click


class Training:
    name: str
    on_click: Any

    def __init__(self, name: str, on_click: Any):
        self.name = name
        self.on_click = on_click


class MealButton(Container):
    def __init__(self, name, nutrients: list[int], start_time, end_time, on_click):
        super().__init__()
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
        self.update_color(start_time, end_time)

    def update_color(self, start_time, end_time):
        now = datetime.now().time()
        start_datetime = datetime.strptime(start_time, '%H:%M').time()
        end_datetime = datetime.strptime(end_time, '%H:%M').time()

        if start_datetime <= now <= end_datetime:
            color = '#FFFFFF'
            bgcolor = '#008F12'
        elif now > end_datetime:
            color = '#000000'
            bgcolor = '#A0EAA0'
        else:
            color = '#000000'
            bgcolor = '#D2E9D2'

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
    meals: dict
    trainings: dict
    date: str

    async def click(self, _):
        await self.client.change_view(view=MealView())

    async def build(self):
        self.date = '2024-01-17'
        account_service_id = 4
        self.meals = await self.client.session.api.admin.meal.get_list(
            account_service_id=account_service_id,
            date=self.date,
        )
        for meal in self.meals:
            if meal['type'] == 'meal_1':
                meal['start_time'] = '7:00'
                meal['end_time'] = '10:00'
            elif meal['type'] == 'meal_2':
                meal['start_time'] = '10:00'
                meal['end_time'] = '13:00'
            elif meal['type'] == 'meal_3':
                meal['start_time'] = '13:00'
                meal['end_time'] = '16:00'
            elif meal['type'] == 'meal_4':
                meal['start_time'] = '16:00'
                meal['end_time'] = '19:00'
            elif meal['type'] == 'meal_5':
                meal['start_time'] = '19:00'
                meal['end_time'] = '20:00'
        self.trainings = await self.client.session.api.client.training.get_list(
            account_service_id=account_service_id,
            date='2024-01-21',
        )
        self.training = await self.client.session.api.client.training.get(
            id_=self.trainings[0]['id'],
        )
        self.exercise = []
        for i, training in enumerate(self.training['exercises']):
            training_info = await self.client.session.api.client.exercise.get(id_=training['exercise'])
            # Находим соответствующий продукт в self.exercise['exercise']
            training_exercise = self.training['exercises'][i]
            if training_exercise is not None:
                training_info['training_exercise'] = training_exercise
            self.exercise.append(training_info)
        firstname = self.client.session.account.firstname

        meals = [
            Meal(
                name=await self.client.session.gtv(key=meal['type']),
                nutrients=[meal['proteins'], meal['fats'], meal['carbohydrates']],
                start_time=meal['start_time'],
                end_time=meal['end_time'],
                on_click=self.click,
            ) for meal in self.meals
        ]

        self.exercise.sort(key=lambda x: x['training_exercise']['priority'])
        trainings = [
            Training(
                name=str(exercise['training_exercise']['priority']) + ' ' + await self.client.session.gtv(
                    key=exercise['name_text']),
                on_click=self.click,
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
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='main_tabs_home_view_current_meal'),
                                        size=16,
                                        font_family=Fonts.MEDIUM,
                                    ),
                                    on_click=self.current_meal,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='training'),
                                        size=16,
                                        font_family=Fonts.MEDIUM,
                                    ),
                                    on_click=self.training,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='support'),
                                        size=16,
                                        font_family=Fonts.MEDIUM,
                                    ),
                                    on_click=self.support,
                                ),
                            ],
                        ),
                        Text(
                            value=await self.client.session.gtv(key='meals'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        Column(
                            controls=[
                                MealButton(
                                    name=meal.name,
                                    nutrients=meal.nutrition,
                                    on_click=meal.on_click,
                                    start_time=meal.start_time,
                                    end_time=meal.end_time,
                                ) for meal in meals
                            ],
                        ),
                        Text(
                            value=await self.client.session.gtv(key='trainings'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        Container(
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
                        ),
                    ],
                    spacing=15,
                ),
                padding=10,
            ),
        ]

    async def current_meal(self, _):
        pass

    async def training(self, _):
        await self.client.change_view(view=TrainingView())

    async def support(self, _):
        pass
