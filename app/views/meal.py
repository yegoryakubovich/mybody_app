#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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


from typing import Any

from flet_core import ButtonStyle, Container, ElevatedButton as FletElevatedButton, FontWeight, MaterialState, \
    RoundedRectangleBorder, TextThemeStyle, padding, Column, Image, TextAlign, Row, ScrollMode, Text
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.layout import View


class Meal:
    name: str
    weight: str
    is_active: bool
    on_click: Any

    def __init__(self, name: str, weight: str, is_active: bool, on_click: Any):
        self.name = name
        self.weight = weight
        self.is_active = is_active
        self.on_click = on_click


class Section:
    name: str
    icon: str
    meals: list[Meal]

    def __init__(self, name: str, icon: str, meals: list[Meal]):
        self.name = name
        self.icon = icon
        self.meals = meals


class MealView(View):
    route = '/today'

    async def build(self):
        self.bgcolor = '#FFFFFF'  # FIXME
        self.scroll = ScrollMode.ALWAYS
        self.padding = 15

        sections = [
            Section(
                name='#Carbohydrates',  # FIXME
                icon='carbohydrates',
                meals=[
                    Meal(
                        name='Rise',  # FIXME в будущем заполняться итерацией массива
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Buckwheat',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Oatmeal',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Barley',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Oatmeal',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Oatmeal',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),

                ]
            ),
            Section(
                name='#Proteins',  # FIXME
                icon='protein',
                meals=[
                    Meal(
                        name='Rise',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Oatmeal',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Barley',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Buckwheat',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                ]
            ),
            Section(
                name='#Fats',  # FIXME
                icon='fats',
                meals=[
                    Meal(
                        name='Rise',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Rise',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Rise',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                    Meal(
                        name='Rise',
                        weight='120g',
                        on_click=None,
                        is_active=False,
                    ),
                ]
            )
        ]
        sections_controls = [
            Container(
                Column(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Row(
                                        controls=[
                                            Text(
                                                value=section.name,
                                                size=25,
                                                weight=FontWeight.BOLD,
                                                color='#000000'  # FIXME
                                            ),
                                            Image(
                                                src=get_svg(
                                                    path=f'assets/icons/{section.icon}.svg',
                                                ),
                                                color='#1d1d1d',  # FIXME
                                                height=25,
                                            ),
                                        ]
                                    ),
                                    Row(
                                        controls=[
                                            FletElevatedButton(
                                                content=Text(
                                                    value=f'{meal.name} {meal.weight}',
                                                    style=TextThemeStyle.BODY_MEDIUM,
                                                    weight=FontWeight.BOLD,
                                                    text_align=TextAlign.CENTER,
                                                    color='#000000',  # FIXME
                                                ),
                                                style=ButtonStyle(
                                                    shape={MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                                                    padding={},
                                                    overlay_color={
                                                        MaterialState.DEFAULT: '#51B62E',
                                                        MaterialState.HOVERED: '#B3DDB8',  # FIXME
                                                    },
                                                ),
                                                bgcolor='#B3DDB8',
                                                elevation=0,
                                                height=25,
                                            ) for meal in section.meals
                                        ],
                                        wrap=True
                                    ),
                                ],
                                spacing=0
                            ),
                            padding=padding.only(bottom=15),
                        ) for section in sections
                    ],
                    spacing=10,
                ),
            )
        ]

        self.controls = [
            Container(
                Row(
                    controls=[
                        Container(
                            Image(
                                src=get_svg(
                                    path=f'assets/icons/back.svg',
                                ),
                                color='#000000',  # FIXME
                                height=20,
                            ),
                            on_click=lambda _: None # FIXME
                        ),
                        Text(
                            value='#Mealtime',  # FIXME
                            size=30,
                            weight=FontWeight.BOLD,
                            color='#000000'  # FIXME
                        ),
                    ]
                ),
                padding=padding.only(bottom=15)
            ),
            Container(
                Text(
                    value='#Dont_Forget_To_Make_a_Report',  # FIXME
                    size=18,
                    color='#000000',
                ),
                padding=padding.only(bottom=15)
            ),
        ] + sections_controls + [
            Container(
                Text(
                    value='#Indicated_Finish_Weight',  # FIXME
                    size=18,
                    color='#000000'
                ),
                padding=padding.only(bottom=15)  # FIXME
            ),
            Container(
                FilledButton(
                    content=Text(
                        value='#Make_a_Report',
                        size=14,
                        color='#ffffff'
                    ),
                    style=ButtonStyle(
                        shape={MaterialState.DEFAULT: RoundedRectangleBorder(radius=4)},
                        padding={},
                        overlay_color={
                            MaterialState.DEFAULT: '#51B62E',
                            MaterialState.HOVERED: '#7ADA58',  # FIXME
                        },
                        shadow_color=None,
                    ),
                    bgcolor='#51B62E',
                    elevation=0,
                ),
            )
        ]
