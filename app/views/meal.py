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


from typing import Any

from flet_core import Column, Container, Image, Row, ScrollMode, Text, padding
from flet_manager.utils import get_svg

from app.views.meal_report import MealReportView
from app.controls.button import FilledButton
from app.controls.button.product_chip import ProductChipButton
from app.controls.layout import View
from app.utils import Fonts


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
    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def go_meal_report(self, _):
        await self.client.change_view(view=MealReportView())

    async def build(self):
        self.bgcolor = '#FFFFFF'  # FIXME
        self.scroll = ScrollMode.ALWAYS

        products = ['Rise', 'Buckwheat', 'Oatmeal', 'Barley']  # FIXME

        sections_list = [
            {
                'name': await self.client.session.gtv(key='Carbohydrates'),
                'icon': 'carbohydrates',
            },
            {
                'name': await self.client.session.gtv(key='Proteins'),
                'icon': 'protein',
            },
            {
                'name': await self.client.session.gtv(key='Fats'),
                'icon': 'fats',
            },
        ]  # FIXME

        sections = [
            Section(
                name=section['name'],  # FIXME
                icon=section['icon'],
                meals=[
                    Meal(
                        name=product,
                        weight='120',
                        on_click=None,  # FIXME
                        is_active=False,
                    ) for product in products
                ],
            ) for section in sections_list
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
                                                font_family=Fonts.BOLD,
                                                color='#000000',  # FIXME
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
                                            ProductChipButton(
                                                f'{meal.name} {meal.weight}{await self.client.session.gtv(key="g")}'
                                            )
                                            for meal in section.meals
                                        ],
                                        wrap=True,
                                    ),
                                ],
                                spacing=0,
                            ),
                            padding=padding.only(bottom=15),
                        ) for section in sections
                    ],
                    spacing=10,
                ),
            )
        ]

        self.controls = self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        Container(
                            Row(
                                controls=[
                                    Container(
                                        Image(
                                            src=get_svg(
                                                path=f'assets/icons/arrow_back.svg',
                                            ),
                                            color='#000000',  # FIXME
                                            height=20,
                                        ),
                                        on_click=self.go_back,  # FIXME
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key='Mealtime'),  # FIXME
                                        size=30,
                                        font_family=Fonts.BOLD,
                                        color='#000000',  # FIXME
                                    ),
                                ],
                            ),
                            padding=padding.only(bottom=15)
                        ),
                        Container(
                            Text(
                                value=await self.client.session.gtv(key='Dont_Forget_To_Make_a_Report'),  # FIXME
                                size=18,
                                color='#000000',
                                font_family=Fonts.REGULAR,
                            ),
                            padding=padding.only(bottom=15),
                        ),
                    ] + sections_controls + [
                        Container(
                            Text(
                                value=await self.client.session.gtv(key='Indicated_Finish_Weight'),  # FIXME
                                size=18,
                                color='#000000',
                                font_family=Fonts.REGULAR,
                            ),
                            padding=padding.only(bottom=15),  # FIXME
                        ),
                        Container(
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='Make_a_Report'),
                                    size=14,
                                    color='#ffffff',
                                    font_family=Fonts.REGULAR,
                                ),
                                on_click=self.go_meal_report,
                            ),
                        )
                    ],
                    spacing=0,
                ),
                padding=15,
            )
        ]
