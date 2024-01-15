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
    chill_time: str
    on_click: Any

    def __init__(self, name: str, chill_time: str, on_click: Any):
        self.name = name
        self.chill_time = chill_time
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
            color = '#FFFFFF'  # FIXME
            bgcolor = '#008F12'  # FIXME
        elif now > end_datetime:
            color = '#000000'  # FIXME
            bgcolor = '#A0EAA0'  # FIXME
        else:
            color = '#000000'  # FIXME
            bgcolor = '#D2E9D2'  # FIXME

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
    async def click(self, _):
        await self.client.change_view(view=MealView())

    async def build(self):

        api_response = {'state': 'suc', 'meals': [
            {'name': 'meal_1', 'belki': 10, 'jiri': 30, 'ugl': 75, 'start_time': '7:00', 'end_time': '10:00'},
            {'name': 'meal_2', 'belki': 10, 'jiri': 30, 'ugl': 75, 'start_time': '10:00', 'end_time': '13:00'},
            {'name': 'meal_3', 'belki': 10, 'jiri': 30, 'ugl': 75, 'start_time': '13:00', 'end_time': '16:00'},
            {'name': 'meal_4', 'belki': 10, 'jiri': 30, 'ugl': 75, 'start_time': '16:00', 'end_time': '19:00'},
            {'name': 'meal_5', 'belki': 10, 'jiri': 30, 'ugl': 75, 'start_time': '19:00', 'end_time': '20:00'},
        ]}

        firstname = self.client.session.account.firstname

        meals = [
            Meal(
                name=await self.client.session.gtv(key=meal.get('name')),
                nutrients=[meal.get('belki'), meal.get('jiri'), meal.get('ugl')],
                on_click=self.click,
                start_time=meal.get('start_time'),
                end_time=meal.get('end_time'),
            ) for meal in api_response['meals']
        ]

        api_response_training = {'state': 'suc', 'training': [
            {'name': 'Exercise_Name'},
            {'name': 'Exercise_Name'},
            {'name': 'Exercise_Name'},
            {'name': 'Exercise_Name'},
        ], 'chill_time': 1}

        trainings = [
            Training(
                name=await self.client.session.gtv(key=training.get('name')),
                on_click=self.click,
                chill_time=str(api_response_training['chill_time']),
            ) for training in api_response_training['training']
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
                                                         value=f"{i + 1}. {training.name}",
                                                         color='#FFFFFF',
                                                         font_family=Fonts.REGULAR,
                                                     ),
                                                 ],
                                                 alignment=MainAxisAlignment.SPACE_BETWEEN,
                                             )
                                             for i, training in enumerate(trainings)
                                         ] + [
                                             Row(
                                                 controls=[
                                                     Image(
                                                         src=Icons.CHILL,
                                                         width=15,
                                                         color='#FFFFFF'
                                                     ),
                                                     Text(
                                                         value=f"{api_response_training['chill_time']} "
                                                               + await self.client.session.gtv(key='min'),
                                                         color='#FFFFFF',
                                                         font_family=Fonts.REGULAR,
                                                     ),
                                                 ],
                                             ),
                                         ],
                            ),
                            bgcolor='#008F12',
                            border_radius=10,
                            padding=10,
                            on_click=self.training,
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
