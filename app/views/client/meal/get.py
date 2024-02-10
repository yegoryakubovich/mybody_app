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
from typing import Any

from flet_core import Column, Container, Image, Row, ScrollMode, Text, padding, AlertDialog

from app.controls.button import FilledButton
from app.controls.button.product_chip import ProductChipButton
from app.controls.input import TextField
from app.controls.layout import ClientBaseView
from app.utils import Fonts, Icons


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


class MealView(ClientBaseView):
    meal: dict
    products: list
    tf_product: TextField
    tf_quantity: TextField
    dlg_modal: AlertDialog

    def __init__(self, meal_id):
        super().__init__()
        self.meal_id = meal_id

    async def build(self):
        self.meal = await self.client.session.api.client.meals.get(
            id_=self.meal_id,
        )
        self.products = []
        for i, product in enumerate(self.meal['products']):
            product_info = await self.client.session.api.client.products.get(id_=product['product'])
            # Находим соответствующий продукт в self.meal['products']
            meal_product = self.meal['products'][i]
            if meal_product is not None:
                product_info['meal_product'] = meal_product
            self.products.append(product_info)

        products_by_type = defaultdict(list)
        for product in self.products:
            meal = Meal(
                name=await self.client.session.gtv(key=product['name_text']),
                weight=product['meal_product']['value'],
                on_click=None,  # FIXME
                is_active=False,
            )
            products_by_type[product['type']].append(meal)

        sections_list = [
            {
                'name': await self.client.session.gtv(key='carbohydrates'),
                'icon': Icons.CARBOHYDRATES,
                'type': 'carbohydrates',
            },
            {
                'name': await self.client.session.gtv(key='proteins'),
                'icon': Icons.PROTEIN,
                'type': 'proteins',
            },
            {
                'name': await self.client.session.gtv(key='fats'),
                'icon': Icons.FATS,
                'type': 'fats',
            },
        ]
        sections = [
            Section(
                name=section['name'],
                icon=section['icon'],
                meals=products_by_type[section['type']],
            ) for section in sections_list
        ]
        gr = await self.client.session.gtv(key="gr")
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
                                            ),
                                            Image(
                                                src=section.icon,
                                                color='#1d1d1d',
                                                height=25,
                                            )
                                        ]
                                    ),
                                    Row(
                                        controls=[
                                            ProductChipButton(
                                                text=f'{meal.name} '
                                                     f'{meal.weight}'
                                                     f' {gr}',
                                                on_click=None,
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

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.meal['type']),
            main_section_controls=[
                Text(
                    value=await self.client.session.gtv(key='client_meal_get_guide_text_info'),
                    size=18,
                    font_family=Fonts.REGULAR,
                ),
            ] + sections_controls + [
                Text(
                    value=await self.client.session.gtv(key='client_meal_get_second_text_info'),
                    size=18,
                    font_family=Fonts.REGULAR,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create_report'),
                        size=14,
                        font_family=Fonts.REGULAR,
                    ),
                    on_click=self.go_meal_report,
                ),
            ],
        )

    async def go_meal_report(self, _):
        from app.views.client.meal.report.create import MealReportView
        await self.client.change_view(view=MealReportView(meal_id=self.meal_id))
